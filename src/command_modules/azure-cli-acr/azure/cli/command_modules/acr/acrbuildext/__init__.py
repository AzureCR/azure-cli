# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long

from azure.cli.core import AzCommandsLoader
import azext_acrbuildext._help  # pylint: disable=unused-import
from ._client_factory import cf_acr_builds, cf_acr_build_tasks
from ._format import build_output_format

class AcrBuildCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        super(AcrBuildCommandsLoader, self).__init__(cli_ctx=cli_ctx)

    def load_command_table(self, _):
        from azure.cli.core.commands import CliCommandType

        acr_build_util = CliCommandType(
            operations_tmpl='azext_acrbuildext.build#{}',
            client_factory=cf_acr_builds
        )

        acr_build_task_util = CliCommandType(
            operations_tmpl='azext_acrbuildext.build_task#{}',
            table_transformer=build_output_format,
            client_factory=cf_acr_build_tasks
        )

        with self.command_group('acr build', acr_build_util) as g:
            g.command('show-logs', 'acr_build_show_logs')
            g.command('', 'acr_queue') # TODO: it should be moved to acr command group once we can integrate the full sdk.

        with self.command_group('acr build-task', acr_build_task_util) as g:
            g.command('create', 'acr_build_task_create')
            g.command('show', 'acr_build_task_show')
            g.command('list', 'acr_build_task_list')
            g.command('delete', 'acr_build_task_delete')
            g.command('list-builds', 'acr_build_task_list_builds')
            g.command('run', 'acr_build_task_run')
            g.command('logs', 'acr_build_task_logs')
        return self.command_table

    def load_arguments(self, _):
        from ._params import load_arguments as acr_load_arguments
        acr_load_arguments(self, _)
        return self.argument_context


COMMAND_LOADER_CLS = AcrBuildCommandsLoader
