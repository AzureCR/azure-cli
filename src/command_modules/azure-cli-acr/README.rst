Microsoft Azure CLI 'acr' Command Module
==================================

This package has [not] been tested [much] with Python 2.7, 3.4 and 3.5.

Commands to manage Azure container registries
-------------
::

    Group
        az acr: Commands to manage Azure container registries.

    Commands:
        catalog: The catalog of repositories in the specified registry.
        create : Create a container registry.
        delete : Delete a container registry.
        list   : List container registries.
        show   : Get a container registry.
        tags   : The list of tags for a given repository in the specified registry.
        update : Update a container registry.

List container registries
-------------
::

    Command
        az acr list: List container registries.

    Arguments
        --resource-group -g: Name of resource group.

    Global Arguments
        --debug            : Increase logging verbosity to show all debug logs.
        --help -h          : Show this help message and exit.
        --output -o        : Output format.  Allowed values: json, jsonc, list, table, tsv.  Default:
                            json.
        --query            : JMESPath query string. See http://jmespath.org/ for more information and
                            examples.
        --verbose          : Increase logging verbosity. Use --debug for full debug logs.

    Examples
        List container registries and show result in a table
            az acr list -o table
        List container registries in a resource group and show result in a table
            az acr list -g <resource-group> -o table

Create a container registry
-------------
::

    Command
        az acr create: Create a container registry.

    Arguments
        --location -l       [Required]: Location.
        --name -n           [Required]: The primary resource name.
        --resource-group -g [Required]: Name of resource group.
        --storage-account-key -k      : Key of storage account.
        --storage-account-name -s     : Name of storage account.

    Global Arguments
        --debug                       : Increase logging verbosity to show all debug logs.
        --help -h                     : Show this help message and exit.
        --output -o                   : Output format.  Allowed values: json, jsonc, list, table, tsv.
                                        Default: json.
        --query                       : JMESPath query string. See http://jmespath.org/ for more
                                        information and examples.
        --verbose                     : Increase logging verbosity. Use --debug for full debug logs.

    Examples
        Create a container registry with managed storage account
            az acr create -n <registry-name> -g <resource-group> -l <location>
        Create a container registry with new/existing storage account in the current subscription
            az acr create -n <registry-name> -g <resource-group> -l <location> -s <storage-account-name>
        Create a container registry with your own storage account
            az acr create -n <registry-name> -g <resource-group> -l <location> -s <storage-account-name>
            -k <storage-account-key>

Delete a container registry
-------------
::

    Command
        az acr delete: Delete a container registry.

    Arguments
        --name -n [Required]: The primary resource name.

    Global Arguments
        --debug             : Increase logging verbosity to show all debug logs.
        --help -h           : Show this help message and exit.
        --output -o         : Output format.  Allowed values: json, jsonc, list, table, tsv.  Default:
                            json.
        --query             : JMESPath query string. See http://jmespath.org/ for more information and
                            examples.
        --verbose           : Increase logging verbosity. Use --debug for full debug logs.

    Examples
        Delete a container registry
            az acr delete -n <registry-name>

Get a container registry
-------------
::

    Command
        az acr show: Get a container registry.

    Arguments
        --name -n [Required]: The primary resource name.

    Global Arguments
        --debug             : Increase logging verbosity to show all debug logs.
        --help -h           : Show this help message and exit.
        --output -o         : Output format.  Allowed values: json, jsonc, list, table, tsv.  Default:
                            json.
        --query             : JMESPath query string. See http://jmespath.org/ for more information and
                            examples.
        --verbose           : Increase logging verbosity. Use --debug for full debug logs.

    Examples
        Get a container registry and show result in a table
            az acr show -n <registry-name> -o table

Update a container registry
-------------
::

    Command
        az acr update: Update a container registry.

    Arguments
        --name -n [Required]: The primary resource name.
        --tags              : Multiple semicolon separated tags in 'key[=value]' format.  Use "" to
                            clear existing tags.

    Global Arguments
        --debug             : Increase logging verbosity to show all debug logs.
        --help -h           : Show this help message and exit.
        --output -o         : Output format.  Allowed values: json, jsonc, list, table, tsv.  Default:
                            json.
        --query             : JMESPath query string. See http://jmespath.org/ for more information and
                            examples.
        --verbose           : Increase logging verbosity. Use --debug for full debug logs.

    Examples
        Update tags of a container registry and show result in a table
            az acr update -n <registry-name> --tags key1=value1;key2=value2 -o table

The catalog of repositories in the specified registry
-------------
::

    Command
        az acr catalog: The catalog of repositories in the specified registry.

    Arguments
        --name -n [Required]: The primary resource name.
        --password          : The password used to log into the container registry.
        --username          : The username used to log into the container registry.

    Global Arguments
        --debug             : Increase logging verbosity to show all debug logs.
        --help -h           : Show this help message and exit.
        --output -o         : Output format.  Allowed values: json, jsonc, list, table, tsv.  Default:
                            json.
        --query             : JMESPath query string. See http://jmespath.org/ for more information and
                            examples.
        --verbose           : Increase logging verbosity. Use --debug for full debug logs.

    Examples
        The catalog of repositories in a registry under the current subscription
            az acr catalog -n <registry-name>
        The catalog of repositories in any registry with credentials
            az acr catalog -n <registry-name> --username <username> --password <password>

The list of tags for a given repository in the specified registry
-------------
::

    Command
        az acr tags: The list of tags for a given repository in the specified registry.

    Arguments
        --name -n    [Required]: The primary resource name.
        --repository [Required]: The repository to obtain tags from.
        --password             : The password used to log into the container registry.
        --username             : The username used to log into the container registry.

    Global Arguments
        --debug                : Increase logging verbosity to show all debug logs.
        --help -h              : Show this help message and exit.
        --output -o            : Output format.  Allowed values: json, jsonc, list, table, tsv.
                                Default: json.
        --query                : JMESPath query string. See http://jmespath.org/ for more information
                                and examples.
        --verbose              : Increase logging verbosity. Use --debug for full debug logs.

    Examples
        The list of tags for a given repository in a registry under the current subscription
            az acr tags -n <registry-name> --repository <repository>
        The list of tags for a given repository in any registry with credentials
            az acr tags -n <registry-name> --repository <repository> --username <username> --password
            <password>

