from flask import Blueprint, jsonify, request
from os.path import join, dirname, realpath
from requests.exceptions import HTTPError
from project.api.models import Hand, Card
from project import db
import json, sys


hands_blueprint = Blueprint('card', __name__)


@hands_blueprint.route("/post_hands", methods=["POST"])
def post_hands():
    try:
        hands_json = request.get_json()
    
        for hand in hands_json:
            player_id = hand['player_id']
            round_id = hand['round_id']
            cards = hand['cards']
            
            for card in cards:
                value = card['value']
                suit = card['suit']

                card = Card.query.filter_by(value=value, suit=suit).first()
                db.session.add(Hand(player_id=player_id, card_id=card.id, round_id=round_id))

        db.session.commit()
    
    except HTTPError:
        return jsonify({"message": "NOT FOUND", "status_code": 404}), 404
    else:
        return jsonify({"message": "Hands Recived", "status_code": 200}), 200


@hands_blueprint.route("/get_hands", methods=["GET"])
def get_hands():
    try:
        round_id = request.args.get('round_id')
        round_hands = Hand.query.filter_by(round_id = round_id).all()

        response = {
            "round_id": round_id,
            "hands": []
        }

        player_ids_set = set([]) 
        for hand in round_hands:
            player_ids_set.add(hand.player_id)

        for player_id in list(player_ids_set):
            player_hands = Hand.query.filter_by(round_id = round_id, player_id=player_id).all()

            hand = {
                "player_id": player_id,
                "cards": []
            }

            for hand in player_hands:
                card = Card.query.filter_by(id=hand.card_id).first()
                
                hand['cards'].append({
                    "value": card.value,
                    "suit": card.suit
                })

            response['hands'].append(hand)

        print(response, file=sys.stderr)


        
    

        # db.session.commit()
    
    except HTTPError:
        return jsonify({"message": "NOT FOUND", "status_code": 404}), 404
    else:
        return jsonify({"message": "hands", "status_code": 200}), 200