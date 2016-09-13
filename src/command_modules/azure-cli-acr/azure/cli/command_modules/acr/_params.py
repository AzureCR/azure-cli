#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.core.commands import (
    register_cli_argument,
    CliArgumentType
)

from azure.cli.core.commands.parameters import (
    resource_group_name_type,
    location_type,
    tags_type
)

from ._validators import validate_registry_name

registry_name_type = CliArgumentType(
    options_list=('--name', '-n'),
    help='Name of container registry',
    validator=validate_registry_name
)

storage_account_name_type = CliArgumentType(
    options_list=('--storage-account-name', '-s'),
    help='Name of storage account.'
)

storage_account_key_type = CliArgumentType(
    options_list=('--storage-account-key', '-k'),
    help='Key of storage account.'
)

register_cli_argument('acr', 'registry_name', arg_type=registry_name_type)
register_cli_argument('acr', 'resource_group', arg_type=resource_group_name_type)
register_cli_argument('acr', 'location', arg_type=location_type)
register_cli_argument('acr', 'tags', arg_type=tags_type)
register_cli_argument('acr', 'storage_account_name', arg_type=storage_account_name_type)
register_cli_argument('acr', 'storage_account_key', arg_type=storage_account_key_type)
