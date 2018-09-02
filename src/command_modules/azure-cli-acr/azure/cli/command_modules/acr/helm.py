# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from os.path import isdir
import time
import requests
from requests.utils import to_native_string

from knack.util import CLIError
from knack.log import get_logger
from azure.cli.core.util import should_disable_connection_verify

from ._docker_utils import (
    get_login_credentials,
    get_access_credentials,
    get_authorization_header,
    log_registry_response
)


logger = get_logger(__name__)


ALLOWED_HTTP_METHOD = ['get', 'post', 'delete']
ROUTE_PREFIX = '/artifact/v1/repo/_helm'


def _parse_helm_error_message(error_message, response):
    import json
    try:
        server_message = json.loads(response.text)['errors'][0]['message']
        error_message = 'Error: {}'.format(server_message) if server_message else error_message
    except (ValueError, KeyError, TypeError, IndexError):
        pass

    if not error_message.endswith('.'):
        error_message = '{}.'.format(error_message)

    try:
        correlation_id = response.headers['x-ms-correlation-request-id']
        return '{} Correlation ID: {}.'.format(error_message, correlation_id)
    except (KeyError, TypeError, AttributeError):
        return error_message


def _request_helm_data_from_registry(http_method,
                                     login_server,
                                     path,
                                     username,
                                     password,
                                     result_index=None,
                                     files_payload=None,
                                     output_file=None,
                                     params=None,
                                     retry_times=3,
                                     retry_interval=5):
    if http_method not in ALLOWED_HTTP_METHOD:
        raise ValueError("Allowed http method: {}".format(ALLOWED_HTTP_METHOD))

    if http_method in ['get', 'delete'] and files_payload:
        raise ValueError("Empty files payload is required for http method: {}".format(http_method))

    if http_method in ['post'] and not files_payload:
        raise ValueError("Non-empty files payload is required for http method: {}".format(http_method))

    url = 'https://{}{}{}'.format(login_server, ROUTE_PREFIX, path)
    headers = get_authorization_header(username, password)

    for i in range(0, retry_times):
        errorMessage = None
        try:
            response = requests.request(
                method=http_method,
                url=url,
                headers=headers,
                params=params,
                files=files_payload,
                verify=(not should_disable_connection_verify())
            )
            log_registry_response(response)

            if response.status_code == 200:
                if output_file:
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    logger.warning("Fetched helm chart '%s'.", output_file)
                    return None, None
                result = response.json()[result_index] if result_index else response.json()
                next_link = response.headers['link'] if 'link' in response.headers else None
                return result, next_link
            elif response.status_code == 201 or response.status_code == 202:
                result = None
                try:
                    result = response.json()[result_index] if result_index else response.json()
                except ValueError:
                    logger.debug('Response is empty or is not a valid json.')
                return result, None
            elif response.status_code == 204:
                return None, None
            elif response.status_code == 401:
                raise CLIError(_parse_helm_error_message('Authentication required.', response))
            elif response.status_code == 404:
                raise CLIError(_parse_helm_error_message('The requested data does not exist.', response))
            else:
                raise Exception(_parse_helm_error_message(
                    'Could not {} the requested data.'.format(http_method), response))
        except CLIError:
            raise
        except Exception as e:  # pylint: disable=broad-except
            errorMessage = str(e)
            logger.debug('Retrying %s with exception %s', i + 1, errorMessage)
            time.sleep(retry_interval)

    raise CLIError(errorMessage)


def acr_helm_list(cmd,
                  registry_name,
                  chart=None,
                  resource_group_name=None,
                  username=None,
                  password=None):
    login_server, username, password = get_access_credentials(
        cli_ctx=cmd.cli_ctx,
        registry_name=registry_name,
        resource_group_name=resource_group_name,
        username=username,
        password=password,
        repository='',
        permission='pull')

    return _request_helm_data_from_registry(
        http_method='get',
        login_server=login_server,
        path='/api/charts/{}'.format(chart) if chart else '/api/charts',
        username=username,
        password=password)[0]


def acr_helm_show(cmd,
                  registry_name,
                  chart,
                  version,
                  resource_group_name=None,
                  username=None,
                  password=None):
    login_server, username, password = get_access_credentials(
        cli_ctx=cmd.cli_ctx,
        registry_name=registry_name,
        resource_group_name=resource_group_name,
        username=username,
        password=password,
        repository='',
        permission='pull')

    return _request_helm_data_from_registry(
        http_method='get',
        login_server=login_server,
        path='/api/charts/{}/{}'.format(chart, version),
        username=username,
        password=password)[0]


def acr_helm_delete(cmd,
                    registry_name,
                    chart,
                    version,
                    resource_group_name=None,
                    username=None,
                    password=None):
    login_server, username, password = get_access_credentials(
        cli_ctx=cmd.cli_ctx,
        registry_name=registry_name,
        resource_group_name=resource_group_name,
        username=username,
        password=password,
        repository='',
        permission='*')

    return _request_helm_data_from_registry(
        http_method='delete',
        login_server=login_server,
        path='/api/charts/{}/{}'.format(chart, version),
        username=username,
        password=password)[0]


def acr_helm_fetch(cmd,
                   registry_name,
                   chart,
                   version=None,
                   resource_group_name=None,
                   username=None,
                   password=None):
    login_server, username, password = get_access_credentials(
        cli_ctx=cmd.cli_ctx,
        registry_name=registry_name,
        resource_group_name=resource_group_name,
        username=username,
        password=password,
        repository='',
        permission='pull')

    version = _request_helm_data_from_registry(
        http_method='get',
        login_server=login_server,
        path='/api/charts/{}/{}'.format(chart, version) if version else '/api/charts/{}'.format(chart),
        username=username,
        password=password)[0]

    if isinstance(version, list):
        version = version[0]

    url = version['urls'][0]

    return _request_helm_data_from_registry(
        http_method='get',
        login_server=login_server,
        path='/{}'.format(url),
        output_file=url.split('/')[-1],
        username=username,
        password=password)[0]


def acr_helm_push(cmd,
                  chart_package,
                  registry_name,
                  resource_group_name=None,
                  username=None,
                  password=None):
    if isdir(chart_package):
        raise CLIError("Please run 'helm package {}' to generate a chart package first.".format(chart_package))

    login_server, username, password = get_access_credentials(
        cli_ctx=cmd.cli_ctx,
        registry_name=registry_name,
        resource_group_name=resource_group_name,
        username=username,
        password=password,
        repository='',
        permission='*')

    try:
        with open(chart_package, 'rb') as input_file:
            return _request_helm_data_from_registry(
                http_method='post',
                login_server=login_server,
                path='/api/charts',
                username=username,
                password=password,
                files_payload={
                    'chart': input_file
                },
                retry_times=1)[0]
    except OSError as e:
        raise CLIError(e)


def acr_helm_repo_add(cmd, registry_name, resource_group_name=None, username=None, password=None):
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
               'https://{}{}'.format(login_server, ROUTE_PREFIX),
               '--username', username, '--password', password])
    p.wait()


def _get_helm_command():
    return 'helm'
