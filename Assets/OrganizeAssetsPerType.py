"""
This script organizes assets within a specified directory of an Unreal Engine project by moving them into 
subdirectories based on their asset type. This helps in maintaining a clean and structured project hierarchy.

Usage:
    - Set the `WORKING_PATH` to the directory containing assets you want to organize.
    - Run the script within the Unreal Editor's Python environment.

Features:
    - Recursively scans assets in a specified directory.
    - Organizes assets by their type into corresponding subdirectories.
    - Displays a progress dialog with the option to cancel the operation.
"""

from typing import List

import unreal

WORKING_PATH: str = "/Game/"


@unreal.uclass()
class EditorAssetLibrary(unreal.EditorAssetLibrary):
    """Subclass of Unreal's EditorAssetLibrary for custom asset operations."""
    pass


def organize_assets_by_type(working_path: str) -> None:
    """
    Organize assets by their type into corresponding subdirectories.

    Args:
        working_path (str): The directory to search for assets.
    """
    editor_asset_lib = EditorAssetLibrary()
    all_assets: List[str] = editor_asset_lib.list_assets(working_path, recursive=True, include_folder=False)
    all_assets_count: int = len(all_assets)

    if all_assets_count > 0:
        with unreal.ScopedSlowTask(all_assets_count, "Organizing assets by type") as slow_task:
            slow_task.make_dialog(True)

            for asset in all_assets:
                asset_data = editor_asset_lib.find_asset_data(asset)
                asset_name = asset_data.asset_name
                asset_class_name = asset_data.asset_class
                target_path_name = f"/Game/{asset_class_name}/{asset_name}.{asset_name}"

                editor_asset_lib.rename_asset(asset_data.object_path, target_path_name)

                if slow_task.should_cancel():
                    break

                slow_task.enter_progress_frame(1, asset)


def main() -> None:
    """Main function to execute the organization of assets by type."""
    organize_assets_by_type(WORKING_PATH)


if __name__ == "__main__":
    main()
