from flask import Blueprint, jsonify, request
from os.path import join, dirname, realpath
from requests.exceptions import HTTPError
from project.api.models import Hand, Card, RoundCards
from project import db
import json
import sys
from treys import Evaluator, Card as EvaluatorCards
from project.api.modules.cards import get_player_hands, get_round_cards, get_round_winner, get_hands_score
import requests

hands_blueprint = Blueprint('card', __name__)


@hands_blueprint.route("/post_hands", methods=["POST"])
def post_hands():
    try:
        hands = request.get_json()
        # hands = hands_json['cards']

    
        for hand in hands:
            player_id = hand['player_id']
            round_id = hand['round_id']
            cards = hand['cards']
            
            for card in cards:
                # print('\n\naaaaaa', file=sys.stderr)
                value = card['value']
                suit = card['suit']

                # print(value, file=sys.stderr)
                # print(suit, file=sys.stderr)
                
                card = Card.query.filter_by(value=value, suit=suit).first()
                print(card, file=sys.stderr)
                
                db.session.add(Hand(player_id=player_id, card_id=card.id, round_id=round_id))

        db.session.commit()



        # Depois de mandar as mãos, deve-se começar o round!
        url = 'https://6wiv4418b6.execute-api.sa-east-1.amazonaws.com/production/start_round'

        try:
            start_round_request = requests.request("POST", url)

            if start_round_request.status_code is 200:
                return jsonify({ 'message': 'Mãos postadas e round começado!' })
            else:
                return jsonify({ 'message': 'Erro ao tentar começar round após postas as mãos.' }), 500

        except Exception as e:
            return jsonify({"error": "Erro ao tentar iniciar o round quando posta as mãos.", "message": str(e)}), 502


    except Exception as e:        
        return jsonify({"message": "Erro ao tentar receber as mãos.", "error": str(e)}), 500
        


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
        
    except Exception as e:
        return jsonify({"message": "Erro ao tentar recuperar as mãos dos usuários.", "error": str(e)}), 500



@hands_blueprint.route("/get_player_hand", methods=["GET"])
def get_player_hand():
    try:
        round_id = request.args.get('round_id')
        player_id = request.args.get('player_id')
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
        
    except Exception as e:
        return jsonify({"message": "Erro ao tentar recuperar a mão dos usuário.", "error": str(e) }), 500

@hands_blueprint.route("/get_round_cards_number", methods=["GET"])
def get_round_cards_number():
    try:
        round_id = request.args.get('round_id')

        round_cards = RoundCards.query.filter_by(round_id = round_id).all()
        
        if round_cards is not None:
            number_of_cards = len(round_cards)
        else:
            number_of_cards = 0

        return jsonify({
            'number': number_of_cards
        }), 200
    except Exception as e:
        return jsonify({
            'message': str(e)
        }), 400

@hands_blueprint.route("/get_winner", methods=["POST"])
def get_winner():
    parameters = request.get_json()
    player_list = parameters['players']
    round_id = parameters['round_id']

    evaluator = Evaluator()


    if player_list is not None:
        try:
            round_cards = get_round_cards(round_id)
            player_hands = get_player_hands(player_list, round_id)            
            player_hands_score = get_hands_score(player_hands, round_cards)
            winner = get_round_winner(player_hands_score)
         
            return jsonify({
                'player_id': winner['player_id']
            }), 200
        except Exception as e:
            return jsonify({
                'message': str(e)
            }), 400
    else:
        return jsonify({
            "message": "Não conseguiu pegar o vencedor"
        }),400
