#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

import re

from azure.cli.core._util import CLIError

def validate_registry_name(namespace):
    if namespace.registry_name:
        registry_name = namespace.registry_name
        if len(registry_name) < 5 or len(registry_name) > 60:
            raise CLIError('The registry name must be between 5 and 60 characters.')

        p = re.compile('^([A-Za-z0-9]+)$')

        if not p.match(registry_name):
            raise CLIError('The registry name can contain only letters and numbers.')
