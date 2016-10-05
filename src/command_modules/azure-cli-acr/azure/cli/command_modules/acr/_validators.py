#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

import re
import uuid

from azure.mgmt.resource.resources.models.resource_group import ResourceGroup

from azure.cli.core._util import CLIError
from azure.cli.command_modules.storage._factory import storage_client_factory

from ._constants import ALLOWED_ROLES
from ._factory import get_arm_service_client

def validate_registry_name(namespace):
    if namespace.registry_name:
        registry_name = namespace.registry_name
        if len(registry_name) < 5 or len(registry_name) > 60:
            raise CLIError('The registry name must be between 5 and 60 characters.')

        p = re.compile('^([A-Za-z0-9]+)$')

        if not p.match(registry_name):
            raise CLIError('The registry name can contain only letters and numbers.')

def validate_storage_account_name(namespace):
    client = storage_client_factory().storage_accounts

    if namespace.storage_account_name is None:
        while True:
            storage_account_name = str(uuid.uuid4()).replace('-', '')[:24]
            if client.check_name_availability(storage_account_name).name_available is True: #pylint: disable=E1101
                namespace.storage_account_name = storage_account_name
                break

def validate_resource_group_name(namespace):
    client = get_arm_service_client()

    if namespace.resource_group_name:
        if not client.resource_groups.check_existence(namespace.resource_group_name):
            parameters = ResourceGroup(location=namespace.location)
            client.resource_groups.create_or_update(namespace.resource_group_name, parameters)

def validate_password(namespace):
    if namespace.password and not namespace.new_sp:
        raise CLIError('--password has to be used with a new service principal')

def validate_role(namespace):
    if namespace.role and not namespace.role.lower() in ALLOWED_ROLES:
        raise CLIError('The role {} is not allowed. Allowed roles {}'.format(
            namespace.role, str(ALLOWED_ROLES)))
