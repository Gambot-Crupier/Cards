from sqlalchemy.sql import func
from project import db


class Hand(db.Model):
    id    = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer,  nullable=False, unique=True)
    cards_list  = db.Column(db.String(10))
    hands = db.relationship('Card', backref='hand', lazy=True)

    def __init__(self, player_id):
        self.player_id = player_id

class Card(db.Model):
    id    = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    value = db.Column(db.String(2),  nullable=False)
    suit  = db.Column(db.String(10), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('hand.player_id'), nullable=False)

    def __init__(self, player_id, value, suit):
        self.player_id = player_id
        self.value = value
        self.suit  = suit