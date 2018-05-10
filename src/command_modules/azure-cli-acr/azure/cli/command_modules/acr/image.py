from azure.cli.core.commands import LongRunningOperation
from azure.mgmt.containerregistry.v2018_02_01_preview.models import (
    ImportImageParameters,
    ImportSource
)
from ._utils import (
    validate_managed_registry,
    get_resource_id_by_registry_name
)

from ._client_factory import cf_acr_registries

IMPORT_NOT_SUPPORTED = "Image imports are only supported for managed registries."

def acr_image_import(cmd,
                     registry_name,
                     image=None,
                     resource_id=None,
                     source_image=None,
                     target_tags=None,
                     resource_group_name=None,
                     untagged_target_repositories=None,
                     mode="NoForce"):
    registry, resource_group_name = validate_managed_registry(
        cmd.cli_ctx, registry_name, resource_group_name, IMPORT_NOT_SUPPORTED)

    client_registries = cf_acr_registries(cmd.cli_ctx)

    if image is not None:
        source_registry = image[:image.index(".")]
        resource_id = get_resource_id_by_registry_name(cmd.cli_ctx, source_registry)
        source_image = image[image.index("/") + 1 :]

    image_source = ImportSource(
        resource_id=resource_id, source_image=source_image)

    import_parameters = ImportImageParameters(source=image_source,
                                              target_tags=target_tags,
                                              untagged_target_repositories=untagged_target_repositories,
                                              mode=mode)

    image_imported = LongRunningOperation(cmd.cli_ctx)(client_registries.import_image(
        resource_group_name=resource_group_name,
        registry_name=registry_name,
        parameters=import_parameters))

    return image_imported
