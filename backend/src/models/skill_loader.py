import importlib as il
import inspect
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now we can import the skill module
import src.models.skill as sk


def load_skills() -> list[sk.Skill]:
    """
    Discover and instantiate all skills in the tools directory.
    Returns a list of all instantiated skill singletons.
    """
    tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
    skills: list[sk.Skill] = []

    # Walk through the tools directory
    for root, _, files in os.walk(tools_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                # Convert file path to module paths for import
                rel_path = os.path.relpath(
                    os.path.join(root, file), os.path.dirname(os.path.dirname(__file__))
                )
                module_path = rel_path.replace(os.path.sep, ".").replace(".py", "")

                try:
                    module = il.import_module(f"src.{module_path}")

                    # Find all Skill subclasses in the module and instantiate singletons
                    for name, obj in inspect.getmembers(module):
                        if (
                            inspect.isclass(obj)
                            and issubclass(obj, sk.Skill)
                            and obj != sk.Skill
                        ):
                            skills.append(obj())
                except ImportError as e:
                    print(f"Failed to import module {module_path}: {e}")
                except Exception as e:
                    print(f"Error loading field from {module_path}: {e}")

    return skills


if __name__ == "__main__":
    SRC_PATH = il.resources.files("src")
    TOOLS_PATH = os.path.join(SRC_PATH, "tools")
    files = [entry for entry in os.listdir(TOOLS_PATH) if os.path.isfile(os.path.join(TOOLS_PATH, entry)) 
             and entry.endswith(".py") and not entry.startswith("__")]
    # Load all skills
    skills = load_skills()

    # Print information about each skill
    print(f"\nLoaded Skills: {len(skills)} (of {len(files)} expected.)")
    print("=" * 80)
    for index, skill in enumerate(skills):
        print(f"Skill {index + 1} of {len(skills)} ({len(files)} expected):")
        print(f"Type: {type(skill)}")
        print(f"Name: {skill.name}")
        print(f"Description: {skill.description}")
        print(f"ID: {skill.id}")
        print("-" * 80)

