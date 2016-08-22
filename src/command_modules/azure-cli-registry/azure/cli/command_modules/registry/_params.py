#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.commands import register_cli_argument

from azure.cli.commands.parameters import (
    name_type,
    resource_group_name_type,
    location_type,
    tags_type
)

register_cli_argument('registry', 'registry_name', arg_type=name_type)
register_cli_argument('registry', 'resource_group', arg_type=resource_group_name_type)
register_cli_argument('registry', 'location', arg_type=location_type)
register_cli_argument('registry', 'tags', arg_type=tags_type)
