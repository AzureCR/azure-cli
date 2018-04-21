# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ._utils import (
    validate_managed_registry,
    get_resource_group_name_by_registry_name
)
from .azure.mgmt.containerregistry.v2018_02_01_preview.models import DockerBuildStepUpdateParameters


BUILD_TASKS_NOT_SUPPORTED = 'Build Steps are only supported for managed registries.'


def acr_build_step_list(cmd,
                        client,
                        build_task_name,
                        registry_name,
                        resource_group_name=None):
    _, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, BUILD_TASKS_NOT_SUPPORTED)
    return client.list(resource_group_name, registry_name, build_task_name)


def acr_build_step_show(cmd,
                        client,
                        step_name,
                        build_task_name,
                        registry_name,
                        resource_group_name=None):
    _, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, BUILD_TASKS_NOT_SUPPORTED)
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


def acr_build_step_update_custom(cmd,
                                 instance,
                                 branch=None,
                                 image_names=None,
                                 is_push_enabled=False,
                                 no_cache=False,
                                 docker_file_path=None,
                                 context_path=None,
                                 build_arguments=None,
                                 base_image_trigger=None):
    # TODO: [doyou] Add custom update
    return instance
