"""
This script assigns a specified material to all static mesh assets within a directory that have a name similar 
to a selected mesh. It automates the process of applying materials across multiple meshes, helping to maintain 
consistent visual styles in an Unreal Engine project.

Usage:
    - Select a mesh and a material in the Unreal Editor.
    - Set the `WORKING_PATH` to the directory where the meshes are located.
    - Run the script within the Unreal Editor's Python environment.

Features:
    - Scans all static meshes in the specified directory.
    - Finds and applies the selected material to all meshes with a matching name.
    - Displays a progress dialog with the option to cancel the operation.
"""

from typing import List

import unreal

WORKING_PATH: str = "/Game/"


@unreal.uclass()
class EditorAssetLibrary(unreal.EditorAssetLibrary):
    """Subclass of Unreal's EditorAssetLibrary for custom asset operations."""
    pass


@unreal.uclass()
class EditorUtility(unreal.GlobalEditorUtilityBase):
    """Subclass of Unreal's GlobalEditorUtilityBase for utility operations."""
    pass


def assign_material_to_similar_named_meshes(working_path: str) -> None:
    """
    Assign a selected material to all static meshes with a similar name within the specified directory.

    Args:
        working_path (str): The directory path to search for static meshes.
    """
    editor_asset_lib = EditorAssetLibrary()
    editor_util = EditorUtility()

    selected_assets = editor_util.get_selected_assets()
    if len(selected_assets) < 2:
        unreal.log_error("Please select both a mesh and a material.")
        return

    selected_mesh = selected_assets[0]
    selected_material = selected_assets[1]

    selected_mesh_name = selected_mesh.get_name()
    selected_mesh_class = selected_mesh.get_class()

    all_assets: List[str] = editor_asset_lib.list_assets(working_path, recursive=True, include_folder=False)
    all_assets_count: int = len(all_assets)

    matching_meshes = [selected_mesh]

    with unreal.ScopedSlowTask(all_assets_count, f"Assigning material to meshes similar to {selected_mesh_name}") as slow_task:
        slow_task.make_dialog(True)

        for asset in all_assets:
            asset_data = editor_asset_lib.find_asset_data(asset)
            asset_name = asset_data.asset_name
            asset_class = asset_data.asset_class

            if asset_name == selected_mesh_name and asset != selected_mesh.get_path_name():
                if asset_class == selected_mesh_class:
                    matching_meshes.append(asset_data.get_asset())
                    unreal.log(f"Found matching mesh: {asset_name}")

            if slow_task.should_cancel():
                break

            slow_task.enter_progress_frame(1, asset_name)

    for mesh in matching_meshes:
        mesh.set_material(0, selected_material)
        unreal.log(f"Assigned material to mesh: {mesh.get_name()}")


def main() -> None:
    """Main function to execute the assignment of material to similar named meshes."""
    assign_material_to_similar_named_meshes(WORKING_PATH)


if __name__ == "__main__":
    main()
