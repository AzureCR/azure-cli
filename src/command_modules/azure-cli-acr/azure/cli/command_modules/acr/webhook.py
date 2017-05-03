# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .azure.mgmt.containerregistry.models import (
    WebhookCreateParameters,
    WebhookUpdateParameters
)

from ._factory import get_acr_service_client
from ._utils import (
    get_resource_group_name_by_registry_name,
    get_registry_location_by_name
)


def acr_webhook_list(registry_name,
                     resource_group_name=None):
    """Lists all the webhooks for the specified container registry."
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    """
    resource_group_name = get_resource_group_name_by_registry_name(
        registry_name, resource_group_name)
    client = get_acr_service_client().webhooks

    return client.list(resource_group_name, registry_name)


def acr_webhook_create(webhook_name,  # pylint: disable=too-many-arguments
                       uri,
                       actions,
                       registry_name,
                       resource_group_name=None,
                       headers=None,
                       is_enabled='true',
                       scope=None,
                       tags=None):
    """Creates a webhook for a container registry.
    :param str webhook_name: The name of webhook
    :param str uri: The service URI for the webhook to post notifications
    :param str actions: The list of actions that trigger the webhook to post notifications
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    :param str headers: Custom headers that will be added to the webhook notifications
    :param str is_enabled: Indicates whether the webhook is enabled
    :param str scope: The scope of repositories where the event can be triggered
    """
    location, resource_group_name = get_registry_location_by_name(
        registry_name, resource_group_name)

    client = get_acr_service_client().webhooks

    return client.create(
        resource_group_name,
        registry_name,
        webhook_name,
        WebhookCreateParameters(
            location=location,
            service_uri=uri,
            actions=actions,
            custom_headers=headers,
            is_enabled=is_enabled == 'true',
            scope=scope,
            tags=tags
        )
    )


def acr_webhook_delete(webhook_name,
                       registry_name,
                       resource_group_name=None):
    """Deletes a webhook from a container registry.
    :param str webhook_name: The name of webhook
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    """
    resource_group_name = get_resource_group_name_by_registry_name(
        registry_name, resource_group_name)
    client = get_acr_service_client().webhooks

    return client.delete(resource_group_name, registry_name, webhook_name)


def acr_webhook_show(webhook_name,
                     registry_name,
                     resource_group_name=None):
    """Gets the properties of the specified webhook.
    :param str webhook_name: The name of webhook
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    """
    resource_group_name = get_resource_group_name_by_registry_name(
        registry_name, resource_group_name)
    client = get_acr_service_client().webhooks

    return client.get(resource_group_name, registry_name, webhook_name)


def acr_webhook_update_custom(instance,  # pylint: disable=too-many-arguments
                              uri=None,
                              actions=None,
                              headers=None,
                              is_enabled=None,
                              scope=None,
                              tags=None):
    if uri is not None:
        instance.service_uri = uri

    if actions is not None:
        instance.actions = actions

    if headers is not None:
        instance.custom_headers = headers

    if is_enabled is not None:
        instance.is_enabled = is_enabled == 'true'

    if scope is not None:
        instance.scope = scope

    if tags is not None:
        instance.tags = tags

    return instance


def acr_webhook_update_get(client,
                           webhook_name,
                           registry_name,
                           resource_group_name=None):
    resource_group_name = get_resource_group_name_by_registry_name(
        registry_name, resource_group_name)

    webhook = client.get(resource_group_name, registry_name, webhook_name)

    return WebhookUpdateParameters(
        tags=webhook.tags,
        is_enabled=webhook.is_enabled,
        scope=webhook.scope,
        actions=webhook.actions)


def acr_webhook_update_set(client,
                           webhook_name,
                           registry_name,
                           resource_group_name=None,
                           parameters=None):
    resource_group_name = get_resource_group_name_by_registry_name(
        registry_name, resource_group_name)

    return client.update(resource_group_name, registry_name, webhook_name, parameters)


def acr_webhook_get_config(webhook_name,
                           registry_name,
                           resource_group_name=None):
    """Gets the configuration of service URI and custom headers for the webhook.
    :param str webhook_name: The name of webhook
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    """
    resource_group_name = get_resource_group_name_by_registry_name(
        registry_name, resource_group_name)
    client = get_acr_service_client().webhooks

    return client.get_callback_config(resource_group_name, registry_name, webhook_name)


def acr_webhook_list_events(webhook_name,
                            registry_name,
                            resource_group_name=None):
    """Lists recent events for the specified webhook.
    :param str webhook_name: The name of webhook
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    """
    resource_group_name = get_resource_group_name_by_registry_name(
        registry_name, resource_group_name)
    client = get_acr_service_client().webhooks

    return client.list_events(resource_group_name, registry_name, webhook_name)


def acr_webhook_ping(webhook_name,
                     registry_name,
                     resource_group_name=None):
    """Triggers a ping event to be sent to the webhook.
    :param str webhook_name: The name of webhook
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    """
    resource_group_name = get_resource_group_name_by_registry_name(
        registry_name, resource_group_name)
    client = get_acr_service_client().webhooks

    return client.ping(resource_group_name, registry_name, webhook_name)
