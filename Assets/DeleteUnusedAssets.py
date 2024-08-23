"""
This script automates the deletion of unused assets within a specified directory of an Unreal Engine project.
By scanning through all assets in the given path, the script identifies which assets are not referenced 
by any other assets. These unreferenced assets are then deleted, helping to clean up the project and 
reduce its size.

The script is designed for developers and artists who want to optimize their projects by removing 
unnecessary assets, improving project performance, and maintaining a clean workspace.

Usage:
    - Adjust the `WORKING_PATH` variable to target the desired directory.
    - Run the script within the Unreal Editor's Python environment.
    - Monitor the progress dialog to see which assets are being processed and deleted.

Features:
    - Recursively scans all assets within the specified directory.
    - Identifies assets with no dependencies or references.
    - Deletes unused assets to free up space and reduce project clutter.
    - Displays a progress dialog during the operation with the option to cancel.
"""

import unreal
from typing import List

WORKING_PATH: str = "/Game/"


@unreal.uclass()
class EditorAssetLibrary(unreal.EditorAssetLibrary):
    """Subclass of Unreal's EditorAssetLibrary for custom asset operations."""
    pass


def delete_unused_assets(working_path: str) -> None:
    """
    Find and delete assets that are not referenced by any other assets.

    Args:
        working_path (str): The directory path to search for assets.
    """
    editor_asset_lib = EditorAssetLibrary()
    all_assets: List[str] = editor_asset_lib.list_assets(working_path, recursive=True, include_folder=False)
    all_assets_count: int = len(all_assets)

    if all_assets_count > 0:
        with unreal.ScopedSlowTask(all_assets_count, "Deleting unused assets") as slow_task:
            slow_task.make_dialog(True)

            for asset in all_assets:
                dependencies = editor_asset_lib.find_package_referencers_for_asset(asset, load_assets=False)

                if not dependencies:
                    print(f">>> Deleting >>> {asset}")
                    editor_asset_lib.delete_asset(asset)

                if slow_task.should_cancel():
                    break

                slow_task.enter_progress_frame(1, asset)


def main():
    """
    Main function to execute the deletion of unused assets.

    This function initiates the search for unused assets in the specified directory,
    deletes each unused asset, and provides a progress dialog for user interaction.
    """
    delete_unused_assets(WORKING_PATH)


if __name__ == "__main__":
    main()
