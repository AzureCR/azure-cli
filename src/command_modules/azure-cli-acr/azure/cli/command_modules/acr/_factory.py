#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.core._profile import Profile
from azure.cli.core._config import az_config
from azure.mgmt.resource.resources import ResourceManagementClient

from azure.cli.core.commands.client_factory import (
    configure_common_settings,
    get_mgmt_service_client
)

from azure.cli.command_modules.acr.mgmt_acr import (
    ContainerRegistry,
    ContainerRegistryConfiguration,
    VERSION
)

import azure.cli.core._logging as _logging
logger = _logging.get_az_logger(__name__)

def get_arm_service_client():
    '''Returns the client for managing ARM resources.
    '''
    return get_mgmt_service_client(ResourceManagementClient)

def get_registry_service_client():
    '''Returns the client for managing container registries.
    '''
    profile = Profile()
    credentials, subscription_id, _ = profile.get_login_credentials()

    customized_api_version = az_config.get('acr', 'apiversion', None)
    if customized_api_version:
        logger.warning('Customized api-version is used: ' + customized_api_version)

    api_version = customized_api_version or VERSION

    config = ContainerRegistryConfiguration(subscription_id, api_version, credentials)
    client = ContainerRegistry(config)

    configure_common_settings(client)

    return client.registries
