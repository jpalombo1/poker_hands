from poker.card import Card
from poker.common import Suits, Values
import random


def generate_deck() -> list[Card]:
    """Generate standard deck of 52 cards with suit and value."""
    deck = [
        Card(suit, value)
        for suit in Suits
        for value in Values
        if suit != Suits.NONE and value != Values.NONE
    ]
    random.shuffle(deck)
    return deck


def generate_hand(deck: list[Card], num_cards: int = 2) -> list[Card]:
    """Randomly get num_cards from deck to use as hand. No replacement."""
    deck_vals = random.sample(list(range(len(deck))), num_cards)
    return [card for idx, card in enumerate(deck) if idx in deck_vals]


def remove_from_deck(deck: list[Card], cards: list[Card]) -> list[Card]:
    """Remove list of cards from deck and return it. If not in the deck, jsut preserve deck as is."""
    for card in cards:
        try:
            index = deck.index(card)
        except ValueError:
            continue
        else:
            deck.pop(index)
    return deck
