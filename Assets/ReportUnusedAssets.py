"""
This script identifies and reports unused assets within a specified directory of an Unreal Engine project.
By scanning through all assets in the given path, the script determines which assets are not referenced 
by any other assets. Unused assets are then printed out, allowing developers and artists to clean up 
and optimize their projects by removing or archiving these unneeded files.

The script is designed to help manage project resources effectively, improving both the organization 
and performance of Unreal Engine projects.

Usage:
    - Adjust the `WORKING_PATH` variable to target the desired directory.
    - Run the script within the Unreal Editor's Python environment.
    - Review the output list of unused assets and decide on appropriate actions.

Features:
    - Recursively scans all assets within the specified directory.
    - Identifies assets with no dependencies or references.
    - Outputs the paths of unused assets for easy review and management.
"""

from typing import List

import unreal

WORKING_PATH: str = "/Game/"


@unreal.uclass()
class EditorAssetLibrary(unreal.EditorAssetLibrary):
    """Subclass of Unreal's EditorAssetLibrary for custom asset operations."""
    pass


def find_unused_assets(working_path: str) -> List[str]:
    """
    Find and return a list of assets that are not referenced by any other assets.

    Args:
        working_path (str): The directory path to search for assets.

    Returns:
        List[str]: A list of asset paths that have no references.
    """
    editor_asset_lib = EditorAssetLibrary()
    all_assets = editor_asset_lib.list_assets(working_path, recursive=True, include_folder=False)
    unused_assets = []

    for asset in all_assets:
        dependencies = editor_asset_lib.find_package_referencers_for_asset(asset, load_assets=False)
        if not dependencies:
            unused_assets.append(asset)
            print(f">>> {asset}")

    return unused_assets


def main() -> None:
    """
    Main function to execute the unused asset report.

    This function initiates the search for unused assets in the specified directory,
    prints out each unused asset, and returns the list for further processing.
    """
    find_unused_assets(WORKING_PATH)


if __name__ == "__main__":
    main()
