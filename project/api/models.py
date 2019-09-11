from project import db


class Card(db.Model):
    __tablename__ = 'Card'
    id             = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    name           = db.Column(db.String(128),  nullable=False)


    def __init__(self, name):
        self.name     = name