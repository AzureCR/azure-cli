#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.commands import cli_command

from collections import OrderedDict

from azure.cli.command_modules.registry.mgmt_cr.models import (
    RegistryParameters
)

from ._cr_utils import (
    _get_mgmt_service_client,
    _get_registries,
    _get_registries_by_resource_group,
    _get_registry_by_name,
    _get_resource_group_by_registry
)

registry_simple_info = lambda result: _cr_format(result, details=False)
registry_details = lambda result: _cr_format(result, details=True)

def _cr_format(result, details):
    '''Returns the list of container registries each of which is an ordered dictionary 
    :param list/dict result: The container registry object(s)
    :param bool details: Whether or not printing container registry details
    '''
    registries = []
    obj_list = result if isinstance(result, list) else [result]

    for item in obj_list:
        registry = OrderedDict()
        if 'name' in item and item['name']:
            registry['NAME'] = item['name']

        resource_group = _get_resource_group_by_registry(item)
        if resource_group:
            registry['RESOURCE GROUP'] = resource_group

        if 'location' in item and item['location']:
            registry['LOCATION'] = item['location']

        if 'tags' in item and item['tags']:
            registry['TAGS'] = str(item['tags'])

        if details:
            if 'properties' in item and item['properties']:
                properties = item['properties']

                if 'loginServer' in properties and properties['loginServer']:
                    registry['LOGIN SERVER'] = properties['loginServer']

                if 'username' in properties and properties['username']:
                    registry['USERNAME'] = properties['username']
                    
                if 'key' in properties and properties['key']:
                    registry['PASSWORD'] = properties['key']

                if 'creationDate' in properties and properties['creationDate']:
                    registry['Creation Date'] = properties['creationDate']

                if 'storageAccount' in properties and properties['storageAccount']:
                    storage_account = properties['storageAccount']

                    if 'name' in storage_account and storage_account['name']:
                        registry['Storage Account Name'] = storage_account['name']

        registries.append(registry)
    return registries

def _cr_list_all():
    '''Returns the list of container registries in the current subscription.
    '''
    return _get_registries()

def _cr_list(resource_group):
    '''Returns the list of container registries in the resource group.
    :param str resource_group: The name of resource group
    '''
    return _get_registries_by_resource_group(resource_group)

def _cr_create(resource_group, registry_name, location):
    '''Returns the created container registry.
    :param str resource_group: The name of resource group
    :param str registry_name: The name of container registry
    :param str location: The name of location
    '''
    return _get_mgmt_service_client().create(resource_group, registry_name, RegistryParameters(location=location))

def _cr_delete(registry_name):
    '''Deletes the container registry that matches the registry name
    :param str registry_name: The name of container registry
    '''
    registry = _get_registry_by_name(registry_name)
    resource_group = _get_resource_group_by_registry(registry)
    return _get_mgmt_service_client().delete(resource_group, registry_name)

def _cr_show(registry_name):
    '''Returns the container registry that matches the registry name.
    :param str registry_name: The name of container registry
    '''
    return _get_registry_by_name(registry_name)

def _cr_update(registry_name, tags=None):
    '''Returns the updated container registry that matches the registry name.
    :param str registry_name: The name of container registry
    '''
    registry = _get_registry_by_name(registry_name)
    resource_group = _get_resource_group_by_registry(registry)

    newTags = registry.tags

    if isinstance(tags, dict):
        if tags:
            for key in tags:
                if tags[key]:
                    newTags[key]=tags[key]
                else:
                    del newTags[key]
        else:
            newTags = {}
            
    return _get_mgmt_service_client().update(resource_group, registry_name, RegistryParameters(location=registry.location, tags=newTags))

cli_command('registry list-all', _cr_list_all, simple_output_query=registry_simple_info)
cli_command('registry list', _cr_list, simple_output_query=registry_simple_info)
cli_command('registry create', _cr_create, simple_output_query=registry_details)
cli_command('registry delete', _cr_delete, simple_output_query=registry_details)
cli_command('registry show', _cr_show, simple_output_query=registry_details)
cli_command('registry update', _cr_update, simple_output_query=registry_details)
