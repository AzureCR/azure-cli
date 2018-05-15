from knack.util import CLIError
from azure.cli.core.commands import LongRunningOperation
from azure.mgmt.containerregistry.v2018_02_01_preview.models import (
    ImportImageParameters,
    ImportSource,
    ImportMode
)
from ._utils import (
    validate_managed_registry,
    get_resource_id_by_registry_name,
    get_registry_name_by_resource_id
)

IMPORT_NOT_SUPPORTED = "Image imports are only supported for managed registries."
INVALID_SOURCE_IMAGE = "Please specify source image in the form of 'registry.azurecr.io/repository[:tag]'."
SOURCE_REGISTRY_NOT_FOUND = "Source registry cannot be found in the current subscription. " \
                            "Please specify the full resource ID for it: "


def acr_image_import(cmd,
                     client,
                     registry_name,
                     source_image,
                     resource_id=None,
                     target_tags=None,
                     resource_group_name=None,
                     repository=None,
                     force=False):
    _, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, IMPORT_NOT_SUPPORTED)

    dot = source_image.find('.')
    slash = source_image.find('/')

    if dot < 0 or slash < 0:
        raise CLIError(INVALID_SOURCE_IMAGE)

    source_registry = source_image[:dot]
    if not source_registry:
        raise CLIError(INVALID_SOURCE_IMAGE)

    if not resource_id:
        resource_id = get_resource_id_by_registry_name(cmd.cli_ctx, source_registry, SOURCE_REGISTRY_NOT_FOUND)
    registry_name_from_resource_id = get_registry_name_by_resource_id(
        resource_id)
    if source_registry != registry_name_from_resource_id:
        raise CLIError(
            "Registry mismatch. Please check either source-image or resource ID " \
            "to make sure that they are referring to the same registry and give another try.")

    source_image = source_image[slash + 1:]
    if not source_image:
        raise CLIError(INVALID_SOURCE_IMAGE)

    image_source = ImportSource(
        resource_id=resource_id, source_image=source_image)

    if target_tags is None and repository is None:
        target_tags = [source_image]

    import_parameters = ImportImageParameters(source=image_source,
                                              target_tags=target_tags,
                                              untagged_target_repositories=repository,
                                              mode=ImportMode.force.value if force else ImportMode.no_force.value)

    return LongRunningOperation(cmd.cli_ctx)(client.import_image(
        resource_group_name=resource_group_name,
        registry_name=registry_name,
        parameters=import_parameters))
