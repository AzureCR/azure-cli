# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError
from ._client_factory import cf_acr_registries

def validate_registry_name(cmd, namespace):
    if namespace.registry_name:
        client = cf_acr_registries(cmd.cli_ctx)
        registry_name = namespace.registry_name

        result = client.check_name_availability(registry_name)

        if not result.name_available:  # pylint: disable=no-member
            raise CLIError(result.message)  # pylint: disable=no-member


def validate_headers(namespace):
    """Extracts multiple space-separated headers in key[=value] format. """
    if isinstance(namespace.headers, list):
        headers_dict = {}
        for item in namespace.headers:
            headers_dict.update(validate_header(item))
        namespace.headers = headers_dict


def validate_header(string):
    """Extracts a single header in key[=value] format. """
    result = {}
    if string:
        comps = string.split('=', 1)
        result = {comps[0]: comps[1]} if len(comps) > 1 else {string: ''}
    return result


def validate_build_arg(namespace):
    if isinstance(namespace.build_arg, list):
        build_arguments_list = []
        for item in namespace.build_arg:
            build_arguments_list.append(validate_build_argument(item, False))
        namespace.build_arg = build_arguments_list


def validate_secret_build_arg(namespace):
    if isinstance(namespace.secret_build_arg, list):
        build_arguments_list = []
        for item in namespace.secret_build_arg:
            build_arguments_list.append(validate_build_argument(item, True))
        namespace.secret_build_arg = build_arguments_list


def validate_build_argument(string, is_secret):
    """Extracts a single build argument in key[=value] format. """
    if string:
        comps = string.split('=', 1)
        if len(comps) > 1:
            return {'name': comps[0], 'value': comps[1], 'isSecret': is_secret}
        return {'name': comps[0], 'value': '', 'isSecret': is_secret}
    return {}


def validate_build_task_name(namespace):
    """Validate the name of the build task name. """
    import re
    build_task_name = namespace.build_task_name
    p = re.compile('^[a-zA-Z0-9]*$')
    if p.match(build_task_name) is None:
        raise CLIError(
            "Build task name may contain alpha numeric characters only and must be between 5 and 50 characters.")


#TODO: ankheman add variable tag support
def validate_image_names(namespace):
    # reference: https://github.com/docker/distribution/tree/master/reference

    image_names = namespace.image_names
    for image_name in image_names:
        if not image_name:
            raise CLIError("'--image -t' value should not be empty.")

        tokens = image_name.split(':')
        if(len(tokens) > 2):
            raise CLIError(
                "'--image -t' value should be repository and optionally a tag in the 'repository:tag' format")
        import re

        # check repository
        repository = tokens[0]
        if len(repository) > 255:
            raise CLIError(
                "The repository of '--image -t' value should be no more than 255 characters.")
        else:
            # TODO: Consider move the validation to server side
            if re.match(r"^[a-z0-9]+(?:(?:(?:[._]|__|[-]*)[a-z0-9]+)+)?(?:(?:/[a-z0-9]+(?:(?:(?:[._]|__|[-]*)[a-z0-9]+)+)?)+)?$", repository) is None:
                raise CLIError(
                    "The '--image -t' value is not valid. Please check https://docs.docker.com/engine/reference/commandline/tag/.")

        # check tag
        if len(tokens) == 2:
            tag = tokens[1]
            if re.match(r"^[\w][\w.-]{0,127}$", tag) is None:
                raise CLIError(
                    "The '--image -t' value is not valid. Please check https://docs.docker.com/engine/reference/commandline/tag/.")
