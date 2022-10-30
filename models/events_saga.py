from datetime import datetime

from sqlalchemy import Column, Integer, text, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app import db
from enums.type_of_operation import TypeOfOperation
from enums.type_of_struction import TypeOfObject

from models.event_handler import EventHandler

class EventSaga(db.Model):
    __tablename__ = "events_saga"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_operation = Column(Enum(TypeOfOperation), nullable=False)
    type_of_object = Column(Enum(TypeOfObject), nullable=True)
    snapshot_id = Column(UUID(as_uuid=True), ForeignKey("snapshots.id"), nullable=True)
    eventHandler_id = Column(UUID(as_uuid=True), ForeignKey("events_handler.id"), nullable=True)
    # id конкретного объекта
    object_id = Column(UUID(as_uuid=True), nullable=False)
    dttm_change = Column(DateTime(True), server_default=text("now()"))

    def __init__(self, type_operation, type_of_object,  eventHandler_id, snapshot_id, object_id):
        self.type_operation = type_operation
        self.eventHandler_id = eventHandler_id
        self.dttm_change = datetime.now()
        self.snapshot_id = snapshot_id
        self.type_of_object = type_of_object
        self.object_id = object_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_history_event(cls, root, snapshot):
        return  db.session.query(EventSaga).join(EventHandler).filter(EventHandler.object_id == root.id) \
            .filter(EventSaga.dttm_change > snapshot.dttm_change).all()

    @classmethod
    def get_last_event_for_param(cls, root):
        return db.session.query(EventSaga).join(EventHandler).filter(EventHandler.object_id == root.id) \
           .filter(EventSaga.type_operation != TypeOfOperation.SNAPSHOT) \
           .order_by(desc(EventSaga.dttm_change)).all()

