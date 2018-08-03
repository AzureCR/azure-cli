# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from os.path import isdir
from base64 import b64encode
import requests
from requests.utils import to_native_string

from knack.util import CLIError
from knack.log import get_logger
from azure.cli.core.util import should_disable_connection_verify

from ._docker_utils import get_login_credentials, log_registry_response


logger = get_logger(__name__)


def _get_basic_auth_str(username, password):
    return 'Basic ' + to_native_string(
        b64encode(('%s:%s' % (username, password)).encode('latin1')).strip()
    )


def acr_helm_push(cmd,
                  chart_package,
                  registry_name,
                  resource_group_name=None,
                  username=None,
                  password=None):
    if isdir(chart_package):
        raise CLIError("Please run 'helm package {}' to generate a chart package first.".format(chart_package))

    login_server, username, password = get_login_credentials(
        cli_ctx=cmd.cli_ctx,
        registry_name=registry_name,
        resource_group_name=resource_group_name,
        username=username,
        password=password,
        use_bearer=False)

    try:
        with open(chart_package, 'rb') as input_file:
            response = requests.request(
                method='post',
                url='https://{}/api/charts'.format(login_server),
                headers={
                    'Authorization': _get_basic_auth_str(username, password)
                },
                files={
                    'chart': input_file
                },
                verify=(not should_disable_connection_verify())
            )
        log_registry_response(response)
        logger.warning(response)
        return response.json()
    except Exception as e:  # pylint: disable=broad-except
        raise CLIError(e)


def acr_helm_init(cmd, registry_name, resource_group_name=None, username=None, password=None):
    from subprocess import Popen
    helm_command = _get_helm_command()

    login_server, username, password = get_login_credentials(
        cli_ctx=cmd.cli_ctx,
        registry_name=registry_name,
        resource_group_name=resource_group_name,
        username=username,
        password=password,
        use_bearer=False)

    p = Popen([helm_command, 'repo', 'add', registry_name,
               'https://{}/'.format(login_server),
               '--username', username, '--password', password])
    p.wait()


def _get_helm_command():
    return 'helm'
