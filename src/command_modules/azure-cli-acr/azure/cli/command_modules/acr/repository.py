#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

import requests

from azure.cli.core.commands import cli_command
from azure.cli.core._util import CLIError

from ._utils import get_registry_by_name

def _obtain_data_from_registry(login_server, path, resultIndex, username, password):
    registryEndpoint = 'https://' + login_server
    resultList = []
    executeNextHttpCall = True

    while executeNextHttpCall:
        executeNextHttpCall = False
        response = requests.get(
            registryEndpoint + path,
            auth=requests.auth.HTTPBasicAuth(
                username,
                password
            )
        )

        if response.status_code == 200:
            resultList += response.json()[resultIndex]
            if 'link' in response.headers and response.headers['link']:
                linkHeader = response.headers['link']
                # The registry is telling us there's more items in the list,
                # and another call is needed. The link header looks something
                # like `Link: </v2/_catalog?last=hello-world&n=1>; rel="next"`
                # we should follow the next path indicated in the link header
                path = linkHeader[(linkHeader.index('<')+1):linkHeader.index('>')]
                executeNextHttpCall = True
        else:
            response.raise_for_status()

    return {resultIndex: resultList}

def _validate_user_credentials(login_server, path, resultIndex, username=None, password=None):
    if username and password:
        return _obtain_data_from_registry(login_server, path, resultIndex, username, password)

    try:
        registry_name = login_server[0:login_server.index('.')]
        registry = get_registry_by_name(registry_name)
        username = registry.properties.username
        password = registry.properties.key
        return _obtain_data_from_registry(login_server, path, resultIndex, username, password)
    except: #pylint: disable=W0702
        raise CLIError('No container registry can be found with name: ' + registry_name +
                       '\nPlease switch subscription or enter username/password')

def acr_catalog(login_server, username=None, password=None):
    '''Returns the catalog of repositories in the specified registry.
    :param str login_server: The URL of registry login server
    :param str username: The username used to log into the container registry
    :param str password: The password used to log into the container registry
    '''
    path = '/v2/_catalog'
    return _validate_user_credentials(login_server, path, 'repositories', username, password)

def acr_tags(login_server, repository, username=None, password=None):
    '''Returns the list of tags for a given repository in the specified registry.
    :param str login_server: The URL of registry login server
    :param str repository: The repository to obtain tags from
    :param str username: The username used to log into the container registry
    :param str password: The password used to log into the container registry
    '''
    path = '/v2/' + repository + '/tags/list'
    return _validate_user_credentials(login_server, path, 'tags', username, password)

cli_command('acr catalog', acr_catalog)
cli_command('acr tags', acr_tags)
