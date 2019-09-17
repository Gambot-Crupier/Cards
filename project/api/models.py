from sqlalchemy.sql import func
from project import db


class Card(db.Model):
    __tablename__ = 'Cards'
    id    = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    value = db.Column(db.String(1),  nullable=False)
    suit  = db.Column(db.String(10), nullable=False)


    def __init__(self, value, suit):
        self.value = value
        self.suit  = suit

    