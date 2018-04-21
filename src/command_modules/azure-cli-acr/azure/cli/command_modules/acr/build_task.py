# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError
from azure.cli.core.commands import LongRunningOperation
from .azure.mgmt.containerregistry.v2018_02_01_preview.models import (
    BuildTaskBuildRequest,
    BuildTaskUpdateParameters
)
from ._utils import (
    arm_deploy_template_build_task_create,
    validate_managed_registry,
    get_resource_group_name_by_registry_name
)

BUILD_TASKS_NOT_SUPPORTED = 'Build Tasks are only supported for managed registries.'


def acr_build_task_create(cmd,
                          client,
                          build_task_name,
                          registry_name,
                          repository_url,
                          image_names,
                          git_access_token,
                          alias=None,
                          status='Enabled',
                          os_type='Linux',
                          cpu=1,
                          timeout=3600,
                          commit_trigger_enabled='true',
                          branch='master',
                          push_enabled='true',
                          no_cache='false',
                          docker_file_path="Dockerfile",
                          build_arg=None,
                          secret_build_arg=None,
                          base_image_trigger='Runtime',
                          resource_group_name=None):

    registry, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, BUILD_TASKS_NOT_SUPPORTED)

    LongRunningOperation(cmd.cli_ctx)(
        arm_deploy_template_build_task_create(
            cli_ctx=cmd.cli_ctx,
            resource_group_name=resource_group_name,
            build_task_name=build_task_name,
            registry_name=registry_name,
            location=registry.location,
            repository_url=repository_url,
            image_names=image_names,
            git_access_token=git_access_token,
            alias=alias if alias else build_task_name,
            status=status,
            os_type=os_type,
            cpu=cpu,
            timeout=timeout,
            commit_trigger_enabled=commit_trigger_enabled == 'true',
            branch=branch,
            push_enabled=push_enabled == 'true',
            no_cache=no_cache == 'true',
            docker_file_path=docker_file_path,
            build_arguments=(build_arg if build_arg else []) + (secret_build_arg if secret_build_arg else []),
            base_image_trigger=base_image_trigger
        )
    )
    return client.get(resource_group_name, registry_name, build_task_name)


def acr_build_task_show(cmd,
                        client,
                        build_task_name,
                        registry_name,
                        resource_group_name=None):
    _, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, BUILD_TASKS_NOT_SUPPORTED)
    return client.get(resource_group_name, registry_name, build_task_name)


def acr_build_task_list(cmd,
                        client,
                        registry_name,
                        resource_group_name=None):
    _, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, BUILD_TASKS_NOT_SUPPORTED)
    return client.list(resource_group_name, registry_name)


def acr_build_task_delete(cmd,
                          client,
                          build_task_name,
                          registry_name,
                          resource_group_name=None):
    _, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, BUILD_TASKS_NOT_SUPPORTED)
    return client.delete(resource_group_name, registry_name, build_task_name)


def acr_build_task_update_get():
    return BuildTaskUpdateParameters()


def acr_build_task_update_set(cmd,
                              client,
                              build_task_name,
                              registry_name,
                              resource_group_name=None,
                              parameters=None):
    resource_group_name = get_resource_group_name_by_registry_name(
        cmd.cli_ctx, registry_name, resource_group_name)
    return client.update(resource_group_name, registry_name, build_task_name, parameters)


def acr_build_task_update_custom(cmd, # pylint: disable=unused-argument
                                 instance,
                                 alias=None,
                                 status=None,
                                 os_type=None,
                                 cpu=None,
                                 timeout=None,
                                 repository_url=None,
                                 commit_trigger_enabled=None,
                                 git_access_token=None,
                                 tags=None):
    if alias is not None:
        instance.alias = alias

    if status is not None:
        instance.status = status

    if os_type is not None:
        instance.platform.os_type = os_type

    if cpu is not None:
        instance.platform.cpu = cpu

    if timeout is not None:
        instance.timeout = timeout

    if repository_url is not None:
        instance.source_repository.repository_url = repository_url

    if commit_trigger_enabled is not None:
        instance.source_repository.is_commit_trigger_enabled = commit_trigger_enabled == 'true'

    if git_access_token is not None:
        instance.source_repository.source_control_auth_properties.git_access_token = git_access_token

    if tags is not None:
        instance.tags = tags

    return instance


def acr_build_task_run(cmd,
                       client, # cf_acr_builds
                       build_task_name,
                       registry_name,
                       no_logs=False,
                       resource_group_name=None):
    _, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, BUILD_TASKS_NOT_SUPPORTED)

    from ._client_factory import cf_acr_registries
    client_registries = cf_acr_registries(cmd.cli_ctx)

    queued_build = LongRunningOperation(cmd.cli_ctx)(
        client_registries.queue_build(resource_group_name, registry_name, BuildTaskBuildRequest(build_task_name)))

    if no_logs:
        return queued_build

    build_id = queued_build.build_id
    print("Queued a build with build ID: {}".format(build_id))
    print("Waiting for a build agent...")
    acr_build_task_logs(cmd, client, registry_name, build_id, build_task_name)


def acr_build_task_list_builds(cmd,
                               client, # cf_acr_builds
                               registry_name,
                               build_task_name=None,
                               resource_group_name=None):
    _, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, BUILD_TASKS_NOT_SUPPORTED)

    if build_task_name:
        filter_str = "BuildTaskName eq '{}'".format(build_task_name)
        return client.list(resource_group_name, registry_name, filter=filter_str)

    return client.list(resource_group_name, registry_name)


def acr_build_task_logs(cmd,
                        client, # cf_acr_builds
                        registry_name,
                        build_id=None,
                        build_task_name=None,
                        resource_group_name=None):
    _, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, BUILD_TASKS_NOT_SUPPORTED)

    if not build_id:
        # show logs for the last build
        paged_builds = acr_build_task_list_builds(cmd, client, registry_name, build_task_name)
        try:
            build_id = paged_builds.get(0)[0].build_id
            print("Showing logs for the last updated build")
            print("Build ID: {}".format(build_id))
        except (AttributeError, KeyError, TypeError, IndexError):
            raise CLIError('Unable to get the latest build information.')

    from .build import acr_build_show_logs
    return acr_build_show_logs(cmd, client, registry_name, build_id, resource_group_name)
