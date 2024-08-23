"""
This script identifies and unifies duplicate assets within a specified directory of an Unreal Engine project.
All duplicates of an asset are consolidated into a single asset, helping to reduce redundancy and maintain consistency.

Usage:
    - Set the `WORKING_PATH` to the directory containing assets you want to unify.
    - Run the script within the Unreal Editor's Python environment.

Features:
    - Recursively scans assets in a specified directory.
    - Identifies and consolidates duplicate assets.
    - Displays a progress dialog with the option to cancel the operation.
"""

from typing import List

import unreal

WORKING_PATH: str = "/Game/"


@unreal.uclass()
class EditorAssetLibrary(unreal.EditorAssetLibrary):
    """Subclass of Unreal's EditorAssetLibrary for custom asset operations."""
    pass


def unify_duplicates(working_path: str) -> None:
    """
    Find and unify duplicate assets within a specified directory.

    Args:
        working_path (str): The directory to search for assets.
    """
    editor_asset_lib = EditorAssetLibrary()
    all_assets: List[str] = editor_asset_lib.list_assets(working_path, recursive=True, include_folder=False)
    all_assets_count: int = len(all_assets)

    if all_assets_count > 0:
        with unreal.ScopedSlowTask(all_assets_count, "Unifying duplicate assets") as slow_task:
            slow_task.make_dialog(True)

            for process_asset in all_assets:
                process_asset_data = editor_asset_lib.find_asset_data(process_asset)
                process_asset_obj = process_asset_data.asset
                process_asset_name = process_asset_data.asset_name
                process_asset_path = process_asset_data.object_path

                matching_assets = [
                    editor_asset_lib.find_asset_data(asset).asset
                    for asset in all_assets
                    if editor_asset_lib.find_asset_data(asset).asset_name == process_asset_name and asset != process_asset_path
                ]

                if matching_assets:
                    editor_asset_lib.consolidate_assets(process_asset_obj, matching_assets)
                    print(f">>> Unifying process completed for {len(matching_assets)} assets")
                else:
                    print(">>> No duplicates found for the selected asset")

                if slow_task.should_cancel():
                    break

                slow_task.enter_progress_frame(1, process_asset_name)


def main() -> None:
    """Main function to execute the unification of duplicate assets."""
    unify_duplicates(WORKING_PATH)


if __name__ == "__main__":
    main()
