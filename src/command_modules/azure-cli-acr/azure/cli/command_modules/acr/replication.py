# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.mgmt.containerregistry.v2017_06_01_preview.models import Replication

from ._constants import REPLICATION_API_VERSION
from ._factory import get_acr_service_client
from ._utils import (
    get_resource_group_name_by_registry_name,
    managed_registry_validation
)


REPLICATIONS_NOT_SUPPORTED = 'Replications are not supported for registries in Basic SKU.'


def acr_replication_list(registry_name, resource_group_name=None):
    """Lists all the replications for the specified container registry.
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    """
    _, resource_group_name = managed_registry_validation(
        registry_name, resource_group_name, REPLICATIONS_NOT_SUPPORTED)
    client = get_acr_service_client(REPLICATION_API_VERSION).replications

    return client.list(resource_group_name, registry_name)


def acr_replication_create(location,
                           registry_name,
                           resource_group_name=None,
                           replication_name=None,
                           tags=None):
    """Creates a replication for a container registry.
    :param str location: The name of location
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    :param str replication_name: The name of replication
    """
    _, resource_group_name = managed_registry_validation(
        registry_name, resource_group_name, REPLICATIONS_NOT_SUPPORTED)

    if replication_name is None:
        replication_name = "".join(location.split()).lower()

    client = get_acr_service_client(REPLICATION_API_VERSION).replications

    return client.create_or_update(
        resource_group_name=resource_group_name,
        registry_name=registry_name,
        replication_name=replication_name,
        location=location,
        tags=tags
    )


def acr_replication_delete(replication_name,
                           registry_name,
                           resource_group_name=None):
    """Deletes a replication from a container registry.
    :param str registry_name: The name of container registry
    """
    _, resource_group_name = managed_registry_validation(
        registry_name, resource_group_name, REPLICATIONS_NOT_SUPPORTED)
    client = get_acr_service_client(REPLICATION_API_VERSION).replications

    return client.delete(resource_group_name, registry_name, replication_name)


def acr_replication_show(replication_name,
                         registry_name,
                         resource_group_name=None):
    """Gets the properties of the specified replication.
    :param str replication_name: The name of replication
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    """
    _, resource_group_name = managed_registry_validation(
        registry_name, resource_group_name, REPLICATIONS_NOT_SUPPORTED)
    client = get_acr_service_client(REPLICATION_API_VERSION).replications

    return client.get(resource_group_name, registry_name, replication_name)


def acr_replication_update_custom(instance, tags=None):
    if tags is not None:
        instance.tags = tags

    return instance


def acr_replication_update_get(client,
                               replication_name,
                               registry_name,
                               resource_group_name=None):
    """Gets the properties of the specified replication.
    :param str replication_name: The name of replication
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    """
    _, resource_group_name = managed_registry_validation(
        registry_name, resource_group_name, REPLICATIONS_NOT_SUPPORTED)

    replication = client.get(resource_group_name, registry_name, replication_name)

    return Replication(
        location=replication.location,
        tags=replication.tags
    )


def acr_replication_update_set(client,
                               replication_name,
                               registry_name,
                               resource_group_name=None,
                               parameters=None):
    """Sets the properties of the specified replication.
    :param str replication_name: The name of replication
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    :param Replication parameters: The replication object
    """
    resource_group_name = get_resource_group_name_by_registry_name(
        registry_name, resource_group_name)

    return client.create_or_update(
        resource_group_name=resource_group_name,
        registry_name=registry_name,
        replication_name=replication_name,
        location=parameters.location,
        tags=parameters.tags)
