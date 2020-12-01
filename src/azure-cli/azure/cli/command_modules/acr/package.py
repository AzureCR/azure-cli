# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import platform
from six.moves.urllib.request import urlopen  # pylint: disable=import-error

from knack.util import CLIError
from knack.log import get_logger

from azure.cli.core.util import in_cloud_console

from ._utils import user_confirmation

from ._docker_utils import (
    get_access_credentials,
    request_data_from_registry,
    PackageAccessTokenPermission,
    PackageType
)


logger = get_logger(__name__)


def acr_package_list(cmd,
                     registry_name,
                     package_type,
                     package_name=None,
                     tenant_suffix=None,
                     username=None,
                     password=None):
    login_server, username, password = get_access_credentials(
        cmd=cmd,
        registry_name=registry_name,
        tenant_suffix=tenant_suffix,
        username=username,
        password=password,
        package_type=package_type,
        repository=package_name,
        permission=PackageAccessTokenPermission.METADATA_READ.value)

    html = request_data_from_registry(
        http_method='get',
        login_server=login_server,
        path=_get_package_path(package_type, package_name),
        username=username,
        password=password)[0]

    print(html)


def acr_package_delete(cmd,
                       registry_name,
                       package_type,
                       package_name,
                       version,
                       tenant_suffix=None,
                       username=None,
                       password=None,
                       yes=False):
    message = "This operation will delete the package '{}' version '{}'".format(package_name, version)
    user_confirmation("{}.\nAre you sure you want to continue?".format(message), yes)

    login_server, username, password = get_access_credentials(
        cmd=cmd,
        registry_name=registry_name,
        tenant_suffix=tenant_suffix,
        username=username,
        password=password,
        package_type=package_type,
        repository=package_name,
        permission=PackageAccessTokenPermission.DELETE.value)

    return request_data_from_registry(
        http_method='delete',
        login_server=login_server,
        path=_get_package_path(package_type, package_name, version),
        username=username,
        password=password)[0]


def _get_package_path(package_type, package_name, version=None):
    if package_type is PackageType.PYPI:
        if not package_name:
            return '/pkg/v1/pypi'
        if not version:
            return '/pkg/v1/pypi/{}'.format(package_name)

        return '/pkg/v1/pypi/{}/{}'.format(package_name, version)

    raise ValueError("Unknown package type {}".format(package_type))
