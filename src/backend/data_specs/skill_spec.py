import typing as t
import pydantic as pyd

import base_types as base
import model_spec as mdl

SkillID = t.NewType("SkillID", base.ID)

class SkillTag(pyd.BaseModel):
  """
  Tag for minimal information for identifying a skill within an agent.
  """

  ID: SkillID
  name: base.ShortName
  description: base.Description
 
class Skill(pyd.BaseModel):
  """
  Tag for identifying a skill used within an agent.
  """
  tag : SkillTag 
  model: mdl.Model | None
  #use_count: pyd.NonNegativeInt = 0
