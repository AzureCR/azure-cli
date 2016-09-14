Microsoft Azure CLI 'acr' Command Module
==================================

Commands to manage Azure container registries
-------------
::

    Group
        az acr: Commands to manage Azure container registries.

    Subgroups:
        repository

    Commands:
        create    : Create a container registry.
        delete    : Delete a container registry.
        list      : List container registries.
        show      : Get a container registry.
        update    : Update a container registry.

Create a container registry
-------------
::

    Command
        az acr create: Create a container registry.

    Arguments
        --location -l       [Required]: Location.
        --name -n           [Required]: Name of container registry.
        --resource-group -g [Required]: Name of resource group.
        --storage-account-key -k      : Key of storage account.
        --storage-account-name -s     : Name of storage account.

    Examples
        Create a container registry with managed storage account
            az acr create -n <registry-name> -g <resource-group> -l <location>
        Create a container registry with new/existing storage account in the current subscription
            az acr create -n <registry-name> -g <resource-group> -l <location> -s <storage-account-name>
        Create a container registry with your own storage account in any subscription
            az acr create -n <registry-name> -g <resource-group> -l <location> -s <storage-account-name>
            -k <storage-account-key>

Delete a container registry
-------------
::

    Command
        az acr delete: Delete a container registry.

    Arguments
        --name -n [Required]: Name of container registry.

List container registries
-------------
::

    Command
        az acr list: List container registries.

    Arguments
        --resource-group -g: Name of resource group.

    Examples
        List container registries and show result in a table
            az acr list -o table
        List container registries in a resource group and show result in a table
            az acr list -g <resource-group> -o table

Get a container registry
-------------
::

    Command
        az acr show: Get a container registry.

    Arguments
        --name -n [Required]: Name of container registry.

Update a container registry
-------------
::

    Command
        az acr update: Update a container registry.

    Arguments
        --name -n [Required]: Name of container registry.
        --tags              : Multiple semicolon separated tags in 'key[=value]' format.  Use "" to
                            clear existing tags.
    Examples
        Update tags of a container registry and show result in a table
            az acr update -n <registry-name> --tags key1=value1;key2=value2 -o table

List repositories in a given container registry
-------------
::

    Command
        az acr repository list: List repositories in a given container registry.

    Arguments
        --login-server [Required]: The URL of a container registry login server.
        --password               : The password used to log into the container registry.
        --username               : The username used to log into the container registry.

    Examples
        List repositories in a given container registry under the current subscription
            az acr repository list --login-server <login-server>
        List repositories in a given container registry with credentials
            az acr repository list --login-server <login-server> --username <username> --password
            <password>

Show tags of a given repository in a given container registry
-------------
::

    Command
        az acr repository show-tags: Show tags of a given repository in a given container registry.

    Arguments
        --login-server [Required]: The URL of a container registry login server.
        --repository   [Required]: The repository to obtain tags from.
        --password               : The password used to log into the container registry.
        --username               : The username used to log into the container registry.

    Examples
        Show tags of a given repository in a given container registry under the current subscription
            az acr repository show-tags --login-server <login-server> --repository <repository>
        Show tags of a given repository in a given container registry with credentials
            az acr repository show-tags --login-server <login-server> --repository <repository>
            --username <username> --password <password>
