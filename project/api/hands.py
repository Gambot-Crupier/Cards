from flask import Blueprint, jsonify, request
from os.path import join, dirname, realpath
from requests.exceptions import HTTPError
from project.api.models import Hand, Card
from project import db
import json, sys


hands_blueprint = Blueprint('cards', __name__)


@hands_blueprint.route('/get_fake_hands', methods=['GET'])
def get_fake_hand():

    UPLOADS_PATH = join(dirname(realpath(__file__)), 'fake_data/hands.json')

    with open(UPLOADS_PATH, 'r') as f:
        hands_json = json.load(f)

    save_hands(hands_json)

    return jsonify({
        'hand': [
            { 'Sucess': 'full' }
        ] 
    })


@hands_blueprint.route("/post_hands", methods=["POST"])
def post_hands():
    try:
        hands_json = request.get_json()
        print(hands_json, file=sys.stderr)
    
        save_hands(hands_json)
    
    except HTTPError:
        return jsonify({"message": "NOT FOUND", "status_code": 404}), 404
    else:
        return jsonify({"message": "Hands Recived", "status_code": 200}), 200


def save_hands(hands_json):
    for hand in hands_json:
        player_id = hand['player_id']
        db.session.add(Hand(player_id=player_id))
        
        cards = hand['cards']
        for card in cards:
            value = card['value']
            suit = card['suit']
            db.session.add(Card(player_id=player_id, value=value, suit=suit))

        db.session.commit()