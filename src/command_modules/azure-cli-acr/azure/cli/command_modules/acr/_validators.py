# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.util import CLIError

from ._factory import get_acr_service_client
from ._utils import get_registry_location_by_name

import azure.cli.core.azlogging as azlogging

logger = azlogging.get_az_logger(__name__)


def validate_registry_name(namespace):
    if namespace.registry_name:
        client = get_acr_service_client().registries
        registry_name = namespace.registry_name

        result = client.check_name_availability(registry_name)

        if not result.name_available:  # pylint: disable=no-member
            raise CLIError(result.message)  # pylint: disable=no-member

def validate_headers(namespace):
    ''' Extracts multiple space-separated headers in key[=value] format '''
    if isinstance(namespace.headers, list):
        headers_dict = {}
        for item in namespace.headers:
            headers_dict.update(validate_header(item))
        namespace.headers = headers_dict

def validate_header(string):
    ''' Extracts a single header in key[=value] format '''
    result = {}
    if string:
        comps = string.split('=', 1)
        result = {comps[0]: comps[1]} if len(comps) > 1 else {string: ''}
    return result

def validate_replication_location(namespace):
    if namespace.location:
        registry_location, _ = get_registry_location_by_name(
            namespace.registry_name, namespace.resource_group_name)
        if namespace.location == "".join(registry_location.split()).lower():
            raise CLIError(
                "Replication should not be in the same location '{}' as the registry."
                .format(namespace.location))
        # Possibly check if a replication already exists in this location
