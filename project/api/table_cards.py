from flask import Blueprint, jsonify, request
from os.path import join, dirname, realpath
from requests.exceptions import HTTPError
from project.api.models import RoundCards, Card
from project import db
import json, sys


table_cards_blueprint = Blueprint('table_cards', __name__)


  
@table_cards_blueprint.route("/table_cards", methods=["POST"])
def post_table_cards():
    try:
        table_cards_json = request.get_json()
        
        save_table_cards(table_cards_json)
    
    except HTTPError:
        return jsonify({"message": "NOT FOUND", "status_code": 404}), 404
    else:
        return jsonify({"message": "Table Cards Recived", "status_code": 200}), 200
     
def save_table_cards(table_cards_json):
    for card in table_cards_json:
        round_id = card['round_id']
        print(round_id, file=sys.stderr)
        db.session.add(RoundCards(round_id))
        
    cards = card['cards']     
    for table_card in cards:
        value = table_card['value']
        suit = table_card['suit']
        
        card_value = Card.query.filter_by(value='value').first()
        card_suit = Card.query.filter_by(suit='suit').first()

        if value and suit is card_value and card_suit:
            card_id = Card.query.filter_by(id='id').first()
        
        else:
            return jsonify({"message": "Not match table cards."})      
        
        db.session.add(RoundCards(card_id=card_id))

    db.session.commit()
        
    