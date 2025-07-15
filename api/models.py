from sqlalchemy import Column, Integer, String, Date, Text, Float
from database import Base

class FctImageDetections(Base):
    __tablename__ = "fct_image_detections"
    message_id             = Column(Integer, primary_key=True, index=True)
    detected_object_class  = Column(String,  primary_key=True, index=True)
    confidence_score       = Column(Float)

class FctMessages(Base):
    __tablename__ = "fct_messages"
    id           = Column(Integer, primary_key=True, index=True)
    date         = Column(Date)
    text         = Column(Text)
    views        = Column(Integer)
    forwards     = Column(Integer)
    replies      = Column(Integer)
    channel_key  = Column("_channel", String)  # maps the DB column “_channel”
