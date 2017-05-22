# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import time
import json
from base64 import b64encode
import requests
from requests.utils import to_native_string

from azure.cli.core.prompting import prompt, prompt_pass, NoTTYException
from azure.cli.core.util import CLIError

from ._utils import get_registry_login_server_by_name
from ._docker_utils import get_login_access_token
from .credential import acr_credential_show

import azure.cli.core.azlogging as azlogging

logger = azlogging.get_az_logger(__name__)

_UNAUTHORIZED = 'Invalid username or password specified.'


def _basic_auth_str(username, password):
    return 'Basic ' + to_native_string(
        b64encode(('%s:%s' % (username, password)).encode('latin1')).strip()
    )


def _bearer_auth_str(token):
    return 'Bearer ' + token


def _obtain_data_from_registry(login_server,
                               path,
                               resultIndex,
                               username,
                               password,
                               retry_times=3,
                               retry_interval=5):
    registryEndpoint = 'https://' + login_server
    resultList = []
    executeNextHttpCall = True

    if username is None:
        auth = _bearer_auth_str(password)
    else:
        auth = _basic_auth_str(username, password)

    headers = {'Authorization': auth}

    while executeNextHttpCall:
        executeNextHttpCall = False
        for i in range (0, retry_times):
            try:
                response = requests.get(
                    registryEndpoint + path,
                    headers=headers
                )

                errorMessage = None

                if response.status_code == 200:
                    resultList += response.json()[resultIndex]
                    if 'link' in response.headers and response.headers['link']:
                        linkHeader = response.headers['link']
                        # The registry is telling us there's more items in the list,
                        # and another call is needed. The link header looks something
                        # like `Link: </v2/_catalog?last=hello-world&n=1>; rel="next"`
                        # we should follow the next path indicated in the link header
                        path = linkHeader[(linkHeader.index('<') + 1):linkHeader.index('>')]
                        executeNextHttpCall = True
                    break
                elif response.status_code == 401:
                    raise CLIError(_UNAUTHORIZED)
                else:
                    errorMessage = response.text
                    raise CLIError(errorMessage)

            except Exception as e:  # pylint: disable=broad-except
                if str(e) is not _UNAUTHORIZED:
                    logger.debug('Retrying %s with exception %s', i + 1, str(e))
                    time.sleep(retry_interval)
                else:
                    raise

    if errorMessage is not None:
        raise CLIError(errorMessage)

    return resultList


def _validate_user_credentials(registry_name,
                               resource_group_name,
                               path,
                               resultIndex,
                               username=None,
                               password=None,
                               repository=None):
    login_server = get_registry_login_server_by_name(registry_name, resource_group_name)

    # 1. if username was specified, verify that password was also specified
    if username:
        if not password:
            try:
                password = prompt_pass(msg='Password: ')
            except NoTTYException:
                raise CLIError('Please specify both username and password in non-interactive mode.')
        return _obtain_data_from_registry(login_server, path, resultIndex, username, password)

    # 2. if we don't yet have credentials, attempt to get an access token
    try:
        access_token = get_login_access_token(login_server, repository)
        return _obtain_data_from_registry(login_server, path, resultIndex, None, access_token)
    except Exception as e:  # pylint: disable=broad-except
        logger.debug("acr_logger: " + str(e))

    # 3. if we still don't have credentials, attempt to get the admin credentials (if enabled)
    try:
        cred = acr_credential_show(registry_name)
        username = cred.username
        password = cred.passwords[0].value
        return _obtain_data_from_registry(login_server, path, resultIndex, username, password)
    except Exception as e:  # pylint: disable=broad-except
        logger.debug("acr_logger: " + str(e))

    # 4. if we still don't have credentials, prompt the user
    try:
        username = prompt('Username: ')
        password = prompt_pass(msg='Password: ')
    except NoTTYException:
        raise CLIError(
            'Unable to authenticate using AAD or admin login credentials. ' +
            'Please specify both username and password in non-interactive mode.')
    return _obtain_data_from_registry(login_server, path, resultIndex, username, password)


def acr_repository_list(registry_name,
                        resource_group_name=None,
                        username=None,
                        password=None):
    """Lists repositories in the specified container registry.
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    :param str username: The username used to log into the container registry
    :param str password: The password used to log into the container registry
    """
    path = '/v2/_catalog'
    return _validate_user_credentials(
        registry_name, resource_group_name, path, 'repositories', username, password)


def acr_repository_show_tags(registry_name,
                             repository,
                             resource_group_name=None,
                             username=None,
                             password=None):
    """Shows tags of a given repository in the specified container registry.
    :param str registry_name: The name of container registry
    :param str repository: The repository to obtain tags from
    :param str resource_group_name: The name of resource group
    :param str username: The username used to log into the container registry
    :param str password: The password used to log into the container registry
    """
    path = '/v2/' + repository + '/tags/list'
    return _validate_user_credentials(
        registry_name, resource_group_name, path, 'tags', username, password, repository)
