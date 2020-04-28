# api/models.py
from api.main import db

class SignaturesHistory(db.Model):
    """This class represents the hisotry of successful token signature comsumptions for a user."""
    __tablename__ = 'signature_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    token_id = db.Column(db.String)
    signature = db.Column(db.String)

    def __init__(self, user_id, token_id, signature):
        self.user_id = user_id
        self.token_id = token_id
        self.signature = signature

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return SignaturesHistory.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Signatures of: {}>".format(self.user_id)