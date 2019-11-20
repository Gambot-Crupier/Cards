from flask import Blueprint, jsonify, request
from os.path import join, dirname, realpath
from requests.exceptions import HTTPError
from project.api.models import Hand, Card, RoundCards
from project import db
import json
import sys
from treys import Evaluator, Card

def get_player_hand(player_list, round_id):
    player_hands = []

    for player in player_list:
        hands = Hand.query.filter_by(round_id = round_id, player_id=player['id']).all()
            
        player_hand = []
        for hand in hands:
            card = Card.query.filter_by(id=hand.card_id).first()
            player_hand.append(Card.new(card.value + card.suit))
            
        player_hands.append(player_hand)

    return player_hands

def get_round_cards(round_id):
    round_cards = []

    card_ids = RoundCards.query.filter_by(round_id = round_id).all()

    for card_id in card_ids:
        card = Card.query.filter_by(id=card_id.card_id).first()
        round_cards.append(Card.new(card.value + card.suit))
    
    return round_cards

