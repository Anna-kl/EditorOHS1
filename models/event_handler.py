from datetime import datetime

from sqlalchemy import Column, Integer, text, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app import db
from enums.status_operation import STATUS_OPERATION


class EventHandler(db.Model):
    __tablename__ = "events_handler"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    event = relationship('Event', back_populates='eventHandler')
    object_id = Column(UUID(as_uuid=True), nullable=True)
    dttm_create = Column(DateTime(True), server_default=text("now()"))
    dttm_close = Column(DateTime(True), nullable=False)
    status = Column(Enum(STATUS_OPERATION), nullable=False)

    def __init__(self, event_id, object_id):
        self.status = STATUS_OPERATION.CREATE
        self.event_id = event_id
        self.dttm_create = datetime.now()
        self.object_id = object_id