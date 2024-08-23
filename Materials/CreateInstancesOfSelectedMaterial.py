"""
This script automates the creation of multiple material instances from a selected base material in Unreal Engine.
It generates a specified number of material instances, naming them sequentially, and setting their parent to the selected material.

Usage:
    - Select a base material in the Unreal Editor.
    - Set the `TOTAL_REQUIRED_INSTANCES` variable to the number of instances you want to create.
    - Run the script within the Unreal Editor's Python environment.

Features:
    - Automatically generates material instances based on a selected base material.
    - Names instances sequentially and organizes them in the content browser.
    - Provides a basic template for batch-creating asset instances.
"""

import unreal

# Set the number of instances to create
TOTAL_REQUIRED_INSTANCES: int = 10


@unreal.uclass()
class EditorUtility(unreal.GlobalEditorUtilityBase):
    """Subclass of Unreal's GlobalEditorUtilityBase for custom utility operations."""
    pass


@unreal.uclass()
class MaterialEditingLibrary(unreal.MaterialEditingLibrary):
    """Subclass of Unreal's MaterialEditingLibrary for material editing operations."""
    pass


def create_material_instances(base_material: unreal.Material, instance_count: int) -> None:
    """
    Create a specified number of material instances from a selected base material.

    Args:
        base_material (unreal.Material): The base material from which instances will be created.
        instance_count (int): The number of material instances to create.
    """
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.MaterialInstanceConstantFactoryNew()

    base_material_name = base_material.get_name()
    base_material_path = base_material.get_path_name()
    created_assets_path = base_material_path.replace(base_material_name, "").rstrip(".")

    material_editing_lib = MaterialEditingLibrary()

    for i in range(instance_count):
        instance_name = f"{base_material_name}_inst_{i + 1}"
        instance_path = f"{created_assets_path}/{instance_name}"

        new_instance = asset_tools.create_asset(instance_name, created_assets_path, None, factory)
        material_editing_lib.set_material_instance_parent(new_instance, base_material)

        unreal.log(f"Created Material Instance: {instance_name} at {instance_path}")


def main() -> None:
    """Main function to execute the creation of material instances."""
    editor_util = EditorUtility()
    selected_assets = editor_util.get_selected_assets()

    if not selected_assets:
        unreal.log_error("No material selected. Please select a material.")
        return

    base_material = selected_assets[0]
    if not isinstance(base_material, unreal.Material):
        unreal.log_error("Selected asset is not a material. Please select a valid material.")
        return

    create_material_instances(base_material, TOTAL_REQUIRED_INSTANCES)


if __name__ == "__main__":
    main()
