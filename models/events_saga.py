from datetime import datetime

from sqlalchemy import Column, Integer, text, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app import db
from enums.type_operation import TypeOperation


class EventSaga(db.Model):
    __tablename__ = "events_saga"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_operation = Column(Enum(TypeOperation), nullable=False)
    snapshot_id = Column(UUID(as_uuid=True), nullable=True)
    eventHandler_id = Column(UUID(as_uuid=True), ForeignKey("events_handler.id"))
    event = relationship('EventHandler', back_populates='eventSaga')
    dttm_change = Column(DateTime(True), server_default=text("now()"))

    def __init__(self, type_operation, eventHandler_id):
        self.type_operation = type_operation
        self.eventHandler_id = eventHandler_id
        self.dttm_change = datetime.now()