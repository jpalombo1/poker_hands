from enum import Enum


class Suits(Enum):
    """Card suits."""

    HEART = "♥"
    SPADE = "♠"
    CLUB = "♣"
    DIAMOND = "♦"
    NONE = ""


class Values(Enum):
    """Card values in order of worst to best."""

    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"
    NONE = ""


VALUE_MAP = {value: idx for idx, value in enumerate(Values)}


class CardsLeft(Enum):
    START = 5
    FLOP = 2
    TURN = 1
    RIVER = 0
