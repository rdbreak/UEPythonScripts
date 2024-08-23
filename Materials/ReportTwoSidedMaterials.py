"""
This script scans all materials and material instances within a specified Unreal Engine project directory to report those
that have the "Two-Sided" property enabled. It is useful for optimizing performance by identifying materials that may 
be unnecessarily two-sided, which can impact rendering efficiency.

Usage:
    - Set the `WORKING_PATH` variable to the directory containing the materials you want to check.
    - Run the script within the Unreal Editor's Python environment.
    - Review the log output for details on which materials are two-sided.

Features:
    - Scans all materials and material instances within a specified directory.
    - Logs warnings for any materials or material instances with the "Two-Sided" property enabled.
    - Displays a progress dialog during the operation with the option to cancel.
"""

from typing import List

import unreal

WORKING_PATH: str = "/Game/"


@unreal.uclass()
class EditorAssetLibrary(unreal.EditorAssetLibrary):
    """Subclass of Unreal's EditorAssetLibrary for custom asset operations."""
    pass


def report_two_sided_materials(working_path: str) -> None:
    """
    Scan and report materials and material instances with the "Two-Sided" property enabled.

    Args:
        working_path (str): The directory path to search for materials.
    """
    editor_asset_lib = EditorAssetLibrary()
    all_assets: List[str] = editor_asset_lib.list_assets(working_path, recursive=True, include_folder=False)
    all_assets_count: int = len(all_assets)

    masters_with_two_sided: int = 0
    instances_with_two_sided: int = 0

    if all_assets_count > 0:
        with unreal.ScopedSlowTask(all_assets_count, "Scanning for two-sided materials") as slow_task:
            slow_task.make_dialog(True)

            for asset in all_assets:
                asset_data = editor_asset_lib.find_asset_data(asset)
                asset_name = asset_data.asset_name
                asset_class = asset_data.asset_class

                if asset_class == "Material":
                    if asset_data.get_asset().get_editor_property("two_sided"):
                        unreal.log_warning(f"Master material [{asset_name}] is TWO-SIDED")
                        masters_with_two_sided += 1
                    else:
                        unreal.log(f"Master material [{asset_name}] OK")
                elif asset_class in {"MaterialInstance", "MaterialInstanceConstant"}:
                    base_overrides = asset_data.get_asset().get_editor_property("base_property_overrides")
                    if base_overrides.get_editor_property("override_two_sided"):
                        unreal.log_warning(f"Material Instance [{asset_name}] is TWO-SIDED")
                        instances_with_two_sided += 1
                    else:
                        unreal.log(f"Material Instance [{asset_name}] OK")

                if slow_task.should_cancel():
                    break

                slow_task.enter_progress_frame(1, asset_name)

        unreal.log_warning(f"Found [{masters_with_two_sided}] Master Materials and [{instances_with_two_sided}] Material Instances with the Two-Sided flag enabled")


def main() -> None:
    """Main function to execute the report of two-sided materials."""
    report_two_sided_materials(WORKING_PATH)


if __name__ == "__main__":
    main()
