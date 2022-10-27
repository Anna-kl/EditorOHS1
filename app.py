import json

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from database import database_url
import requests

from enums.type_of_struction import TypeOfStruct

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.classifier import Classifier
from models.armed_force import ArmedForce
from models.event import Event


@app.route('/', methods=['POST'])
def hello_world():
    data_from_request = request.get_json()

    data = json.loads(data_from_request['data_send'])
    data['parent_id'] = data['parent_id'] if 'parent_id' in data.keys() else None
    data['description'] = data['description'] if 'description' in data.keys() else None,
    classifier = Classifier(**data)
    # new_class = Classifier(attributes=data['attributes'],
    #                        description=data['description'] if len(data['description']) != 0 else None,
    #                        name=data['name'],
    #                        fields=data['fields'],
    #                        parent_id=data['parent_id'] if len(data['parent_id']) != 0 else None,
    #                        status=data['status'])
    db.session.add(classifier)
    db.session.commit()
    return jsonify({'message': 'registered', 'code': 201})

@app.route('/event', methods=['POST'])
def create_event():
    data_from_request = request.get_json()
    data_from_request['parent_id'] = data_from_request['parent_id'] if 'parent_id' in data_from_request.keys() else None
    data_from_request['type'] = data_from_request['type'] if 'type' in data_from_request.keys() else None
    data_from_request['attributes'] = data_from_request['attributes'] if 'attributes' in data_from_request.keys() else None
    event=Event(**data_from_request)
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'registered', 'code': 201})

# def handler_service_struct(classifier):


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
