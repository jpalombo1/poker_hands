#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 23:59:25 2018

@author: josephpalombo
"""
import random


# Get shuffled deck of 52 cards, suit and number
def generate_deck():
    deck = dict()
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    suits = ["hearts", "spade", "clubs", "diamonds"]
    card_order = [i for i in range(1, 53)]
    random.shuffle(card_order)
    num = 0
    for card in cards:
        for suit in suits:
            deck[card_order[num]] = [card, suit]
            num += 1
    return deck


# Get player hands, flop, turn, river by drawing randomly from deck
def generate_hand(deck, num_cards):
    hand = random.sample(deck.keys(), num_cards)
    player_hand = []
    for card in hand:
        player_hand.append(deck[card])
        deck.pop(card)
    return player_hand, deck


# Get nmerical ranking hand
def hand_eval(hand):

    num_values = []
    suit_values = []
    flush = False
    straight = False
    set4 = False
    set3 = False
    pair = False
    pair2 = False
    kicker = 0
    kicker2 = 0

    # Get numbers
    for card in hand:
        num_values.append(card_ranking[card[0]])

    # check numbers for straight
    num_values.sort()
    straight_run = 0
    for ind in range(len(num_values) - 1):
        if num_values[ind + 1] == num_values[ind] + 1:
            straight_run += 1
            if straight_run > 4:
                straight = True
                kicker = num_values[ind + 1]
        else:
            straight_run = 1

    # check for sets and pairs
    pair_count = 0
    for c in set(num_values):
        if num_values.count(c) == 4:
            set4 = True
            kicker = c
        elif num_values.count(c) == 3:
            set3 = True
            if pair:
                kicker2 = kicker
                kicker = c
            else:
                kicker = c
        elif num_values.count(c) == 2 and pair_count == 1:
            pair2 = True
            if c > kicker:
                kicker2 = kicker
                kicker = c
        elif num_values.count(c) == 2 and pair_count == 0:
            pair = True
            pair_count += 1
            if set3:
                kicker2 = c
            else:
                kicker = c
    # Check suits for flush
    for card in hand:
        suit_values.append(card[1])
    for f in set(suit_values):
        if suit_values.count(f) > 4:
            flush = True

    # Get hand based on conditions
    value = 0
    if flush and straight and kicker == 14:
        value = 9
    elif flush and straight:
        value = 8
    elif set4:
        value = 7
    elif set3 and pair:
        value = 6
    elif flush:
        value = 5
    elif straight:
        value = 4
    elif set3:
        value = 3
        kicker2 = num_values[-1]
    elif pair2:
        value = 2
    elif pair:
        value = 1
        kicker2 = num_values[-1]
    else:
        value = 0
        kicker = num_values[-1]
        kicker2 = num_values[-2]

    return [value, kicker, kicker2]


def head_to_head(p1_eval, p2_eval):
    if p1_eval[0] > p2_eval[0]:
        return 1
    if p1_eval[0] < p2_eval[0]:
        return 0
    else:
        if p1_eval[1] > p2_eval[1]:
            return 1
        if p1_eval[1] < p2_eval[1]:
            return 0
        else:
            if p1_eval[2] > p2_eval[2]:
                return 1
            if p1_eval[2] < p2_eval[2]:
                return 0
            else:
                return 0.5


def prob_win(p1_hand, p2_hand, deck, cards_left):
    p1_win = 0
    games = 0
    split = 0
    if cards_left == 0:
        p1_eval = hand_eval(p1_hand)
        p2_eval = hand_eval(p2_hand)
        p1_win = head_to_head(p1_eval, p2_eval)
        games += 1

    if cards_left == 1:
        for possible in deck:
            p1_hand += [deck[possible]]
            p2_hand += [deck[possible]]
            p1_eval = hand_eval(p1_hand)
            p2_eval = hand_eval(p2_hand)
            if head_to_head(p1_eval, p2_eval) != 0.5:
                p1_win += head_to_head(p1_eval, p2_eval)
            else:
                split += 1
            p1_hand = p1_hand[:-1]
            p2_hand = p2_hand[:-1]
            games += 1

    if cards_left == 2:
        for possible in deck:
            for possible2 in deck:
                p1_hand += [deck[possible]] + [deck[possible2]]
                p2_hand += [deck[possible]] + [deck[possible2]]
                p1_eval = hand_eval(p1_hand)
                p2_eval = hand_eval(p2_hand)
                if head_to_head(p1_eval, p2_eval) != 0.5:
                    p1_win += head_to_head(p1_eval, p2_eval)
                else:
                    split += 1
                p1_hand = p1_hand[:-2]
                p2_hand = p2_hand[:-2]
                games += 1

    if cards_left == 5:
        for possible in deck:
            for possible2 in deck:
                for possible3 in deck:
                    for possible4 in deck:
                        for possible5 in deck:
                            p1_hand += (
                                [deck[possible]]
                                + [deck[possible2]]
                                + [deck[possible3]]
                                + [deck[possible4]]
                                + [deck[possible5]]
                            )
                            p2_hand += (
                                [deck[possible]]
                                + [deck[possible2]]
                                + [deck[possible3]]
                                + [deck[possible4]]
                                + [deck[possible5]]
                            )
                            p1_eval = hand_eval(p1_hand)
                            p2_eval = hand_eval(p2_hand)
                            if head_to_head(p1_eval, p2_eval) != 0.5:
                                p1_win += head_to_head(p1_eval, p2_eval)
                            else:
                                split += 1
                            p1_hand = p1_hand[:-5]
                            p2_hand = p2_hand[:-5]

    return [p1_win / games * 100, (1 - p1_win / games) * 100, split / games * 100]


deck = generate_deck()
card_ranking = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}
# Dealt
(player1_hand, deck) = generate_hand(deck, 2)
(player2_hand, deck) = generate_hand(deck, 2)
print("P1:", player1_hand)
print("P2:", player2_hand)
# Flop
(flop, deck) = generate_hand(deck, 3)
player1_hand += flop
player2_hand += flop
print("Flop: ", flop)
win_probs = prob_win(player1_hand, player2_hand, deck, 2)
player1_hand = player1_hand[:-2]
player2_hand = player2_hand[:-2]
print("P1 win: {0}  %".format(int(win_probs[0] * 10) / 10))
print("P2 win: {0}  %".format(int(win_probs[1] * 10) / 10))
print("Split: {0}  %".format(int(win_probs[2] * 10) / 10))
# Turn
(turn, deck) = generate_hand(deck, 1)
player1_hand += turn
player2_hand += turn
print("Turn: ", turn)
win_probs = prob_win(player1_hand, player2_hand, deck, 1)
player1_hand = player1_hand[:-1]
player2_hand = player2_hand[:-1]
print("P1 win: {0}  %".format(int(win_probs[0] * 10) / 10))
print("P2 win: {0}  %".format(int(win_probs[1] * 10) / 10))
print("Split: {0}  %".format(int(win_probs[2] * 10) / 10))
# River
(river, deck) = generate_hand(deck, 1)
player1_hand += river
player2_hand += river
print("River: ", river)
win_probs = prob_win(player1_hand, player2_hand, deck, 0)
print("P1 win: {0}  %".format(int(win_probs[0] * 10) / 10))
print("P2 win: {0}  %".format(int(win_probs[1] * 10) / 10))
print("Split: {0}  %".format(int(win_probs[2] * 10) / 10))


# Final Chance
