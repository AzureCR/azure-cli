# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long

from azure.cli.core import AzCommandsLoader
import azext_acrbuildext._help  # pylint: disable=unused-import
from ._client_factory import cf_acr_builds, cf_acr_build_tasks, cf_acr_build_steps
from ._format import build_output_format, build_task_output_format, build_step_output_format

class AcrBuildCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        super(AcrBuildCommandsLoader, self).__init__(cli_ctx=cli_ctx)

    def load_command_table(self, _):
        from azure.cli.core.commands import CliCommandType

        acr_build_util = CliCommandType(
            operations_tmpl='azext_acrbuildext.build#{}',
            table_transformer=build_output_format,
            client_factory=cf_acr_builds
        )

        acr_build_task_util = CliCommandType(
            operations_tmpl='azext_acrbuildext.build_task#{}',
            table_transformer=build_task_output_format,
            client_factory=cf_acr_build_tasks
        )

        acr_build_step_util = CliCommandType(
            operations_tmpl='azext_acrbuildext.build_step#{}',
            table_transformer=build_step_output_format,
            client_factory=cf_acr_build_steps
        )

        with self.command_group('acr', acr_build_util) as g:
            g.command('build', 'acr_build')

        with self.command_group('acr build-task', acr_build_task_util) as g:
            g.command('create', 'acr_build_task_create')
            g.command('show', 'acr_build_task_show')
            g.command('list', 'acr_build_task_list')
            g.command('delete', 'acr_build_task_delete')
            g.generic_update_command('update',
                                     getter_name='acr_build_task_update_get',
                                     setter_name='acr_build_task_update_set',
                                     custom_func_name='acr_build_task_update_custom',
                                     custom_func_type=acr_build_task_util,
                                     client_factory=cf_acr_build_tasks,
                                     table_transformer=build_task_output_format)
            g.command('run', 'acr_build_task_run', client_factory=cf_acr_builds,
                      table_transformer=build_output_format)
            g.command('list-builds', 'acr_build_task_list_builds', client_factory=cf_acr_builds,
                      table_transformer=build_output_format)
            g.command('logs', 'acr_build_task_logs', client_factory=cf_acr_builds,
                      table_transformer=None)

        with self.command_group('acr build-task step', acr_build_step_util) as g:
            g.command('list', 'acr_build_step_list')
            g.command('show', 'acr_build_step_show')
            g.generic_update_command('update',
                                     getter_name='acr_build_step_update_get',
                                     setter_name='acr_build_step_update_set',
                                     custom_func_name='acr_build_step_update_custom',
                                     custom_func_type=acr_build_step_util,
                                     client_factory=cf_acr_build_steps,
                                     table_transformer=build_step_output_format)

        return self.command_table

    def load_arguments(self, _):
        from ._params import load_arguments as acr_load_arguments
        acr_load_arguments(self, _)
        return self.argument_context


COMMAND_LOADER_CLS = AcrBuildCommandsLoader
