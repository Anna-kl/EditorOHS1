from sqlalchemy import Column, Integer, text, String, DateTime, Enum, create_engine
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app import db
from enums.type_of_struction import TypeOfObject
from enums.type_of_operation import TypeOfOperation


class Event(db.Model):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    parent_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    type = Column(Enum(TypeOfOperation), nullable=True)
    object = Column(Enum(TypeOfObject),  nullable=False)

    def __init__(self, name, description, parent_id, type, rule, attributes, object):
        self.name = name
        self.rule = rule
        self.attributes = attributes
        self.type = type
        self.parent_id = parent_id
        self.description = description

    @classmethod
    def get_event(cls, type_of_operation, type_of_object):
        return db.session.query(Event).filter(Event.type == type_of_operation).filter(
            Event.object == type_of_object).first()