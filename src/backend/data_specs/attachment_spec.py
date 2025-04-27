import typing as t
import pydantic as pyd
import enum

import base_types as base

AttachmentID = t.NewType("AttachmentID", base.ID)

class AttachmentType(str, enum.Enum):
  jpg = 'jpg',
  png = 'png',
  pdf = 'pdf',
  wav = 'wav',
  proxy = 'proxy'

class AttachmentTag(pyd.BaseModel):
  """
  Proxy tag to keep from passing full attachments back and forth without
  expicit request.
  """
  ID: AttachmentID
  name: base.ShortName
  type: AttachmentType

class Attachment(pyd.BaseModel):
  """
  Minimum container for shuttling attachment data back and forth between
  frontend and backend
  """
  tag: AttachmentTag
  data: bytearray 