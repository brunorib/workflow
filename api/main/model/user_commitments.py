# api/models.py
import json
from api.main import db

class UserCommitments(db.Model):
    """This class represents the commitments for a user."""
    __tablename__ = 'commitments'

    user_id = db.Column(db.Integer, primary_key=True)
    commitments = db.Column(db.JSON)

    def __init__(self, user_id, commitments):
        self.user_id = user_id
        self.commitments = json.dumps(commitments)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return UserCommitments.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Commmitments of: {}>".format(self.user_id)