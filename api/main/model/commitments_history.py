# api/models.py
import json
import hashlib
from api.main import db

class CommitmentsHistory(db.Model):
    """This class represents the hisotry of successful commitments for a user."""
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    commitments = db.Column(db.JSON)
    com_hash = db.Column(db.String)

    def __init__(self, user_id, commitments):
        self.user_id = user_id
        self.commitments = json.dumps(commitments)
        self.com_hash = self.get_hash(commitments)

    def get_commitments(self):
        return json.loads(self.commitments)

    def get_hash(self, commitments):
        str_to_be_hash = commitments[0]
        for com in commitments[1:]:
            str_to_be_hash += "|" + com
        m = hashlib.sha256()
        m.update(str_to_be_hash.encode('utf-8'))
        return m.hexdigest()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return CommitmentsHistory.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Commmitments of: {}>".format(self.user_id)