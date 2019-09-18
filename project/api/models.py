from sqlalchemy.sql import func
from project import db




class Hand(db.Model):
    __tablename__ = 'Hands'
    id    = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer,  nullable=False)
    cards_list  = db.Column(db.String(10), nullable=False)
    hands = db.relationship('Card', backref='Hands', lazy=True)


    def __init__(self, value, suit):
        self.value = value
        self.suit  = suit

class Card(db.Model):
    __tablename__ = 'Cards'
    id    = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    value = db.Column(db.String(1),  nullable=False)
    suit  = db.Column(db.String(10), nullable=False)
    hand_id = db.Column(db.Integer, db.ForeignKey('Hands.id'), nullable=False)


    def __init__(self, value, suit):
        self.value = value
        self.suit  = suit