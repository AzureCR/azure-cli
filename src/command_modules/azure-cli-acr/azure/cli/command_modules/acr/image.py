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
                     image=None,
                     resource_id=None,
                     source_image=None,
                     target_tags=None,
                     resource_group_name=None,
                     untagged_target_repositories=None,
                     mode='NoForce'):
    registry, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, IMPORT_NOT_SUPPORTED)

    if image is not None:
        try:
            source_registry = image[:image.index(".")]
        except ValueError:
            raise CLIError("Source image not valid.")
        resource_id = get_resource_id_by_registry_name(cmd.cli_ctx, source_registry)
        source_image = image[image.index("/") + 1 :]
    elif resource_id is None and source_image is None:
        raise CLIError("Source image not valid.")

    image_source = ImportSource(resource_id=resource_id, source_image=source_image)

    if target_tags is None:
        target_tags = [source_image]

    import_parameters = ImportImageParameters(source=image_source,
                                              target_tags=target_tags,
                                              untagged_target_repositories=untagged_target_repositories,
                                              mode=mode)

    return LongRunningOperation(cmd.cli_ctx)(client.import_image(
        resource_group_name=resource_group_name,
        registry_name=registry_name,
        parameters=import_parameters))
