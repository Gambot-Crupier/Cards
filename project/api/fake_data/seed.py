from project.api.models import Card

def seed_database(db):
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['d', 's', 'h', 'c']

    for suit in suits:
        for value in values:
            card = Card(value, suit)
            db.session.add(card)

    db.session.commit()