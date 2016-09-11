#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.core.commands import cli_command

from azure.cli.command_modules.acr.containerregistry.models import (
    RegistryParameters,
    RegistryProperties,
    StorageAccountProperties
)

from ._factory import (
    get_registry_service_client,
    get_storage_end_point_suffix
)

from ._arm_utils import (
    arm_get_registries_in_subscription,
    arm_get_registries_in_resource_group,
    arm_get_registry_by_name,
    arm_deploy_template
)

from ._utils import (
    get_registry_by_name,
    get_resource_group_by_registry,
    validate_registry_name
)

from ._format import output_format

import azure.cli.core._logging as _logging
logger = _logging.get_az_logger(__name__)

def acr_list(resource_group=None):
    '''Returns the list of container registries.
    :param str resource_group: The name of resource group
    '''
    if resource_group:
        return arm_get_registries_in_resource_group(resource_group)
    else:
        return arm_get_registries_in_subscription()

def acr_create(resource_group, registry_name, location, storage_account_name=None, storage_account_key=None, deployment_name="Microsoft.ContainerRegistry"):
    '''Returns the created container registry.
    :param str resource_group: The name of resource group
    :param str registry_name: The name of container registry
    :param str location: The name of location
    :param str storage_account_name: The name of storage account
    :param str storage_account_key: The key of storage account
    :param str deployment_name: The name of deployment
    '''
    validate_registry_name(registry_name)
    if storage_account_name:
        if storage_account_key:
            storage_account_properties = StorageAccountProperties(name=storage_account_name, access_key=storage_account_key, endpoint_suffix=get_storage_end_point_suffix())
            registry_properties = RegistryProperties(storage_account=storage_account_properties)
            registry_parameters = RegistryParameters(location=location, properties=registry_properties)
            return get_registry_service_client().create(resource_group, registry_name, registry_parameters)
        else:
            return arm_deploy_template(resource_group, registry_name, location, storage_account_name, deployment_name)
    else:
        return get_registry_service_client().create(resource_group, registry_name, RegistryParameters(location=location))

def acr_delete(registry_name):
    '''Deletes the container registry that matches the registry name
    :param str registry_name: The name of container registry
    '''
    validate_registry_name(registry_name)
    registry = arm_get_registry_by_name(registry_name)
    if registry is None:
        logger.error('No container registry can be found with name: ' + registry_name)
        raise SystemExit(1)

    resource_group = get_resource_group_by_registry(registry)
    return get_registry_service_client().delete(resource_group, registry_name)

def acr_show(registry_name):
    '''Returns the container registry that matches the registry name.
    :param str registry_name: The name of container registry
    '''
    validate_registry_name(registry_name)
    registry = arm_get_registry_by_name(registry_name)
    if registry is None:
        logger.error('No container registry can be found with name: ' + registry_name)
        raise SystemExit(1)

    resource_group = get_resource_group_by_registry(registry)
    return get_registry_service_client().get_properties(resource_group, registry_name)

def acr_update(registry_name, tags=None):
    '''Returns the updated container registry that matches the registry name.
    :param str registry_name: The name of container registry
    '''
    validate_registry_name(registry_name)
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
            
    return get_registry_service_client().update(resource_group, registry_name, RegistryParameters(location=registry.location, tags=newTags))

cli_command('acr list', acr_list, table_transformer=output_format)
cli_command('acr create', acr_create, table_transformer=output_format)
cli_command('acr delete', acr_delete, table_transformer=output_format)
cli_command('acr show', acr_show, table_transformer=output_format)
cli_command('acr update', acr_update, table_transformer=output_format)
