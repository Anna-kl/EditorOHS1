from sqlalchemy import Column, Integer, text, String, DateTime, Enum, create_engine
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
import json
from app import db
from enums.status import Status

from enums.type_of_operation import TypeOfOperation
def check_attributes():
    return True

class Tree:
    root = None
    children = []

    def __init__(self, root, comment=None):
        if isinstance(root, dict) is False:
            self.root = {
                'id': str(root.id),
            'name': root.name,
            'description': root.description,
            'parent_id': str(root.parent_id),
            'status': root.status.name
            }
        else:
            self.root = root['root']
        self.children = []
        if comment is not None:
            self.comment = comment

    @staticmethod
    def insert_root(root, record):
        if record.parent_id == uuid.UUID(root.root['id']):
            root.children.append(Tree(record, TypeOfOperation.ADD.name))
        else:
            if len(root.children) != 0:
                list(map(lambda x: Tree.insert_root(x, record), root.children))

        return root

    @staticmethod
    def print(root, separator):
        print('{}{}  {} \n'.format(separator, root.root['name'], root.comment if 'comment' in root.__dict__.keys() else None))
        if len(root.children) !=0:
            separator += '->'
            list(map(lambda x: Tree.print(x, separator),root.children))


class Classifier(db.Model):
    __tablename__ = "classifiers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    parent_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(Enum(Status), nullable=False)

    def __init__(self,  name, description,  status, parent_id):
        self.name = name
        self.parent_id = parent_id
        self.status = status
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def get_root(object):
        if object.parent_id is not None:
            object = db.session.query(Classifier).filter(Classifier.id == object.parent_id).first()
            if object:
                return object.get_root(object)
        else:
            return object

    def get_tree(self, root):
        trees = db.session.query(Classifier).filter(Classifier.parent_id == root.root['id']).all()
        if len(trees) == 0:
            return json.dumps(root.__dict__,  sort_keys=False,
                   indent=4,
                   ensure_ascii=False,
                    separators=(',', ': '))
        else:
            for tr in trees:
                tr_root = Tree(tr)
                root.children.append(self.get_tree(tr_root))
        return json.dumps(root.__dict__,   sort_keys=False,
                   indent=4,
                   ensure_ascii=False,
                   separators=(',', ': '))

    @staticmethod
    def check_insert_root(record, root):
        root = db.session.query(Classifier).filter(Classifier.id == root.parent_id).first()
        if root.id == record.id:
            return False
        else:
            if root is None:
                return True
        Classifier.check_insert_root(record, root)

    def check_duplicate(self):
        test = db.session.query(Classifier).filter(Classifier.parent_id == self.parent_id).filter(Classifier.name == self.name).first()
        if db.session.query(Classifier).filter(Classifier.parent_id == self.parent_id).filter(Classifier.name == self.name).first():
            return True
        return False

    @classmethod
    def get_from_id(cls, id):
        return db.session.query(Classifier).filter(Classifier.id == id).first()

    @staticmethod
    def load_from_snapshot(data):
        root = json.loads(data)
        tree = Tree(root)
        if len(root['children']) != 0:
            tree.children = list(map(lambda x: json.loads(x), root['children']))
        return tree