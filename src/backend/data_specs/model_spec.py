import typing as t
import pydantic as pyd
import base_types as base

class Model(pyd.BaseModel):
  model_name: base.ShortName
  api_key: base.ShortName | None
  options: base.ConfigArguments