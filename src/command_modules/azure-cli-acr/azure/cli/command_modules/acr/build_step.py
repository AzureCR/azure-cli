# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ._utils import (
    validate_managed_registry,
    get_resource_group_name_by_registry_name
)
from .azure.mgmt.containerregistry.v2018_02_01_preview.models import DockerBuildStepUpdateParameters

BUILD_STEPS_NOT_SUPPORTED = 'Build Steps are only supported for managed registries.'


def acr_build_step_list(cmd,
                        client,
                        build_task_name,
                        registry_name,
                        resource_group_name=None):
    _, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, BUILD_STEPS_NOT_SUPPORTED)
    return client.list(resource_group_name, registry_name, build_task_name)


def acr_build_step_show(cmd,
                        client,
                        step_name,
                        build_task_name,
                        registry_name,
                        resource_group_name=None):
    _, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, BUILD_STEPS_NOT_SUPPORTED)
    return client.get(resource_group_name, registry_name, build_task_name, step_name)


def acr_build_step_update_get():
    return DockerBuildStepUpdateParameters()


def acr_build_step_update_set(cmd,
                              client,
                              step_name,
                              build_task_name,
                              registry_name,
                              resource_group_name=None,
                              parameters=None):
    resource_group_name = get_resource_group_name_by_registry_name(
        cmd.cli_ctx, registry_name, resource_group_name)
    return client.update(resource_group_name, registry_name, build_task_name, step_name, parameters)


def acr_build_step_update_custom(cmd, # pylint: disable=unused-argument
                                 instance,
                                 branch=None,
                                 image_names=None,
                                 push_enabled=None,
                                 no_cache=None,
                                 docker_file_path=None,
                                 build_arg=None,
                                 secret_build_arg=None,
                                 base_image_trigger=None):
    if branch is not None:
        instance.branch = branch

    if image_names is not None:
        instance.image_names = image_names

    if push_enabled is not None:
        instance.is_push_enabled = push_enabled == 'true'

    if no_cache is not None:
        instance.no_cache = no_cache == 'true'

    if docker_file_path is not None:
        instance.docker_file_path = docker_file_path

    if build_arg is not None or secret_build_arg is not None:
        instance.build_arguments = (build_arg if build_arg else []) + (secret_build_arg if secret_build_arg else [])

    if base_image_trigger is not None:
        instance.base_image_trigger = base_image_trigger

    return instance
