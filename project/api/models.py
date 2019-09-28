from sqlalchemy.sql import func
from project import db

## Uma carta pode estra em varias mãos, nisso o que determina que uma mesma carta
## não caia para mais de 1 pessoa é o round

class Card(db.Model):
    id    = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    value = db.Column(db.String(2),  nullable=False)
    suit  = db.Column(db.String(10), nullable=False)
    # player_id = db.Column(db.Integer, db.ForeignKey('hand.player_id'))
    hands = db.relationship('Hand', backref='card', lazy=True)
    rounds = db.relationship('RoundCards', backref='card', lazy=True)

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit


class Hand(db.Model):
    id    = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer,  nullable=False, unique=True)
    sequence = db.relationship('Sequence', backref='hand', lazy=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))


    def __init__(self, card_id, player_id):
        self.player_id = player_id
        self.card_id = card_id


class Sequence(db.Model):
    id = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    win_order = db.Column(db.Integer)
    hand_id = db.Column(db.Integer, db.ForeignKey('hand.id'))
    round_id = db.Column(db.Integer, nullable=False)

    def __init__(self, hand_id, round_id):
        self.hand_id = hand_id
        self.round_id = round_id


class RoundCards(db.Model):
    round_id = db.Column(db.Integer,  primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)
  
    def __init__(self, round_id, card_id):
        self.round_id = round_id
        self.card_id = card_id