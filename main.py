#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 23:59:25 2018

@author: josephpalombo
"""
from poker.deck import generate_deck, generate_hand, remove_from_deck
from poker.common import CardsLeft
from poker.evaluate import prob_win


def main():
    """."""
    deck = generate_deck()
    p1_hand = generate_hand(deck)
    deck = remove_from_deck(deck, p1_hand)
    p2_hand = generate_hand(deck)
    deck = remove_from_deck(deck, p2_hand)
    prev_game_part = CardsLeft.START
    hand_finish = 2
    for game_part in [CardsLeft.FLOP, CardsLeft.TURN, CardsLeft.RIVER]:
        print(f"\nTURN: {game_part.name}")
        print(f"\tP1 : {p1_hand}")
        print(f"\tP2 : {p2_hand}")
        print(f"\tDeck Cards: {len(deck)}")
        game_cards = prev_game_part.value - game_part.value
        hand_finish += game_cards
        dealt_hand = generate_hand(deck, num_cards=game_cards)
        p1_hand += dealt_hand
        p2_hand += dealt_hand
        deck = remove_from_deck(deck, dealt_hand)
        win_prob = prob_win(p1_hand, p2_hand, deck, game_part)
        prev_game_part = game_part
        print(f"\tCards Dealt: {dealt_hand}")
        print(f"\tP1 win: {win_prob * 100:.0f}%")
        p1_hand = p1_hand[:hand_finish]
        p2_hand = p2_hand[:hand_finish]


if __name__ == "__main__":
    main()
