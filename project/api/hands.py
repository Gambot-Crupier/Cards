from os.path import join, dirname, realpath
from flask import Blueprint, jsonify, request
from requests.exceptions import HTTPError
import json, sys


hands_blueprint = Blueprint('cards', __name__)


@hands_blueprint.route('/get_fake_hands', methods=['GET'])
def get_fake_hand():

    UPLOADS_PATH = join(dirname(realpath(__file__)), 'fake_data/hands.json')

    with open(UPLOADS_PATH, 'r') as f:
        distros_dict = json.load(f)

    for distro in distros_dict:
        print(distro['player_id'], file=sys.stderr)

    save_hands()

    return jsonify({
        'hand': [
            { 'value': 'A', 'suit': 'diamond' },
            { 'value': '2', 'suit': 'club' },
            { 'value': '3', 'suit': 'heart' },
            { 'value': '4', 'suit': 'spade' },
        ] 
    })



@hands_blueprint.route("/post_hands", methods=["POST"])
def post_hands():
    try:
        data = request.get_json()
        print(data, file=sys.stderr)

    except HTTPError:
        return jsonify({"message": "NOT FOUND", "status_code": 404}), 404
    else:
        return jsonify({"message": "Hands Recived", "status_code": 200}), 200





def save_hands():
    return