# Microsoft Azure CLI 'registry' Command Module

## Commands to manage Azure container registries
```
Group
    az registry: Commands to manage Azure container registries.

Commands:
    catalog: The catalog of repositories in the specified registry.
    create : Create a container registry.
    delete : Delete a container registry.
    list   : List container registries.
    show   : Get a container registry.
    tags   : The list of tags for a given repository in the specified registry.
    update : Update a container registry.
```

## List container registries
```
Command
    az registry list: List container registries.

Arguments
    --resource-group -g: Name of resource group.

Global Arguments
    --debug            : Increase logging verbosity to show all debug logs.
    --help -h          : Show this help message and exit.
    --output -o        : Output format.  Allowed values: json, tsv, list, table, jsonc.  Default:
                         json.
    --query            : JMESPath query string. See http://jmespath.org/ for more information and
                         examples.
    --verbose          : Increase logging verbosity. Use --debug for full debug logs.

Examples
    List container registries and show result in a table
        az registry list -o table
    List container registries in a resource group and show result in a table
        az registry list -g <resource-group> -o table
```

## Create a container registry
```
Command
    az registry create: Create a container registry.

Arguments
    --location -l       [Required]: Location.
    --name -n           [Required]: The primary resource name.
    --resource-group -g [Required]: Name of resource group.
    --storage-account-key         : Key of storage account.
    --storage-account-name        : Name of storage account.

Global Arguments
    --debug                       : Increase logging verbosity to show all debug logs.
    --help -h                     : Show this help message and exit.
    --output -o                   : Output format.  Allowed values: json, tsv, list, table, jsonc.
                                    Default: json.
    --query                       : JMESPath query string. See http://jmespath.org/ for more
                                    information and examples.
    --verbose                     : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Create a container registry with managed storage account
        az registry create -n <registry-name> -g <resource-group> -l <location>
    Create a container registry with dedicated storage account (new or existing)
        az registry create -n <registry-name> -g <resource-group> -l <location> --storage-account-
        name <storage-account-name>
    Create a container registry with your own storage account
        az registry create -n <registry-name> -g <resource-group> -l <location> --storage-account-
        name <storage-account-name> --storage-account-key <storage-account-key>
```

## Delete a container registry
```
Command
    az registry delete: Delete a container registry.

Arguments
    --name -n [Required]: The primary resource name.

Global Arguments
    --debug             : Increase logging verbosity to show all debug logs.
    --help -h           : Show this help message and exit.
    --output -o         : Output format.  Allowed values: json, tsv, list, table, jsonc.  Default:
                          json.
    --query             : JMESPath query string. See http://jmespath.org/ for more information and
                          examples.
    --verbose           : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Delete a container registry
        az registry delete -n <registry-name>
```

## Get a container registry
```
Command
    az registry show: Get a container registry.

Arguments
    --name -n [Required]: The primary resource name.

Global Arguments
    --debug             : Increase logging verbosity to show all debug logs.
    --help -h           : Show this help message and exit.
    --output -o         : Output format.  Allowed values: json, tsv, list, table, jsonc.  Default:
                          json.
    --query             : JMESPath query string. See http://jmespath.org/ for more information and
                          examples.
    --verbose           : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Get a container registry and show result in a table
        az registry show -n <registry-name> -o table
```

## Update a container registry
```
Command
    az registry update: Update a container registry.

Arguments
    --name -n [Required]: The primary resource name.
    --tags              : Multiple semicolon separated tags in 'key[=value]' format.  Use "" to
                          clear existing tags.

Global Arguments
    --debug             : Increase logging verbosity to show all debug logs.
    --help -h           : Show this help message and exit.
    --output -o         : Output format.  Allowed values: json, tsv, list, table, jsonc.  Default:
                          json.
    --query             : JMESPath query string. See http://jmespath.org/ for more information and
                          examples.
    --verbose           : Increase logging verbosity. Use --debug for full debug logs.

Examples
    Update tags of a container registry and show result in a table
        az registry update -n <registry-name> --tags key1=value1;key2=value2 -o table
```

## The catalog of repositories in the specified registry
```
Command
    az registry catalog: The catalog of repositories in the specified registry.

Arguments
    --name -n [Required]: The primary resource name.
    --password          : The password used to log into the container registry.
    --username          : The username used to log into the container registry.

Global Arguments
    --debug             : Increase logging verbosity to show all debug logs.
    --help -h           : Show this help message and exit.
    --output -o         : Output format.  Allowed values: json, tsv, list, table, jsonc.  Default:
                          json.
    --query             : JMESPath query string. See http://jmespath.org/ for more information and
                          examples.
    --verbose           : Increase logging verbosity. Use --debug for full debug logs.

Examples
    The catalog of repositories in a registry under the current subscription
        az registry catalog -n <registry-name>
    The catalog of repositories in any registry with credentials
        az registry catalog -n <registry-name> --username <username> --password <password>
```

## The list of tags for a given repository in the specified registry
```
Command
    az registry tags: The list of tags for a given repository in the specified registry.

Arguments
    --name -n    [Required]: The primary resource name.
    --repository [Required]: The repository to obtain tags from.
    --password             : The password used to log into the container registry.
    --username             : The username used to log into the container registry.

Global Arguments
    --debug                : Increase logging verbosity to show all debug logs.
    --help -h              : Show this help message and exit.
    --output -o            : Output format.  Allowed values: json, tsv, list, table, jsonc.
                             Default: json.
    --query                : JMESPath query string. See http://jmespath.org/ for more information
                             and examples.
    --verbose              : Increase logging verbosity. Use --debug for full debug logs.

Examples
    The list of tags for a given repository in a registry under the current subscription
        az registry tags -n <registry-name> --repository <repository>
    The list of tags for a given repository in any registry with credentials
        az registry tags -n <registry-name> --repository <repository> --username <username>
        --password <password>
```