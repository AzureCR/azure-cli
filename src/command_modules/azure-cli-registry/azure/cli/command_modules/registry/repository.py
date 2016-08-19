#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

import requests

from azure.cli.commands import cli_command

from ._utils import (
    get_registry_by_name,
    validate_registry_name
)

import azure.cli._logging as _logging
logger = _logging.get_az_logger(__name__)

def _obtain_data_from_registry(registry_name, path, resultIndex, username, password):
    registryEndpoint = 'https://' + registry_name + '.azurecr.io'
    resultList = []
    executeNextHttpCall = True

    while executeNextHttpCall:
        executeNextHttpCall = False
        response = requests.get(registryEndpoint + path,
            auth=requests.auth.HTTPBasicAuth(
               username,
               password
            )
        )

        if response.status_code == 200:
            resultList += response.json()[resultIndex]
            if 'link' in response.headers and response.headers['link']:
                linkHeader = response.headers['link']
                # the registry is telling us there's more items in the list, and another call is needed
                # the link header looks something like `Link: </v2/_catalog?last=hello-world&n=1>; rel="next"`
                # we should follow the next path indicated in the link header
                path = linkHeader[(linkHeader.index('<')+1):linkHeader.index('>')]
                executeNextHttpCall = True
        else:
            response.raise_for_status()

    return {resultIndex: resultList}

def _validate_user_credentials(registry_name, path, resultIndex, username=None, password=None):
    if username and password:
        return _obtain_data_from_registry(registry_name, path, resultIndex, username, password)

    try:
        registry = get_registry_by_name(registry_name)
        username = registry.properties.username
        password = registry.properties.key
        return _obtain_data_from_registry(registry_name, path, resultIndex, username, password)
    except: # pylint: disable=W0702
        logger.error('No container registry can be found with name: ' + registry_name)
        logger.error('Please switch subscription or enter username/password')
        raise SystemExit(1)

def cr_catalog(registry_name, username=None, password=None):
    '''Returns the catalog of repositories in the specified registry.
    :param str registry_name: The name of your Azure container registry
    :param str username: The username used to log into the container registry
    :param str password: The password used to log into the container registry
    '''
    validate_registry_name(registry_name)
    path = '/v2/_catalog'
    return _validate_user_credentials(registry_name, path, 'repositories', username, password)

def cr_tags(registry_name, repository, username=None, password=None):
    '''Returns the list of tags for a given repository in the specified registry.
    :param str registry_name: The name of your Azure container registry
    :param str repository: The repository to obtain tags from
    :param str username: The username used to log into the container registry
    :param str password: The password used to log into the container registry
    '''
    validate_registry_name(registry_name)
    path = '/v2/' + repository + '/tags/list'
    return _validate_user_credentials(registry_name, path, 'tags', username, password)

cli_command('registry catalog', cr_catalog)
cli_command('registry tags', cr_tags)
