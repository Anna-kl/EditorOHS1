from sqlalchemy import Column, Integer, text, String, DateTime, create_engine, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app import db
from enums.status import Status


class ArmedForce(db.Model):
    __tablename__ = "armed_force"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    parent_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    view_vf_id = Column(UUID(as_uuid=True), ForeignKey("classifiers.id"))
    genus_vf_id = Column(UUID(as_uuid=True), ForeignKey("classifiers.id"))
    purpose_id = Column(UUID(as_uuid=True), ForeignKey("classifiers.id"))
    struction_vf_id = Column(UUID(as_uuid=True), ForeignKey("classifiers.id"))
    status = Column(Enum(Status), nullable=False)