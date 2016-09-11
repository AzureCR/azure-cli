#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

from azure.cli.core.help_files import helps

#pylint: disable=line-too-long

helps['acr'] = """
            type: group
            short-summary: Commands to manage Azure container registries.
            """

helps['acr list'] = """
            type: command
            short-summary: List container registries.
            examples:
                - name: List container registries and show result in a table
                  text:
                    az acr list -o table
                - name: List container registries in a resource group and show result in a table
                  text:
                    az acr list -g <resource-group> -o table
            """

helps['acr create'] = """
            type: command
            short-summary: Create a container registry.
            examples:
                - name: Create a container registry with managed storage account
                  text:
                    az acr create -n <registry-name> -g <resource-group> -l <location>
                - name: Create a container registry with new/existing storage account in the current subscription
                  text:
                    az acr create -n <registry-name> -g <resource-group> -l <location> -s <storage-account-name>
                - name: Create a container registry with your own storage account in any subscription
                  text:
                    az acr create -n <registry-name> -g <resource-group> -l <location> -s <storage-account-name> -k <storage-account-key>
            """

helps['acr delete'] = """
            type: command
            short-summary: Delete a container registry.
            examples:
                - name: Delete a container registry
                  text:
                    az acr delete -n <registry-name>
            """

helps['acr show'] = """
            type: command
            short-summary: Get a container registry.
            examples:
                - name: Get a container registry and show result in a table
                  text:
                    az acr show -n <registry-name> -o table
            """

helps['acr update'] = """
            type: command
            short-summary: Update a container registry.
            examples:
                - name: Update tags of a container registry and show result in a table
                  text:
                    az acr update -n <registry-name> --tags key1=value1;key2=value2 -o table
            """

helps['acr catalog'] = """
            type: command
            short-summary: The catalog of repositories in the specified registry.
            examples:
                - name: The catalog of repositories in a registry under the current subscription
                  text:
                    az acr catalog -n <registry-name>
                - name: The catalog of repositories in any registry with credentials
                  text:
                    az acr catalog -n <registry-name> --username <username> --password <password>
            """

helps['acr tags'] = """
            type: command
            short-summary: The list of tags for a given repository in the specified registry.
            examples:
                - name: The list of tags for a given repository in a registry under the current subscription
                  text:
                    az acr tags -n <registry-name> --repository <repository>
                - name: The list of tags for a given repository in any registry with credentials
                  text:
                    az acr tags -n <registry-name> --repository <repository> --username <username> --password <password>
            """
