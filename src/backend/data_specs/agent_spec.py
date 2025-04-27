import typing as t
import pydantic as pyd

import base_types as base
import model_spec as mdl
import skill_spec as skill

AgentID = t.NewType("AgentID", base.ID)

class AgentTag(pyd.BaseModel):
    """
    Minimal identifying information for an agent when embedded.
    """

    ID: AgentID
    name: base.ShortName
    description: base.Description

class Agent(pyd.BaseModel):
    """
    Tag for identifying a unique agent.
    """
    tag: AgentTag
    model: mdl.Model
    skills: list[skill.SkillTag]
    options: base.ConfigArguments
    # use_count: pyd.NonNegativeInt = 0

class AgentMap(pyd.BaseModel):
    """
    Map of AgentIDs to the associated Agents.
    This map should always be 1:1
    """

    __root__: pyd.Dict[AgentID, Agent]

    def __init__(self, data: t.Iterable[Agent]):
        if isinstance(data, t.Iterable):
            super().__init__(
                __root__={agent.tag.ID: agent for agent in data}
            )
        else:
            raise TypeError(
                f"ERROR instantiating a {self.__class__.__name__}:\n"
                f"Expected an iterable of AgentInfo values, but got {type(data).__name__} instead."
            )
