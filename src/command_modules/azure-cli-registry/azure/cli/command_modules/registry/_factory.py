#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli._profile import Profile
from azure.cli.commands.client_factory import configure_common_settings

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
    '''Returns the client for managing resource.
    '''
    profile = Profile()
    cred, subscription_id, _ = profile.get_login_credentials()

    client = ResourceManagementClient(cred, subscription_id, base_url=get_env()[ENDPOINT_URLS.RESOURCE_MANAGER])

    configure_common_settings(client)

    return client

def get_mgmt_service_client():
    '''Returns the client for managing container registries.
    '''
    profile = Profile()
    cred, subscription_id, _ = profile.get_login_credentials()
    
    config = ContainerRegistryConfiguration(subscription_id, VERSION, cred, base_url=get_env()[ENDPOINT_URLS.RESOURCE_MANAGER])
    client = ContainerRegistry(config)

    configure_common_settings(client)

    return client.registries
