#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.commands import cli_command

from azure.cli.command_modules.registry.mgmt_cr.models import RegistryParameters

from ._factory import get_mgmt_service_client

from ._arm_utils import (
    arm_get_registries_in_subscription,
    arm_get_registries_in_resource_group,
    arm_get_registry_by_name,
    arm_deploy_template
)

from ._utils import (
    get_registry_by_name,
    get_resource_group_by_registry
)

from ._format import output_format

import azure.cli._logging as _logging
logger = _logging.get_az_logger(__name__)

def cr_list(resource_group=None):
    '''Returns the list of container registries.
    :param str resource_group: The name of resource group
    '''
    if resource_group:
        return arm_get_registries_in_resource_group(resource_group)
    else:
        return arm_get_registries_in_subscription()

def cr_create(resource_group, registry_name, location, storage_account_name=None, deployment_name="Microsoft.Krater"):
    '''Returns the created container registry.
    :param str resource_group: The name of resource group
    :param str registry_name: The name of container registry
    :param str location: The name of location
    :param str storage_account_name: The name of storage account
    :param str deployment_name: The name of deployment  
    '''
    if storage_account_name:
        return arm_deploy_template(resource_group, registry_name, location, storage_account_name, deployment_name)
    else:
        return get_mgmt_service_client().create(resource_group, registry_name, RegistryParameters(location=location))

def cr_delete(registry_name):
    '''Deletes the container registry that matches the registry name
    :param str registry_name: The name of container registry
    '''
    registry = arm_get_registry_by_name(registry_name)
    if registry is None:
        logger.error('No container registry can be found with name: ' + registry_name)
        raise SystemExit(1)

    resource_group = get_resource_group_by_registry(registry)
    return get_mgmt_service_client().delete(resource_group, registry_name)

def cr_show(registry_name):
    '''Returns the container registry that matches the registry name.
    :param str registry_name: The name of container registry
    '''
    registry = arm_get_registry_by_name(registry_name)
    if registry is None:
        logger.error('No container registry can be found with name: ' + registry_name)
        raise SystemExit(1)

    resource_group = get_resource_group_by_registry(registry)
    return get_mgmt_service_client().get_properties(resource_group, registry_name)

def cr_update(registry_name, tags=None):
    '''Returns the updated container registry that matches the registry name.
    :param str registry_name: The name of container registry
    '''
    registry = get_registry_by_name(registry_name)
    if registry is None:
        logger.error('No container registry can be found with name: ' + registry_name)
        raise SystemExit(1)
        
    resource_group = get_resource_group_by_registry(registry)

    newTags = registry.tags

    if isinstance(tags, dict):
        if tags:
            for key in tags:
                if tags[key]:
                    newTags[key]=tags[key]
                elif key in newTags:
                    del newTags[key]
        else:
            newTags = {}
            
    return get_mgmt_service_client().update(resource_group, registry_name, RegistryParameters(location=registry.location, tags=newTags))

cli_command('registry list', cr_list, simple_output_query=output_format)
cli_command('registry create', cr_create, simple_output_query=output_format)
cli_command('registry delete', cr_delete, simple_output_query=output_format)
cli_command('registry show', cr_show, simple_output_query=output_format)
cli_command('registry update', cr_update, simple_output_query=output_format)
