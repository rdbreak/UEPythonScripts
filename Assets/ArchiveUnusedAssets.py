"""
This script automates the process of archiving unused assets within a specified directory of an Unreal Engine project.
Unused assets are identified as those without any references, and these are moved to an archive directory to keep the 
project organized and reduce clutter.

Usage:
    - Set the `WORKING_PATH` to the directory containing assets you want to check.
    - Set the `ARCHIVE_PATH` to the directory where you want to move unused assets.
    - Run the script within the Unreal Editor's Python environment.

Features:
    - Recursively scans assets in a specified directory.
    - Identifies and moves unused assets to an archive location.
    - Provides a progress dialog with the option to cancel the operation.
"""

from typing import List

import unreal

WORKING_PATH: str = "/Game/"
ARCHIVE_PATH: str = "/Game/_ARCHIVE/"


@unreal.uclass()
class EditorAssetLibrary(unreal.EditorAssetLibrary):
    """Subclass of Unreal's EditorAssetLibrary for custom asset operations."""
    pass


def archive_unused_assets(working_path: str, archive_path: str) -> None:
    """
    Find and move unused assets to an archive directory.

    Args:
        working_path (str): The directory to search for assets.
        archive_path (str): The directory to move unused assets to.
    """
    editor_asset_lib = EditorAssetLibrary()
    all_assets: List[str] = editor_asset_lib.list_assets(working_path, recursive=True, include_folder=False)
    all_assets_count: int = len(all_assets)

    if all_assets_count > 0:
        with unreal.ScopedSlowTask(all_assets_count, "Archiving unused assets") as slow_task:
            slow_task.make_dialog(True)

            for asset in all_assets:
                dependencies = editor_asset_lib.find_package_referencers_for_asset(asset, load_assets=False)

                if not dependencies:
                    unreal.log(f">>> Archiving >>> {asset}")

                    asset_data = editor_asset_lib.find_asset_data(asset)
                    asset_name = asset_data.asset_name
                    target_path_name = f"{archive_path}{asset_name}.{asset_name}"

                    editor_asset_lib.rename_asset(asset_data.object_path, target_path_name)
                    unreal.log(f">>> The asset original name [{asset_data.object_path}] and new is [{target_path_name}]")

                if slow_task.should_cancel():
                    break

                slow_task.enter_progress_frame(1, asset)


def main() -> None:
    """Main function to execute the archiving of unused assets."""
    archive_unused_assets(WORKING_PATH, ARCHIVE_PATH)


if __name__ == "__main__":
    main()
