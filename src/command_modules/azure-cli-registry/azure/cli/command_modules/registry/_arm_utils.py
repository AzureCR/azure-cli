#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.command_modules.registry.mgmt_cr.models import RegistryParameters

from ._factory import (
    get_arm_service_client,
    get_storage_end_point_url
)

from azure.cli.command_modules.registry.mgmt_cr import VERSION

resource_type = 'Microsoft.Krater/registries'

def arm_get_registries_in_subscription():
    '''Returns the list of container registries in the current subscription.
    '''
    client = get_arm_service_client()
    filter_str = "resourceType eq '{}'".format(resource_type)
    result = list(client.resources.list(filter=filter_str))
    
    return [RegistryParameters(item.id, item.name, item.location, item.tags) for item in result]

def arm_get_registries_in_resource_group(resource_group):
    '''Returns the list of container registries in the resource group.
    :param str resource_group: The name of resource group
    '''
    client = get_arm_service_client()
    filter_str = "resourceType eq '{}'".format(resource_type)
    result = list(client.resource_groups.list_resources(resource_group, filter=filter_str))

    return [RegistryParameters(item.id, item.name, item.location, item.tags) for item in result]

def arm_get_registry_by_name(registry_name):
    '''Returns the container registry that matches the registry name.
    :param str registry_name: The name of container registry
    '''
    registries = arm_get_registries_in_subscription()
    elements = [item for item in registries if item.name.lower() == registry_name.lower()]

    if len(elements) == 0:
        return None
    elif len(elements) == 1:
        return elements[0]
    else:
        raise ValueError('More than one container registries are found with name: ' + registry_name)

def arm_deploy_template_dedicated(resource_group, registry_name, location, 
                storage_account_name, deployment_name):
    '''Deploys ARM template to create a container registry using the storage account in the current subscription.
    :param str resource_group: The name of resource group
    :param str registry_name: The name of container registry
    :param str location: The name of location
    :param str storage_account_name: The name of storage account
    :param str deployment_name: The name of deployment
    '''
    parameters = _parameters_dedicated(registry_name, location, storage_account_name)
    return _arm_deploy_template(resource_group, deployment_name, 'template.dedicated.json', parameters)

def arm_deploy_template_byos(resource_group, registry_name, location, 
                storage_account_name, storage_account_key, deployment_name):
    '''Deploys ARM template to create a container registry using the user's own storage account.
    :param str resource_group: The name of resource group
    :param str registry_name: The name of container registry
    :param str location: The name of location
    :param str storage_account_name: The name of storage account
    :param str storage_account_key: The key of storage account
    :param str deployment_name: The name of deployment
    '''
    parameters = _parameters_byos(registry_name, location, storage_account_name, storage_account_key)
    return _arm_deploy_template(resource_group, deployment_name, 'template.byos.json', parameters)

def _arm_deploy_template(resource_group, deployment_name, template_path, parameters, mode='incremental'):
    '''Deploys ARM template to create a container registry.
    :param str resource_group: The name of resource group
    :param str deployment_name: The name of deployment
    :param str template_path: The template file path
    :param dict parameters: The parameters for this deployment
    :param str mode: The mode of deployment
    '''
    from azure.mgmt.resource.resources.models import DeploymentProperties
    from azure.cli._util import get_file_json
    import os

    file_path = os.path.join(os.path.dirname(__file__), template_path)
    template = get_file_json(file_path)
    properties = DeploymentProperties(template=template, parameters=parameters, mode=mode)
    
    client = get_arm_service_client()
    
    return client.deployments.create_or_update(resource_group, deployment_name, properties)

def _parameters_dedicated(registry_name, location, storage_account_name):
    '''Returns a dict of deployment parameters
    :param str registry_name: The name of container registry
    :param str location: The name of location
    :param str storage_account_name: The name of storage account
    '''
    parameters = {
        'registryName': {'value': registry_name},
        'registryLocation': {'value': location},
        'registryApiVersion': {'value': VERSION},
        'storageAccountName': {'value': storage_account_name},
        'storageAccountLocation': {'value': 'westus'},
        'storageAccountApiVersion': {'value': '2015-05-01-preview'}
    }
    return parameters

def _parameters_byos(registry_name, location, storage_account_name, storage_account_key):
    '''Returns a dict of deployment parameters
    :param str registry_name: The name of container registry
    :param str location: The name of location
    :param str storage_account_name: The name of storage account
    :param str storage_account_key: The key of storage account
    '''
    parameters = {
        'registryName': {'value': registry_name},
        'registryLocation': {'value': location},
        'registryApiVersion': {'value': VERSION},
        'storageAccountName': {'value': storage_account_name},
        'storageAccountKey': {'value': storage_account_key},
        'storageEndPointUrl': {'value': get_storage_end_point_url(storage_account_name)}
    }
    return parameters
