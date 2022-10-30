import json

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from database import database_url
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.classifier import Classifier, Tree
from models.event import Event
from enums.type_of_operation import TypeOfOperation
from enums.type_of_struction import TypeOfObject
from models.event_handler import EventHandler
from models.events_saga import EventSaga
from models.snapshot import Snapshot
from models.armed_force import ArmedForce

from services.create_event import ServicesEvent
from services.services_load import ServicesLoad

@app.route('/object', methods=['POST'])
def add_object():
    data_from_request = request.get_json()
    service_event = ServicesEvent(data_from_request)
    if service_event.error:
        return jsonify({'message': service_event.error_message, 'code': 201})

    return jsonify({'message':service_event.message, 'code': 201})


@app.route('/load-data', methods=['GET'])
def load_from_snapshot():
    services = ServicesLoad(request.args)
    # args = request.args
    # snapshot =
    # if snapshot.type_of_object == TypeOfObject.CLASSIFIER:
    #     snapshot_data = Classifier.load_from_snapshot(snapshot.data)
    # last_event = db.session.query(EventSaga).filter(EventSaga.type_of_object == TypeOfObject[args['type_of_object']])\
    #     .filter(EventSaga.dttm_change > snapshot.dttm_change).order_by(EventSaga.dttm_change).all()
    # index = 0
    step = int(args['step'])
    for event in last_event:
        if index<len(last_event) - step:
            if args['type_of_object'] == TypeOfObject.CLASSIFIER.name:
                object = Classifier.get_from_id(event.object_id)
                snapshot_data.insert_root(snapshot_data, object)
    snapshot_data.print(snapshot_data, '')

    return jsonify({'message': snapshot_data, 'code': 201})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
