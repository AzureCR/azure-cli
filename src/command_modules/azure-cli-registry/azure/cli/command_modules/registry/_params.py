#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.commands import (
    register_cli_argument,
    CliArgumentType
)

from azure.cli.commands.parameters import (
    name_type,
    resource_group_name_type,
    location_type,
    tags_type
)

storage_account_name_type = CliArgumentType(
    help='Name of storage account.'
)

storage_account_key_type = CliArgumentType(
    help='Key of storage account.'
)

register_cli_argument('registry', 'registry_name', arg_type=name_type)
register_cli_argument('registry', 'resource_group', arg_type=resource_group_name_type)
register_cli_argument('registry', 'location', arg_type=location_type)
register_cli_argument('registry', 'tags', arg_type=tags_type)
register_cli_argument('registry', 'storage_account_name', arg_type=storage_account_name_type)
register_cli_argument('registry', 'storage_account_key', arg_type=storage_account_key_type)
