from flask import Blueprint, jsonify, request
from os.path import join, dirname, realpath
from requests.exceptions import HTTPError
from project.api.models import RoundCards, Card
from project import db
import json, sys


table_cards_blueprint = Blueprint('table_cards', __name__)


@table_cards_blueprint.route('/get_table_cards', methods=['GET'])
def get_table_cards():
    try:
        round_id = request.args.get('round_id')
        table_cards = RoundCards.query.filter_by(round_id = round_id).all()
        
        response = {
            "round_id": round_id,
            "cards": [],
        }  
        for cards in table_cards:
                card = Card.query.filter_by(id=cards.card_id).first()
                
                response['cards'].append({
                    "value": card.value,
                    "suit": card.suit
                })

        return json.dumps(response), 200
        
    except:
        return jsonify({"message": "Error on retriving round hands"}), 404
  



@table_cards_blueprint.route("/post_table_cards", methods=["POST"])
def post_table_cards():
    try:
        table_cards_json = request.get_json()
        round_id = table_cards_json['round_id']
        cards = table_cards_json['cards']

        for table_card in cards:
            value = table_card['value']
            suit = table_card['suit']

            card = Card.query.filter_by(value=value, suit=suit).first()

            db.session.add(RoundCards(round_id=round_id, card_id=card.id))
                
        db.session.commit()

        return jsonify({"message": "Table Cards Recived"}), 200
    
    except Exception as e:
        return jsonify({ "error": str(e), "message": "Erro ao receber as cartas!" }), 500
        
