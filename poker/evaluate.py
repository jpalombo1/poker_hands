from poker.card import Card
from poker.common import Suits, Values, VALUE_MAP, CardsLeft
from itertools import combinations


def get_straight(input_hand: list[Card], num_consecutive: int = 5) -> list[list[Card]]:
    """Check if there is a straight in your hand.

    Sort first to easily check incrementing. Use set so unique values only in straight increment.
    Keep addign to straight indexes if current value one more than previous. Else reset straight by adding current index, set previous value.
    If straight count exceed consecutive minimum, collect last num_consective cards of straight in hand to form a straight (e.g 6 cards, use highest 5).
    """
    hand = [card for card in input_hand]
    hand.sort(key=lambda card: VALUE_MAP[card.value])
    straights = []
    straight_count = [0]
    prev_value = -100
    for idx, card in enumerate(hand):
        value = VALUE_MAP[card.value]
        if value == prev_value:
            straight_count[-1] = idx
        elif value == prev_value + 1:
            straight_count.append(idx)
        else:
            straight_count = [idx]
        prev_value = value

        if len(straight_count) >= num_consecutive:
            straights.append(
                [hand[s_idx] for s_idx in straight_count[-1 * num_consecutive :]]
            )

    return straights


def get_flush(hand: list[Card], num_needed: int = 5) -> list[list[Card]]:
    """Check flush by counting how many cards have given suit in hand for all suits. Empty value will equate all cards of suit value independent."""
    flushes = []
    for suit in Suits:
        if suit == Suits.NONE:
            continue
        suit_count = hand.count(Card(suit, Values.NONE))
        if suit_count >= num_needed:
            flushes.append([card for card in hand if card.suit == suit])
    return flushes


def get_kind(hand: list[Card], num_kind: int = 2) -> list[list[Card]]:
    """Check for same value cards: pairs, sets, 4 of kind depending on num_kind set to."""
    kinds = []
    values = [VALUE_MAP[card.value] for card in hand]
    for unique_val in set(values):
        if values.count(unique_val) == num_kind:
            kinds.append([card for card in hand if VALUE_MAP[card.value] == unique_val])
    return kinds


def _card_kickers(hands: list[list[Card]]) -> list[Card]:
    """Get highest card of sets of cards as card kickers, then order for given kickers."""
    top_cards = [hand[0] for hand in hands]
    top_cards.sort(key=lambda card: VALUE_MAP[card.value], reverse=True)
    return top_cards


def _leftover_kicker(full_hand: list[Card], use_hand: list[Card]) -> list[Card]:
    """Get other cards not part of used hands that would act as a kicker, just rest of cards."""
    unused_cards = [card for card in full_hand if card not in use_hand]
    unused_cards.sort(key=lambda card: VALUE_MAP[card.value], reverse=True)
    return unused_cards


def get_kickers(hand: list[Card]) -> list[Card]:
    """Get kicker card for hand or non used card in hand to determine ties.

    For 5 card straight/flush or high card return high card(s) of values.
    For kind 4,3 return kicker value of set, then leftover highest cards.
    For pairs, get max 2 pairs, 2 kicker values of pair(s), the leftover high cards.
    Calculate number of kicker left to use in 5 card hand depending on cards played already (e.g 3 kind uses 2 leftover kicker,s 2 pair uses 5 - 2*2 or 1 left)
    """
    flushes = get_flush(hand)
    if len(flushes) > 0:
        return _card_kickers(flushes)
    straights = get_straight(hand)
    if len(straights) > 0:
        return _card_kickers(straights)
    four_kind = get_kind(hand, num_kind=4)
    if len(four_kind) > 0:
        num_left = 1
        return (
            _card_kickers(four_kind) + _leftover_kicker(hand, four_kind[0])[:num_left]
        )
    three_kind = get_kind(hand, num_kind=3)
    if len(three_kind) > 0:
        num_left = 2
        return (
            _card_kickers(three_kind) + _leftover_kicker(hand, three_kind[0])[:num_left]
        )
    pairs = get_kind(hand, num_kind=2)
    if len(pairs) > 0:
        pair_suits = _card_kickers(pairs)
        pair_use = [
            pair
            for pair in pairs
            for pair_kicker in pair_suits[:2]
            if pair_kicker in pair
        ]
        num_left = 5 - 2 * len(pairs)
        use_hand = sum(pair_use, [])
        return _card_kickers(pair_use) + _leftover_kicker(hand, use_hand)[:num_left]
    return _card_kickers([hand])


def get_score(hand: list[Card]) -> int:
    """Get score based on hands made, kicker from it.

    Straight / royal flush worth the most
    """
    flushes = get_flush(hand)
    straights = get_straight(hand)
    four_kind = get_kind(hand, num_kind=4)
    three_kind = get_kind(hand, num_kind=3)
    pairs = get_kind(hand, num_kind=2)
    kickers = get_kickers(hand)
    if len(flushes) > 0 and len(straights) > 0 and kickers[0].value == Values.ACE:
        return 9
    if len(flushes) > 0 and len(straights) > 0:
        return 8
    if len(four_kind) > 0:
        return 7
    if len(three_kind) > 0 and len(pairs) > 0:
        return 6
    if len(flushes) > 0:
        return 5
    if len(straights) > 0:
        return 4
    if len(three_kind) > 0:
        return 3
    if len(pairs) > 1:
        return 2
    if len(pairs) > 0:
        return 1

    return 0


def head_to_head(input_player_hands: list[list[Card]], player_number: int = 0) -> float:
    """Evaluate specified player vs other players hand.

    Get scores and if still tied (both have pairs, etc.) compare kickers until a winner if not then a tie.
    """
    player_hands = [p_hand for p_hand in input_player_hands]
    p_focus_hand = player_hands[player_number]
    p_score = get_score(p_focus_hand)
    player_hands.pop(player_number)
    other_scores = [get_score(p_hand) for p_hand in player_hands]

    if all(p_score > o_score for o_score in other_scores):
        return 1.0
    if any(p_score < o_score for o_score in other_scores):
        return 0.0

    p_kicker = get_kickers(p_focus_hand)
    tie_players = [
        p_hand
        for idx, p_hand in enumerate(player_hands)
        if other_scores[idx] == p_score
    ]
    for pidx, pkick in enumerate(p_kicker):
        other_kickers = [get_kickers(p_hand)[: len(p_kicker)] for p_hand in tie_players]
        p_score = VALUE_MAP[pkick.value]
        other_scores = [
            VALUE_MAP[okick[pidx].value] for okick in other_kickers if len(okick) > pidx
        ]
        if len(other_scores) == 0:
            return 1.0 / len(tie_players)
        if all(p_score > o_score for o_score in other_scores):
            return 1.0
        if any(p_score < o_score for o_score in other_scores):
            return 0.0
        print(tie_players)
        print(other_scores)
        tie_players = [
            p_hand
            for idx, p_hand in enumerate(tie_players)
            if other_scores[idx] == p_score
        ]

    return 1.0 / len(other_kickers)


def prob_win(
    player_hands: list[Card],
    deck: list[Card],
    cards_left: CardsLeft,
    player_number: int = 0,
) -> float:
    """Probability of winning from 0 to 1. depending on hand for specified player.

    Find all the combinations of cards possible given the deck and number of cards needed.
    Then give each possible combo of cards to each player, calculate who wins.
    Probabilitiy of win for player 1 is # hands won/ total possible hands.
    """
    p_win: float = 0.0
    games: int = 0
    if cards_left == CardsLeft.RIVER:
        return head_to_head(player_hands, player_number)

    all_cards = combinations(deck, cards_left.value)
    hand_length = len(player_hands[player_number])
    for possible_cards in all_cards:
        player_hands = [
            player_hand + list(possible_cards) for player_hand in player_hands
        ]
        p_win += head_to_head(player_hands, player_number)
        player_hands = [player_hand[:hand_length] for player_hand in player_hands]
        games += 1

    return p_win / games
