#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli._profile import Profile
from azure.cli.commands.client_factory import (
    configure_common_settings,
    get_mgmt_service_client
)

from azure.cli._azure_env import (
    get_env,
    ENDPOINT_URLS
)

from azure.cli.command_modules.registry.mgmt_cr import (
    ContainerRegistry,
    ContainerRegistryConfiguration,
    VERSION
)

from azure.mgmt.resource.resources import ResourceManagementClient

def get_arm_service_client():
    '''Returns the client for managing ARM resources.
    '''
    return get_mgmt_service_client(ResourceManagementClient)

def get_registry_service_client():
    '''Returns the client for managing container registries.
    '''
    profile = Profile()
    cred, subscription_id, _ = profile.get_login_credentials()
    
    config = ContainerRegistryConfiguration(subscription_id, VERSION, cred, base_url=get_env()[ENDPOINT_URLS.RESOURCE_MANAGER])
    client = ContainerRegistry(config)

    configure_common_settings(client)

    return client.registries

def get_storage_end_point_url(storage_account_name):
    '''Returns the end point url for the storage account name
    :param str storage_account_name: The name of storage account
    '''
    return 'https://' + storage_account_name + '.' + get_env()[ENDPOINT_URLS.STORAGE_END_POINT_SUFFIX]
