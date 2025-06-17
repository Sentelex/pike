import importlib
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
                # Convert file path to module path
                rel_path = os.path.relpath(
                    os.path.join(root, file), os.path.dirname(os.path.dirname(__file__))
                )
                # Construct the full module path including 'src'
                module_path = rel_path.replace(os.path.sep, ".").replace(".py", "")

                try:
                    # Import the module
                    module = importlib.import_module(f"src.{module_path}")

                    # Find all Skill subclasses in the module
                    for name, obj in inspect.getmembers(module):
                        if (
                            inspect.isclass(obj)
                            and issubclass(obj, sk.Skill)
                            and obj != sk.Skill
                        ):
                            # Create the singleton instance through the metaclass
                            skill = obj()
                            skills.append(skill)
                except ImportError as e:
                    print(f"Failed to import module {module_path}: {e}")
                except Exception as e:
                    print(f"Error loading field from {module_path}: {e}")

    return skills


if __name__ == "__main__":
    # Load all skills
    skills = load_skills()

    # Print information about each skill
    print("Skill list:\n\t{skills}")
    print("\nLoaded Skills:")
    print("=" * 80)
    for skill in skills:
        print(f"\nType: {type(skill)}")
        print(f"Name: {skill.name}")
        print(f"Description: {skill.description}")
        print(f"ID: {skill.id}")
        print("-" * 80)

# f2223d53-3459-560b-9fd5-7b4a765663a6 Action Item Extractor
# 006abd29-148e-5084-a176-cecf42518fe4 Stock Price Fetcher
# b63efdf8-ab6d-56e8-8076-fe378da379a6 Other File Parser
# 9ec92ca4-2a61-5b79-a4e7-46456f458ce5 PDF Parser
# 0cbcbbf6-b8b1-59e7-a3aa-44e2b8ed9f91 Webpage Parser
# 1d165e36-df74-5796-a333-72b400e15d18 Text Summarizer
