#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.help_files import helps

#pylint: disable=line-too-long

helps['registry list'] = """
            type: command
            short-summary: List container registries.
            """

helps['registry create'] = """
            type: command
            short-summary: Create a container registry.
            long-summary: Create a container registry. See examples.
            examples:
                - name: Create a container registry
                  text:
                    az registry create -n <registry-name> -g <resource-group> -l <location>
                - name: Create a container registry with new/existing storage account
                  text:
                    az registry create -n <registry-name> -g <resource-group> -l <location> -s <storage-account-name>
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
            long-summary: Update a container registry. See examples.
            examples:
                - name: Update tags of a container registry.
                  text:
                    az registry update -n <registry-name> --tags key1=value1;key2=value2
            """
