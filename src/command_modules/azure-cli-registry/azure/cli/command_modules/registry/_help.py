#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.help_files import helps

#pylint: disable=line-too-long

helps['registry'] = """
            type: group
            short-summary: Commands to manage Azure container registries.
            """

helps['registry list'] = """
            type: command
            short-summary: List container registries.
            examples:
                - name: List container registries and show result in a table
                  text:
                    az registry list -o table
                - name: List container registries in a resource group and show result in a table
                  text:
                    az registry list -g <resource-group> -o table
            """

helps['registry create'] = """
            type: command
            short-summary: Create a container registry.
            examples:
                - name: Create a container registry with managed storage account
                  text:
                    az registry create -n <registry-name> -g <resource-group> -l <location>
                - name: Create a container registry with dedicated storage account (new or existing)
                  text:
                    az registry create -n <registry-name> -g <resource-group> -l <location> --storage-account-name <storage-account-name>
                - name: Create a container registry with your own storage account
                  text:
                    az registry create -n <registry-name> -g <resource-group> -l <location> --storage-account-name <storage-account-name> --storage-account-key <storage-account-key>
            """

helps['registry delete'] = """
            type: command
            short-summary: Delete a container registry.
            examples:
                - name: Delete a container registry
                  text:
                    az registry delete -n <registry-name>
            """

helps['registry show'] = """
            type: command
            short-summary: Get a container registry.
            examples:
                - name: Get a container registry and show result in a table
                  text:
                    az registry show -n <registry-name> -o table
            """

helps['registry update'] = """
            type: command
            short-summary: Update a container registry.
            examples:
                - name: Update tags of a container registry and show result in a table
                  text:
                    az registry update -n <registry-name> --tags key1=value1;key2=value2 -o table
            """

helps['registry catalog'] = """
            type: command
            short-summary: The catalog of repositories in the specified registry.
            examples:
                - name: The catalog of repositories in a registry under the current subscription
                  text:
                    az registry catalog -n <registry-name>
                - name: The catalog of repositories in any registry with credentials
                  text:
                    az registry catalog -n <registry-name> --username <username> --password <password>
            """

helps['registry tags'] = """
            type: command
            short-summary: The list of tags for a given repository in the specified registry.
            examples:
                - name: The list of tags for a given repository in a registry under the current subscription
                  text:
                    az registry tags -n <registry-name> --repository <repository>
                - name: The list of tags for a given repository in any registry with credentials
                  text:
                    az registry tags -n <registry-name> --repository <repository> --username <username> --password <password>
            """
