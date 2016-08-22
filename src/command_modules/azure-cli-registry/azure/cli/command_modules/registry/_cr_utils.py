#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli._profile import Profile
from azure.cli.commands.client_factory import configure_common_settings

from azure.cli.command_modules.registry.mgmt_cr import (
    ContainerRegistry,
    ContainerRegistryConfiguration,
    VERSION
)

from azure.cli.command_modules.registry.mgmt_cr.models import (
    RegistryParameters
)

from azure.cli._azure_env import (
    get_env,
    ENDPOINT_URLS
)

def _get_mgmt_service_client():
    '''Returns the client for managing container registries.
    '''
    profile = Profile()
    cred, subscription_id, _ = profile.get_login_credentials()
    
    config = ContainerRegistryConfiguration(subscription_id, VERSION, cred, get_env()[ENDPOINT_URLS.RESOURCE_MANAGER])
    client = ContainerRegistry(config)

    configure_common_settings(client)

    return client.registries

def _get_registries():
    '''Returns the list of container registries in the current subscription.
    '''
    return _get_mgmt_service_client().list().value # pylint: disable=E1101

def _get_registries_by_resource_group(resource_group):
    '''Returns the list of container registries in the resource group.
    :param str resource_group: The name of resource group
    '''
    return _get_mgmt_service_client().list_by_resource_group(resource_group).value # pylint: disable=E1101

def _get_registry_by_name(registry_name):
    '''Returns the container registry that matches the registry name.
    :param str registry_name: The name of container registry
    '''
    registries = _get_registries()
    elements = [r for r in registries if r.name == registry_name]

    if len(elements) == 0:
        raise ValueError('No container registry can be found with name: ' + registry_name)
    elif len(elements) == 1:
        return elements[0]
    else:
        raise ValueError('More than one container registries are found with name: ' + registry_name)

def _get_resource_id (registry):
    '''Returns the resource id of a container registry.
    :param RegistryParameters/dict registry: The container registry object
    '''
    if isinstance(registry, RegistryParameters):
        return registry.id
    elif isinstance(registry, dict):
        return registry['id']
    else:
        raise ValueError('Unknown registry: ' + str(registry))

def _get_subscription_id_by_registry(registry):
    '''Returns the subscription id of a container registry.
    :param RegistryParameters/dict registry: The container registry object
    '''
    resource_id = _get_resource_id(registry)
    return resource_id[resource_id.index('/subscriptions/') + len('/subscriptions/') : resource_id.index('/resourcegroups/')]

def _get_resource_group_by_registry(registry):
    '''Returns the resource group of a container registry.
    :param RegistryParameters/dict registry: The container registry object
    '''
    resource_id = _get_resource_id(registry)
    return resource_id[resource_id.index('/resourcegroups/') + len('/resourcegroups/') : resource_id.index('/providers/')]
