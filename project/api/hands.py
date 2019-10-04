from flask import Blueprint, jsonify, request
from os.path import join, dirname, realpath
from requests.exceptions import HTTPError
from project.api.models import Hand, Card
from project import db
import json
import sys

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

            response_hand = {
                "player_id": player_id,
                "cards": []
            }

            for hand in player_hands:
                card = Card.query.filter_by(id=hand.card_id).first()

                response_hand['cards'].append({
                    "value": card.value,
                    "suit": card.suit
                })

            response['hands'].append(response_hand)

        return json.dumps(response), 200
        
    except:
        return jsonify({"message": "Error on retriving round hands", "status_code": 404}), 404



@hands_blueprint.route("/get_player_hand", methods=["GET"])
def get_player_hand():
    try:
        round_id = request.args.get('round_id')
        player_id = request.args.get('round_id')
        hands = Hand.query.filter_by(round_id = round_id, player_id=player_id).all()

        response = {
            "round_id": round_id,
            "player_id": player_id, 
            "cards": [],
        }

        for hand in hands:
            card = Card.query.filter_by(id=hand.card_id).first()

            response['cards'].append({
                "value": card.value,
                "suit": card.suit
            })

        return json.dumps(response), 200
        
    except:
        return jsonify({"message": "Error on retriving round hands", "status_code": 404}), 404