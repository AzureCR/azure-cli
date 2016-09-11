#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.core._profile import Profile
from azure.cli.core.commands.client_factory import (
    configure_common_settings,
    get_mgmt_service_client
)

from azure.cli.command_modules.acr.containerregistry import (
    ContainerRegistry,
    ContainerRegistryConfiguration,
    VERSION
)

from azure.mgmt.resource.resources import ResourceManagementClient
from azure.storage._constants import SERVICE_HOST_BASE

def get_arm_service_client():
    '''Returns the client for managing ARM resources.
    '''
    return get_mgmt_service_client(ResourceManagementClient)

def get_registry_service_client():
    '''Returns the client for managing container registries.
    '''
    profile = Profile()
    credentials, subscription_id, _ = profile.get_login_credentials()

    config = ContainerRegistryConfiguration(subscription_id, VERSION, credentials)
    client = ContainerRegistry(config)

    configure_common_settings(client)

    return client.registries

def get_storage_end_point_suffix():
    '''Returns storage account end point suffix.
    '''
    return SERVICE_HOST_BASE
