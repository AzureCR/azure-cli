#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.command_modules.acr.mgmt_acr.models import RegistryParameters

from ._constants import RESOURCE_TYPE
from ._factory import get_arm_service_client

from azure.cli.command_modules.acr.mgmt_acr import VERSION

def arm_get_registries_in_subscription():
    '''Returns the list of container registries in the current subscription.
    '''
    client = get_arm_service_client()
    filter_str = "resourceType eq '{}'".format(RESOURCE_TYPE)
    result = list(client.resources.list(filter=filter_str))

    return [RegistryParameters(item.id, item.name, item.location, item.tags) for item in result]

def arm_get_registries_in_resource_group(resource_group_name):
    '''Returns the list of container registries in the resource group.
    :param str resource_group_name: The name of resource group
    '''
    client = get_arm_service_client()
    filter_str = "resourceType eq '{}'".format(RESOURCE_TYPE)
    result = list(client.resource_groups.list_resources(resource_group_name, filter=filter_str))

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

def arm_deploy_template(resource_group_name, registry_name, location, storage_account_name):
    '''Deploys ARM template to create a container registry.
    :param str resource_group_name: The name of resource group
    :param str registry_name: The name of container registry
    :param str location: The name of location
    :param str storage_account_name: The name of storage account
    '''
    from azure.mgmt.resource.resources.models import DeploymentProperties
    from azure.cli.core._util import get_file_json
    import os

    file_path = os.path.join(os.path.dirname(__file__), 'template.json')
    template = get_file_json(file_path)
    parameters = _parameters(registry_name, location, storage_account_name)
    properties = DeploymentProperties(template=template, parameters=parameters, mode='incremental')

    client = get_arm_service_client()
    deployment_name = 'Deployment.' + registry_name

    return client.deployments.create_or_update(resource_group_name, deployment_name, properties)

def _parameters(registry_name, location, storage_account_name):
    '''Returns a dict of deployment parameters.
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
