import src.models.skill as sk
import src.models.skill_loader as sl

AGENT_LOOKUP: dict[str, list[str]] | None
skill_set: list[sk.Skill] | None

if 'AGENT_LOOKUP' not in globals():
    AGENT_LOOKUP = None

if 'skill_set' not in globals():
    skill_set = None

def initialize_skills():
    """Initialize the skill set and load skills."""
    global skill_set
    if skill_set is None:
        skill_set = sl.load_skills()

def initialize_registry():
    """Initialize the skill registry and load skills."""
    global AGENT_LOOKUP
    if AGENT_LOOKUP is None:
        if skill_set is None:
            initialize_skills()
        AGENT_LOOKUP = {"default":[skill.name for skill in skill_set]}

initialize_registry()

for k, v in AGENT_LOOKUP.items():
    sk.Skill.store_collection(k, v)
