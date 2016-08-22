#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.help_files import helps

#pylint: disable=line-too-long

helps['registry list-all'] = """
            type: command
            short-summary: Get all container registries in the current subscription.
            """

helps['registry list'] = """
            type: command
            short-summary: Get all container registries in a resource group.
            """

helps['registry create'] = """
            type: command
            short-summary: Create a container registry.
            long-summary: Create a container registry. See examples.
            examples:
                - name: Create a container registry
                  text:
                    az registry create -n <registry-name> -g <resource-group> -l <location>
            """

helps['registry delete'] = """
            type: command
            short-summary: Delete a container registry.
            """

helps['registry show'] = """
            type: command
            short-summary: Get a container registry.
            """

helps['registry update'] = """
            type: command
            short-summary: Update a container registry.
            """
