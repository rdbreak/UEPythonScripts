"""
This script identifies and unifies duplicate assets based on user selection within an Unreal Engine project.
The script consolidates all duplicates of a selected asset into a single asset, ensuring consistency and reducing redundancy.

Usage:
    - Select an asset in the Unreal Editor that you want to check for duplicates.
    - Run the script within the Unreal Editor's Python environment.

Features:
    - Scans the entire project directory for duplicates of the selected asset.
    - Identifies and consolidates duplicate assets.
    - Displays a progress dialog with the option to cancel the operation.
"""

from typing import List

import unreal

WORKING_PATH: str = "/Game/"


@unreal.uclass()
class EditorUtil(unreal.GlobalEditorUtilityBase):
    """Subclass of Unreal's GlobalEditorUtilityBase for custom utility operations."""
    pass


@unreal.uclass()
class EditorAssetLibrary(unreal.EditorAssetLibrary):
    """Subclass of Unreal's EditorAssetLibrary for custom asset operations."""
    pass


def unify_selected_asset_duplicates(selected_asset: unreal.Object, working_path: str) -> None:
    """
    Unify duplicate assets of the selected asset within the specified directory.

    Args:
        selected_asset (unreal.Object): The asset selected by the user.
        working_path (str): The directory to search for duplicates.
    """
    editor_asset_lib = EditorAssetLibrary()
    selected_asset_name: str = selected_asset.get_name()
    selected_asset_path: str = selected_asset.get_path_name()

    all_assets: List[str] = editor_asset_lib.list_assets(working_path, recursive=True, include_folder=False)
    all_assets_count: int = len(all_assets)

    matching_assets: List[unreal.Object] = []

    with unreal.ScopedSlowTask(all_assets_count, selected_asset_path) as slow_task:
        slow_task.make_dialog(True)

        for asset in all_assets:
            asset_data = editor_asset_lib.find_asset_data(asset)
            asset_name = asset_data.get_asset().get_name()

            if asset_name == selected_asset_name and asset != selected_asset_path:
                unreal.log(f">>> Duplicate found for the asset {asset_name} located at {asset}")
                matching_assets.append(asset_data.get_asset())

            if slow_task.should_cancel():
                break

            slow_task.enter_progress_frame(1, asset_name)

    if matching_assets:
        editor_asset_lib.consolidate_assets(selected_asset, matching_assets)
        unreal.log(f">>> Unifying process completed for {len(matching_assets)} assets")
    else:
        unreal.log(">>> No duplicates found for the selected asset")


def main() -> None:
    """
    Main function to execute the unification of duplicates for the selected asset.
    """
    editor_util = EditorUtil()
    selected_assets = editor_util.get_selected_assets()

    if selected_assets:
        selected_asset = selected_assets[0]
        unify_selected_asset_duplicates(selected_asset, WORKING_PATH)
    else:
        unreal.log(">>> No asset selected. Please select an asset to check for duplicates.")


if __name__ == "__main__":
    main()
