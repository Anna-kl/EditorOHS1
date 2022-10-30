from sqlalchemy import Column, Integer, text, String, DateTime, create_engine, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app import db
from enums.status import Status


def get_root(object):
    if object.parent_id is not None:
        object = db.session.query(ArmedForce).filter(id == object.parent_id).first()
        if object:
            get_root(object)
    else:
        return object


class ArmedForce(db.Model):
    __tablename__ = "armed_force"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    parent_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    view_vf_id = Column(UUID(as_uuid=True), ForeignKey("classifiers.id"))
    status = Column(Enum(Status), nullable=False)

    def __init__(self, name, parent_id, view_vf_id, genus_vf_id, purpose_id, struction_vf_id, status):
        self.name = name
        self.status = status
        self.parent_id = parent_id
        self.purpose_id = purpose_id
        self.genus_vf_id = genus_vf_id
        self.view_vf_id = view_vf_id
        self.struction_vf_id = struction_vf_id

    def get_root(self):
        if self.parent_id is not None:
            object = db.session.query(Classifier).filter(Classifier.id == uuid.UUID(self.parent_id)).first()
            if object:
                return self.get_root(object)
        else:
            return self

