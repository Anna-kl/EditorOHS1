from sqlalchemy import Column, Integer, text, String, DateTime, Enum, create_engine
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app import db
from enums.status import Status


class Classifier(db.Model):
    __tablename__ = "classifiers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    parent_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    fields = Column(String, nullable=False)
    attributes = Column(String, nullable=False)
    status = Column(Enum(Status), nullable=False)

    def __init__(self,  name, description, fields, attributes, status, parent_id):
        self.name = name
        self.fields = fields
        self.attributes = attributes
        self.parent_id = parent_id
        self.status = status
        self.description = description

    def check_attributes(self):
        return True