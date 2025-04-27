import typing as t
import pydantic as pyd
import uuid as u
import enum

ID = t.NewType("ID", u.UUID)
ShortName = t.Annotated[str, pyd.constr(max_length=256)]
Description = t.Annotated[str, pyd.constr(max_length=2048)]

class AdditionalTypes(str, enum.Enum):
  string: 'str'
  float: 'float'
  int: 'int'
  bool: 'bool'
  enum: 'enum'

class ConfigArguments(pyd.BaseModel):
  name: ShortName
  data_type: AdditionalTypes
  value: str | float | int | bool | None # Enum will come back as a string and be type converted on back end
  constraints: Description # Non-negative, max_length, valid enum_list, etc..