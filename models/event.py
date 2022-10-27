from sqlalchemy import Column, Integer, text, String, DateTime, Enum, create_engine
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app import db
from enums.type_of_struction import TypeOfStruct
from enums.type_operation import TypeOperation


class Event(db.Model):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    parent_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    type = Column(Enum(TypeOperation), nullable=True)
    rule = Column(String, nullable=False)
    attributes = Column(String, nullable=True)

    def __init__(self, name, description, parent_id, type, rule, attributes):
        self.name = name
        self.rule = rule
        self.attributes = attributes
        self.type = type
        self.parent_id = parent_id
        self.description = description
