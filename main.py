#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 23:59:25 2018

@author: josephpalombo
"""
from poker.card import Card
from poker.deck import generate_deck, generate_hand, remove_from_deck
from poker.common import CardsLeft
from poker.evaluate import prob_win

NUM_PLAYERS = 5


def main():
    """."""
    deck = generate_deck()
    player_hands: list[list[Card]] = []
    for _ in range(NUM_PLAYERS):
        player_hand = generate_hand(deck)
        player_hands.append(player_hand)
        deck = remove_from_deck(deck, player_hand)
    prev_game_part = CardsLeft.START
    hand_finish_cards = len(player_hands[0])
    print(f"\nTURN: {prev_game_part.name}")
    player_str = "\n\tPlayer ".join(
        [str(idx) + ": " + str(hand) for idx, hand in enumerate(player_hands)]
    )
    print(f"\tPlayer {player_str}")
    print(f"\tDeck Cards: {len(deck)}")
    for game_part in [CardsLeft.FLOP, CardsLeft.TURN, CardsLeft.RIVER]:
        game_cards = prev_game_part.value - game_part.value
        hand_finish_cards += game_cards
        dealt_hand = generate_hand(deck, num_cards=game_cards)
        for player_hand in player_hands:
            player_hand += dealt_hand
        deck = remove_from_deck(deck, dealt_hand)
        win_probs = [
            prob_win(player_hands, deck, game_part, pnum) for pnum in range(NUM_PLAYERS)
        ]
        for player_hand in player_hands:
            player_hand = player_hand[:hand_finish_cards]
        prev_game_part = game_part
        print(f"\nTURN: {game_part.name}")
        player_str = "\n\tPlayer ".join(
            [str(idx) + ": " + str(hand) for idx, hand in enumerate(player_hands)]
        )
        print(f"\tPlayer {player_str}")
        print(f"\tDeck Cards: {len(deck)}")
        print(f"\tCards Dealt: {dealt_hand}")
        win_str = "% ".join(
            [f"{idx}. {int(wprob * 100):.2f}" for idx, wprob in enumerate(win_probs)]
        )
        print(f"\tWin Prob: {win_str}% Total: {int(sum(win_probs)* 100)}%")


if __name__ == "__main__":
    main()
