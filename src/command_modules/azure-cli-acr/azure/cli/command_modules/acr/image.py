from azure.cli.core.commands import LongRunningOperation
from knack.util import CLIError
from azure.mgmt.containerregistry.v2018_02_01_preview.models import (
    ImportImageParameters,
    ImportSource
)
from ._utils import (
    validate_managed_registry,
    get_resource_id_by_registry_name
)

IMPORT_NOT_SUPPORTED = "Image imports are only supported for managed registries."

def acr_image_import(cmd,
                     client,
                     registry_name,
                     source_image,
                     resource_id=None,
                     tags=None,
                     resource_group_name=None,
                     repositories=None,
                     mode='NoForce'):
    _, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, IMPORT_NOT_SUPPORTED)

    slash = source_image.find("/")
    if slash < 0:
        if not resource_id: raise CLIError("Source image not valid.")
    else:
        try:
            source_registry = source_image[:source_image.index(".")]
        except ValueError:
            raise CLIError("Source image not valid.")
        resource_id = get_resource_id_by_registry_name(cmd.cli_ctx, source_registry)
        source_image = source_image[source_image.index("/") + 1 :]

    image_source = ImportSource(resource_id=resource_id, source_image=source_image)

    #todo move to RP
    if tags is None and repositories is None:
        tags = [source_image]

    import_parameters = ImportImageParameters(source=image_source,
                                              target_tags=tags,
                                              untagged_target_repositories=repositories,
                                              mode=mode)

    return LongRunningOperation(cmd.cli_ctx)(client.import_image(
        resource_group_name=resource_group_name,
        registry_name=registry_name,
        parameters=import_parameters))
