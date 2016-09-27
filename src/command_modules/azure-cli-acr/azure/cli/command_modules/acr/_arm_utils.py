#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.core._util import CLIError
from azure.cli.core.commands.parameters import (
    get_resources_in_subscription,
    get_resources_in_resource_group
)

from azure.cli.command_modules.acr.mgmt_acr import VERSION
from azure.cli.command_modules.acr.mgmt_acr.models import Registry

from ._constants import (
    RESOURCE_PROVIDER,
    RESOURCE_TYPE
)
from ._factory import (
    get_arm_service_client,
    get_storage_service_client,
    get_tenant_id
)
from ._utils import get_resource_group_name_by_resource_id

def arm_get_registries_in_subscription():
    '''Returns the list of container registries in the current subscription.
    '''
    result = get_resources_in_subscription(RESOURCE_TYPE)
    return [Registry(item.id, item.name, item.location, item.tags) for item in result]

def arm_get_registries_in_resource_group(resource_group_name):
    '''Returns the list of container registries in the resource group.
    :param str resource_group_name: The name of resource group
    '''
    result = get_resources_in_resource_group(resource_group_name, RESOURCE_TYPE)
    return [Registry(item.id, item.name, item.location, item.tags) for item in result]

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
        raise CLIError(
            'More than one container registries are found with name: {}'.format(registry_name))

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

    parameters = _parameters(registry_name, location, storage_account_name)
    storage_account_resource_group, _ = _arm_get_storage_account(storage_account_name)

    if storage_account_resource_group:
        file_path = os.path.join(os.path.dirname(__file__), 'template.existing.json')
        parameters['storageAccountResourceGroup'] = {'value': storage_account_resource_group}
    else:
        file_path = os.path.join(os.path.dirname(__file__), 'template.new.json')
        parameters['storageAccountType'] = {'value': 'Standard_LRS'}

    template = get_file_json(file_path)
    properties = DeploymentProperties(template=template, parameters=parameters, mode='incremental')

    return _arm_deploy_template(resource_group_name, properties)

def _arm_deploy_template(resource_group_name, properties, index=0):
    '''Deploys ARM template to create a container registry.
    :param str resource_group_name: The name of resource group
    :param DeploymentProperties properties: The properties of a deployment
    :param int index: The index added to deployment name to avoid conflict
    '''
    if index == 0:
        deployment_name = RESOURCE_PROVIDER
    elif index > 9: # Just a number to avoid infinite loops
        raise CLIError(
            'The resource group {} has too many deployments'.format(resource_group_name))
    else:
        deployment_name = RESOURCE_PROVIDER + '_' + str(index)

    client = get_arm_service_client()

    try:
        client.deployments.validate(resource_group_name, deployment_name, properties)
        return client.deployments.create_or_update(resource_group_name, deployment_name, properties)
    except: #pylint: disable=W0702
        return _arm_deploy_template(resource_group_name, properties, index + 1)

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
        'storageAccountApiVersion': {'value': '2015-05-01-preview'},
        'tenantId': {'value': get_tenant_id()}
    }
    return parameters

def _arm_get_storage_account(storage_account_name):
    '''Returns the dict of tags in the storage account.
    :param str storage_account_name: The name of storage account
    '''
    result = get_resources_in_subscription('Microsoft.Storage/storageAccounts')
    elements = [item for item in result if item.name.lower() == storage_account_name.lower()]

    if len(elements) == 0:
        return None, None
    elif len(elements) == 1:
        storage_account_resource_group = get_resource_group_name_by_resource_id(elements[0].id)
        return storage_account_resource_group, elements[0].tags
    else:
        raise CLIError(
            'More than one storage accounts are found with name: {}'.format(storage_account_name))

def add_tag_storage_account(storage_account_name, key, value):
    '''Add a new tag (key, value) to the storage account.
    :param str storage_account_name: The name of storage account
    :param str key: The key of the new tag
    :param str value: The value of the new tag
    '''
    from azure.mgmt.storage.models import StorageAccountUpdateParameters
    storage_account_resource_group, tags = _arm_get_storage_account(storage_account_name)

    newKey = key
    index = 1
    while newKey in tags:
        newKey = key + '_' + str(index)
        index += 1
        if index > 99: # Just a number to avoid infinite loops
            raise CLIError(
                'The storage account {} has too many tags'.format(storage_account_name))

    tags[newKey] = value
    client = get_storage_service_client().storage_accounts

    return client.update(storage_account_resource_group,
                         storage_account_name,
                         StorageAccountUpdateParameters(tags=tags))

def delete_tag_storage_account(storage_account_name, registry_name):
    '''Delete a tag (key, value) from the storage account.
    :param str storage_account_name: The name of storage account
    :param str registry_name: The name of container registry
    '''
    from azure.mgmt.storage.models import StorageAccountUpdateParameters
    storage_account_resource_group, tags = _arm_get_storage_account(storage_account_name)

    for key, value in tags.items():
        if value == registry_name:
            del tags[key]

    client = get_storage_service_client().storage_accounts

    return client.update(storage_account_resource_group,
                         storage_account_name,
                         StorageAccountUpdateParameters(tags=tags))
