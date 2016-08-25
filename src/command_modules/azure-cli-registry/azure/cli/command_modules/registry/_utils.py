#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.command_modules.registry.mgmt_cr.models import RegistryParameters

from ._factory import get_mgmt_service_client

def _get_registries_in_subscription():
    '''Returns the list of container registries in the current subscription.
    '''
    return get_mgmt_service_client().list().value # pylint: disable=E1101

def _get_registries_in_resource_group(resource_group):
    '''Returns the list of container registries in the resource group.
    :param str resource_group: The name of resource group
    '''
    return get_mgmt_service_client().list_by_resource_group(resource_group).value # pylint: disable=E1101

def get_registry_by_name(registry_name):
    '''Returns the container registry that matches the registry name.
    :param str registry_name: The name of container registry
    '''
    registries = _get_registries_in_subscription()
    elements = [item for item in registries if item.name.lower() == registry_name.lower()]

    if len(elements) == 0:
        return None
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

def get_subscription_id_by_registry(registry):
    '''Returns the subscription id of a container registry.
    :param RegistryParameters/dict registry: The container registry object
    '''
    resource_id = _get_resource_id(registry)
    resource_group_keyword = _get_resource_group_keyword(resource_id)
    return resource_id[resource_id.index('/subscriptions/') + len('/subscriptions/') : resource_id.index(resource_group_keyword)]

def get_resource_group_by_registry(registry):
    '''Returns the resource group of a container registry.
    :param RegistryParameters/dict registry: The container registry object
    '''
    resource_id = _get_resource_id(registry)
    resource_group_keyword = _get_resource_group_keyword(resource_id)
    return resource_id[resource_id.index(resource_group_keyword) + len(resource_group_keyword) : resource_id.index('/providers/')]

def _get_resource_group_keyword(resource_id):
    '''Returns the resource group keyword for parsing resource id.
    :param str resource_id: The resource id of a container registry
    '''
    if '/resourcegroups/' in resource_id:
        return '/resourcegroups/'
    elif '/resourceGroups/' in resource_id:
        return '/resourceGroups/'
    else:
        raise ValueError('Invalid resource id: ' + resource_id)
