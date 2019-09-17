from flask import Blueprint, jsonify

hands_blueprint = Blueprint('cards', __name__)

@hands_blueprint.route('/hand', methods=['GET'])
def get_hand():
    return jsonify({
        'hand': [
            { 'value': 'A', 'suit': 'diamond' },
            { 'value': '2', 'suit': 'club' },
            { 'value': '3', 'suit': 'heart' },
            { 'value': '4', 'suit': 'spade' },
        ] 
    })