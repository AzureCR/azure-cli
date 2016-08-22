#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

CLIENT_ID = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'

ENV_DEFAULT = 'dogfood'

COMMON_TENANT = 'common'

#ported from https://github.com/Azure/azure-xplat-cli/blob/dev/lib/util/profile/environment.js
class ENDPOINT_URLS: #pylint: disable=too-few-public-methods,old-style-class,no-init
    MANAGEMENT = 'management'
    ACTIVE_DIRECTORY_AUTHORITY = 'active_directory_authority'
    ACTIVE_DIRECTORY_GRAPH_RESOURCE_ID = 'active_directory_graph_resource_id'
    RESOURCE_MANAGER = 'resource_manager'

_environments = {
    ENV_DEFAULT: {
        ENDPOINT_URLS.MANAGEMENT: 'https://management.core.windows.net/',
        ENDPOINT_URLS.ACTIVE_DIRECTORY_AUTHORITY : 'https://login.windows-ppe.net',
        ENDPOINT_URLS.ACTIVE_DIRECTORY_GRAPH_RESOURCE_ID: 'https://graph.ppe.windows.net/',
        ENDPOINT_URLS.RESOURCE_MANAGER: 'https://api-dogfood.resources.windows-int.net/',
        }
}

def get_env(env_name=None):
    if env_name is None:
        env_name = ENV_DEFAULT
    elif env_name not in _environments:
        raise ValueError
    return _environments[env_name]

def get_authority_url(tenant=None, env_name=None):
    env = get_env(env_name)
    return env[ENDPOINT_URLS.ACTIVE_DIRECTORY_AUTHORITY] + '/' + (tenant or COMMON_TENANT)
