from base64 import b64encode
import os
import requests
from requests.utils import to_native_string

from azure.cli.core.prompting import prompt, prompt_pass, NoTTYException
import azure.cli.core.azlogging as azlogging
from azure.cli.core.util import CLIError

from ._utils import (
    get_resource_group_name_by_registry_name,
    get_registry_by_name
)
from .credential import acr_credential_show
from .repository import _headers, Unauthorized, NotFound

logger = azlogging.get_az_logger(__name__)
APIUSERNAME = os.getenv('multiUser')
APIPASSWORD = os.getenv('multiPass')

def get_response_for_show(resource_group_name, registry_name, name, api_username, api_password):
    registry_name, _ = get_registry_by_name(registry_name, resource_group_name)
    id = registry_name.id
    endpoint = "http://api20170808022712.azurewebsites.net" + id + "/buildDefinitions/" + name
    response = requests.get(endpoint, headers=_headers(api_username, api_password))
    if response.status_code == 200:
        return response.json()
    raise CLIError("There was an error retrieving the resource. " + str(response.status_code))

def put_multi_arch_artifact(data, username, password, registry_name, name, resource_group_name):
    registry_name, _ = get_registry_by_name(registry_name, resource_group_name)
    id = registry_name.id
    endpoint = "http://api20170808022712.azurewebsites.net" + id + "/buildDefinitions/" + name
    response = requests.put(endpoint, json=data, headers=_headers(username, password))
    if response.status_code == 200:
        return response.json()
    raise CLIError("There was an error creating the resource. " + str(response.status_code))

def delete_multi_arch_artifact(resource_group_name, registry_name, name, api_username, api_password):
    registry_name, _ = get_registry_by_name(registry_name, resource_group_name)
    id = registry_name.id
    endpoint = "http://api20170808022712.azurewebsites.net" + id + "/buildDefinitions/" + name
    response = requests.delete(endpoint, headers=_headers(api_username, api_password))
    if response.status_code == 200:
        return "Succesfully deleted resource."
    raise CLIError("There was an error deleting the resource. " + str(response.status_code))

def _validate_user_credentials(registry_name,
                               repository,
                               multi_arch_tag,
                               platform,
                               build_name,
                               resource_group_name=None,
                               username=None,
                               password=None,
                               yaml=None):

    registry, _ = get_registry_by_name(registry_name, resource_group_name)
    location = registry.location
    login_server = registry.login_server
    #1.  if username was specified, verify that password was also specified
    if username:
        if not password:
            try:
                password = prompt_pass(msg='Password: ')
            except NoTTYException:
                raise CLIError('Please specify both username and password in non-interactive mode.')
        return create_build(location,
                            registry_name,
                            repository,
                            multi_arch_tag,
                            platform,
                            build_name,
                            login_server,
                            resource_group_name,
                            username,
                            password,
                            yaml)
    # 2.  if we still don't have credentials, attempt to get the admin
    # credentials (if enabled)
    try:
        cred = acr_credential_show(registry_name)
        username = cred.username
        password = cred.passwords[0].value
        return create_build(location,
                            registry_name,
                            repository,
                            multi_arch_tag,
                            platform,
                            build_name,
                            login_server,
                            resource_group_name,
                            username,
                            password,
                            yaml)
    except NotFound as e:
        raise CLIError(str(e))
    except Unauthorized as e:
        logger.warning("Unable to authenticate using admin login credentials: %s", str(e))
    except Exception as e:  # pylint: disable=broad-except
        logger.warning("Admin user authentication failed with message: %s", str(e))
    # 3.  if we still don't have credentials, prompt the user
    try:
        username = prompt('Username: ')
        password = prompt_pass(msg='Password: ')
    except NoTTYException:
        raise CLIError('Unable to authenticate using AAD tokens or admin login credentials. ' +
                       'Please specify both username and password in non-interactive mode.')
    return create_build(location,
                        registry_name,
                        repository,
                        multi_arch_tag,
                        platform,
                        build_name,
                        login_server,
                        resource_group_name,
                        username,
                        password,
                        yaml)

def create_build(location,
                 registry_name,
                 repository,
                 multiArch_tag,
                 platform,
                 build_name,
                 login_server,
                 resource_group_name=None,
                 username=None,
                 password=None,
                 yaml=None):

    resource_group_name = get_resource_group_name_by_registry_name(registry_name)
    if not yaml:
        tag_prefix = login_server + '/' + repository + ':'
        manifests = ""
        for key, value in platform.items():
            manifests = manifests + ("- image: " + tag_prefix + key + "\n  platform:\n    architecture: " +
                                     value.split("-")[1] + "\n    os: " + value.split("-")[0] + "\n")
        multiYaml = "image: " + tag_prefix + multiArch_tag + "\nmanifests:\n" + manifests
        request = {"location":location, "properties":{"buildType":"MultiArch",
                                                      "buildArguments":{"multiArchYaml":multiYaml,
                                                                        "username":username,
                                                                        "password":password}}}
        return put_multi_arch_artifact(request,
                                       APIUSERNAME,
                                       APIPASSWORD,
                                       registry_name,
                                       build_name,
                                       resource_group_name)
    else:
        try:
            file = open(yaml, "r")
            multiYaml = file.read()
            file.close()
            request = {"location":location, "properties":{"buildType":"MultiArch",
                                                          "buildArguments":{"multiArchYaml":multiYaml,
                                                                            "username":username,
                                                                            "password":password}}}
            return put_multi_arch_artifact(request,
                                           APIUSERNAME,
                                           APIPASSWORD,
                                           registry_name,
                                           build_name,
                                           resource_group_name)
        except FileNotFoundError as e:
            logger.warning("Unable to find file %s", str(e))

def acr_multi_build_definition_create(registry_name,
                                      repository,
                                      tags=None,
                                      multi_arch_tag=None,
                                      build_name=None,
                                      resource_group_name=None,
                                      username=None,
                                      password=None,
                                      yaml=None):
    if yaml and not build_name:
        raise CLIError("Please specify a build-name")
    if not yaml and (not multi_arch_tag or not tags):
        raise CLIError("Please specify the multiArch-tag and the tags that form the multi-architecture flux")
    if not build_name:
        build_name = repository.replace("/", ";") + ":" + multi_arch_tag
    return _validate_user_credentials(registry_name,
                                      repository,
                                      multi_arch_tag,
                                      tags,
                                      build_name,
                                      resource_group_name,
                                      username,
                                      password,
                                      yaml)

def acr_multi_build_definition_show(registry_name, build_name, resource_group_name=None):
    resource_group_name = get_resource_group_name_by_registry_name(registry_name)
    return get_response_for_show(resource_group_name, registry_name, build_name, APIUSERNAME, APIPASSWORD)

def acr_multi_build_definition_delete(registry_name, build_name, resource_group_name=None):
    resource_group_name = get_resource_group_name_by_registry_name(registry_name)
    return delete_multi_arch_artifact(resource_group_name, registry_name, build_name, APIUSERNAME, APIPASSWORD)
