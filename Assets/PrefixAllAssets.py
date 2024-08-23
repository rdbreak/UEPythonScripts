"""
This script automates the process of renaming Unreal Engine assets by adding a specific prefix
based on the asset type. It iterates over all assets within a specified directory, checks if the
asset name already contains the appropriate prefix, and if not, renames the asset accordingly.

The script is designed to work with various asset types, including materials, animations, textures,
and blueprints, among others. It uses the Unreal Python API to interact with assets within the
Unreal Engine editor, making it a powerful tool for organizing and managing large projects.

Key Features:
- Automatically detects the asset type and applies the correct prefix.
- Skips assets that already have the correct prefix to avoid redundant renaming.
- Integrates with Unreal Engine's ScopedSlowTask to provide a progress bar and allow for task cancellation.

This script is ideal for developers and artists who need to enforce naming conventions across
their Unreal Engine projects, ensuring consistency and easier asset management.

Usage:
- Place this script within your Unreal Engine project's script directory.
- Adjust the `WORKING_PATH` variable if necessary to target a different directory.
- Run the script within the Unreal Editor's Python environment.
"""

from typing import Dict, List

import unreal

# Define prefixes for different asset types
PREFIXES: Dict[str, str] = {
    "AnimBlueprint":    "animBP",
    "AnimSequence":     "anim",
    "Animation":        "anim",
    "BlendSpace1D":     "animBlnd",
    "Blueprint":        "bp",
    "CurveFloat":       "crvF",
    "CurveLinearColor": "crvL",
    "Material":         "mat",
    "MaterialFunction": "mat_func",
    "MaterialInstance": "mat_inst",
    "ParticleSystem":   "fx",
    "PhysicsAsset":     "phsx",
    "SkeletalMesh":     "sk",
    "Skeleton":         "skln",
    "SoundCue":         "cue",
    "SoundWave":        "wv",
    "StaticMesh":       "sm",
    "Texture2D":        "tex",
    "TextureCube":      "HDRI"
}

WORKING_PATH: str = "/Game/"


@unreal.uclass()
class GetEditorAssetLibrary(unreal.EditorAssetLibrary):
    """Subclass of Unreal's EditorAssetLibrary to allow custom asset operations."""
    pass


def get_proper_prefix(class_name: str) -> str:
    """Retrieve the appropriate prefix based on the asset class name.

    Args:
        class_name (str): The name of the asset class.

    Returns:
        str: The corresponding prefix for the asset class. Returns an empty string if no prefix is found.
    """
    return PREFIXES.get(class_name, "")


def main() -> None:
    """Main function to rename assets based on their class type by adding a prefix.

    This function iterates through all assets in the specified working path, checks if the asset name
    already contains the appropriate prefix, and if not, renames the asset by adding the correct prefix.
    """
    editor_asset_lib: GetEditorAssetLibrary = GetEditorAssetLibrary()
    all_assets: List[str] = editor_asset_lib.list_assets(WORKING_PATH, recursive=True, include_folder=False)
    all_assets_count: int = len(all_assets)

    with unreal.ScopedSlowTask(all_assets_count, "Processing assets") as slow_task:
        slow_task.make_dialog(True)

        for asset in all_assets:
            asset_data: unreal.AssetData = editor_asset_lib.find_asset_data(asset)
            asset_name: str = asset_data.asset_name
            asset_class_name: str = asset_data.asset_class
            asset_prefix: str = get_proper_prefix(asset_class_name)

            if asset_prefix and not asset_name.startswith(asset_prefix):
                new_asset_name: str = f"{asset_prefix}_{asset_name}"
                asset_path_name: str = asset_data.object_path
                asset_path_only: str = asset_data.package_path
                target_path_name: str = f"{asset_path_only}/{new_asset_name}.{new_asset_name}"

                editor_asset_lib.rename_asset(asset_path_name, target_path_name)
                print(f">>> Renaming [{asset_path_name}] to [{target_path_name}]")

            if slow_task.should_cancel():
                break
            slow_task.enter_progress_frame(1, asset_name)


if __name__ == "__main__":
    main()
