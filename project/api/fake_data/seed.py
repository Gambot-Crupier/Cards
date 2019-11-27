from project.api.models import Card

def seed_database(db):
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['D', 'S', 'H', 'C']

    for suit in suits:
        for value in values:
            card = Card(value, suit)
            db.session.add(card)

    db.session.commit()