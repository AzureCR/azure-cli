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

helps['acr update'] = """
            type: command
            examples:
                - name: Update tags of a container registry and show result in a table
                  text:
                    az acr update -n <registry-name> --tags key1=value1;key2=value2 -o table
            """

helps['acr repository list'] = """
            type: command
            examples:
                - name: List repositories in a given container registry under the current subscription
                  text:
                    az acr repository list --login-server <login-server>
                - name: List repositories in a given container registry with credentials
                  text:
                    az acr repository list --login-server <login-server> --username <username> --password <password>
            """

helps['acr repository show-tags'] = """
            type: command
            examples:
                - name: Show tags of a given repository in a given container registry under the current subscription
                  text:
                    az acr repository show-tags --login-server <login-server> --repository <repository>
                - name: Show tags of a given repository in a given container registry with credentials
                  text:
                    az acr repository show-tags --login-server <login-server> --repository <repository> --username <username> --password <password>
            """
