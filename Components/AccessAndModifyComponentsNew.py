"""
This script accesses and modifies the components of selected actors within the Unreal Engine editor.
It specifically checks for StaticMeshComponents and resets their relative location to the origin.
This can be useful for batch-processing actors to ensure their components are properly aligned.

Usage:
    - Select the actors you want to modify in the Unreal Editor.
    - Run the script within the Unreal Editor's Python environment.
    - Review the output log for details on the modifications made.

Features:
    - Supports both inherited and non-inherited components.
    - Logs details of each actor and component processed.
    - Provides a basic template for accessing and modifying actor components.
"""

from typing import List

import unreal


@unreal.uclass()
class EditorUtility(unreal.GlobalEditorUtilityBase):
    """Subclass of Unreal's GlobalEditorUtilityBase for custom utility operations."""
    pass


def reset_static_mesh_component_locations(actors: List[unreal.Actor]) -> None:
    """
    Reset the relative location of all StaticMeshComponents attached to the selected actors' root components.

    Args:
        actors (List[unreal.Actor]): The list of selected actors to process.
    """
    for actor in actors:
        unreal.log(f"Processing actor: {actor.get_name()}")
        unreal.log("*************************************************")

        components = actor.root_component.get_children_components(include_all_descendants=True)
        component_count = len(components)
        unreal.log(f"Found [{component_count}] components attached to the root.")

        for component in components:
            component_name = component.get_name()
            component_class_name = component.get_class().get_name()

            unreal.log(f"Checking component [{component_name}] which is of type [{component_class_name}]")

            if component_class_name == "StaticMeshComponent":
                unreal.log(">> StaticMeshComponent detected.")
                original_location = component.get_relative_location()
                unreal.log(f"Original Location: {original_location}")

                component.set_relative_location(unreal.Vector(0.0, 0.0, 0.0), sweep=False, teleport=True)

                updated_location = component.get_relative_location()
                unreal.log(f"Updated Location: {updated_location}")
            else:
                unreal.log(">> Not a StaticMeshComponent.")


def main() -> None:
    """Main function to execute the reset of StaticMeshComponent locations for selected actors."""
    editor_util = EditorUtility()
    selected_actors = editor_util.get_selection_set()
    reset_static_mesh_component_locations(selected_actors)


if __name__ == "__main__":
    main()
