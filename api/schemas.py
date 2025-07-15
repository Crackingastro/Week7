from pydantic import BaseModel

class TopProduct(BaseModel):
    detected_object_class: str
    count: int

class ChannelFolderActivity(BaseModel):
    channel: str
    date_count: int
