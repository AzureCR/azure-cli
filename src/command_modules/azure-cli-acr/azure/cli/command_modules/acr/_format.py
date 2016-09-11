#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from collections import OrderedDict

from ._constants import RESOURCE_TYPE
from ._utils import get_resource_group_name_by_registry

_basic_map = {
    'name': 'NAME',
    'resourceGroup': 'RESOURCE GROUP',
    'location': 'LOCATION',
    'tags': 'TAGS'
}

_properties_map = {
    'loginServer': 'LOGIN SERVER',
    'username': 'USERNAME',
    'key': 'PASSWORD',
    'creationDate': 'CREATION DATE',
}

_storage_account_map = {
    'name': 'STORAGE ACCOUNT NAME'
}

_parameters_map = {
    'registryName': 'NAME',
    'location': 'LOCATION',
    'storageAccountName': 'STORAGE ACCOUNT NAME'
}

_order_map = {
    'NAME': 1,
    'RESOURCE GROUP': 2,
    'LOCATION': 3,
    'TAGS': 4,
    'LOGIN SERVER': 11,
    'USERNAME': 12,
    'PASSWORD': 13,
    'CREATION DATE': 14,
    'STORAGE ACCOUNT NAME': 21
}

def output_format(result):
    '''Returns the list of container registries each of which is an ordered dictionary.
    :param list/dict result: The container registry object(s) or deployment result(s)
    '''
    obj_list = result if isinstance(result, list) else [result]
    return [_format(item) for item in obj_list]

def _format(item):
    '''Returns an ordered dictionary of the container registry or deployment result.
    :param dict item: The container registry object or deployment result
    '''
    if isinstance(item, dict) and \
       'id' in item and \
       '/providers/Microsoft.Resources/deployments/' in item['id']:
        return _format_deployment(item)
    elif isinstance(item, dict) and \
         'id' in item and \
         ('/providers/' + RESOURCE_TYPE + '/') in item['id']:
        return _format_registry(item)
    else:
        raise ValueError('Unknown item: ' + str(item))

def _format_deployment(item):
    '''Returns an ordered dictionary of the deployment result.
    :param dict item: The deployment result
    '''
    basic_info = {_basic_map[key]: str(item[key]) for key in item if key in _basic_map}

    parameters_info = {}
    if 'properties' in item and \
       item['properties'] and \
       'parameters' in item['properties'] and \
       item['properties']['parameters']:
        parameters = item['properties']['parameters']
        parameters_info = {_parameters_map[key]: str(parameters[key]['value'])
                           for key in parameters if key in _parameters_map}

    all_info = basic_info.copy()
    all_info.update(parameters_info)

    return OrderedDict(sorted(all_info.items(), key=lambda t: _order_map[t[0]]))

def _format_registry(item):
    '''Returns an ordered dictionary of the container registry.
    :param dict item: The container registry object
    '''
    basic_info = {_basic_map[key]: str(item[key]) for key in item if key in _basic_map}

    resource_group_name = get_resource_group_name_by_registry(item)
    if resource_group_name:
        basic_info['RESOURCE GROUP'] = resource_group_name

    properties_info = {}
    storage_account_info = {}
    if 'properties' in item and item['properties']:
        properties = item['properties']
        properties_info = {_properties_map[key]: str(properties[key])
                           for key in properties if key in _properties_map}

        if 'storageAccount' in properties and properties['storageAccount']:
            storage_account = properties['storageAccount']
            storage_account_info = {_storage_account_map[key]: str(storage_account[key])
                                    for key in storage_account if key in _storage_account_map}

    all_info = basic_info.copy()
    all_info.update(properties_info)
    all_info.update(storage_account_info)

    return OrderedDict(sorted(all_info.items(), key=lambda t: _order_map[t[0]]))
