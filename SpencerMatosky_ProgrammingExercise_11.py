"""
poker_draw.py

A simple five-card draw poker game. The program shuffles a Deck, deals
the player a hand of five cards, and then asks which cards to replace
(for example: 1, 3, 5). The chosen cards are replaced with new cards
from the deck, and the program prints which cards were replaced and the
final hand. 
"""

import random
import re
import sys

# Number of cards in a poker hand
HAND_SIZE = 5

# Ranks and suits used to build a standard 52-card deck
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
         "Jack", "Queen", "King", "Ace"]
SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]


class Card:
    """
    A single playing card.

    Attributes:
        rank (str): the card's rank, such as "7" or "Queen".
        suit (str): the card's suit, such as "Hearts".
    """

    def __init__(self, rank, suit):
        """
        Create a card.

        Args:
            rank (str): the card's rank.
            suit (str): the card's suit.
        """
        self.rank = rank
        self.suit = suit

    def __str__(self):
        """
        Give the card's name.

        Returns:
            str: the card as text, such as "Queen of Hearts".
        """
        return f"{self.rank} of {self.suit}"


class Deck:
    """
    A deck of 52 playing cards.

    Attributes:
        cards (list of Card): the cards still in the deck. The next card
            dealt is the first one in the list.
    """

    def __init__(self):
        """Create a new, unshuffled deck of 52 cards."""
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        """
        Put the cards remaining in the deck into random order.

        Returns:
            None
        """
        random.shuffle(self.cards)

    def deal_card(self):
        """
        Remove and give back the top card of the deck.

        Returns:
            Card: the card taken from the top of the deck.

        Raises:
            ValueError: if there are no cards left in the deck.
        """
        if not self.cards:
            raise ValueError("The deck is empty.")
        return self.cards.pop(0)

    def deal_hand(self, size=HAND_SIZE):
        """
        Deal a hand of cards from the top of the deck.

        Args:
            size (int): the number of cards to deal (default 5).

        Returns:
            list of Card: the cards dealt, in order.
        """
        return [self.deal_card() for _ in range(size)]

    def __len__(self):
        """
        Give the number of cards left in the deck.

        Returns:
            int: the number of cards remaining.
        """
        return len(self.cards)


def parse_selection(text):
    """
    Convert the user's text into a list of card positions to replace.

    The numbers may be separated by commas, spaces, or both, such as
    "1, 3, 5" or "1 3 5". Empty text means no cards are replaced.

    Args:
        text (str): the text the user entered.

    Returns:
        list of int: the positions (1-5) in ascending order.

    Raises:
        ValueError: if an entry is not a number, is outside 1-5, or is
            entered more than once.
    """
    pieces = [piece for piece in re.split(r"[,\s]+", text.strip()) if piece]
    positions = []

    # Check each entry before adding it to the list of positions
    for piece in pieces:
        if not piece.isdecimal():
            raise ValueError(f"'{piece}' is not a number.")

        position = int(piece)
        if position < 1 or position > HAND_SIZE:
            raise ValueError(f"{position} is not between 1 and {HAND_SIZE}.")
        if position in positions:
            raise ValueError(f"{position} was entered more than once.")

        positions.append(position)

    return sorted(positions)


def get_discards():
    """
    Ask the user which cards to replace.

    Keeps asking until the entry is valid. Pressing Enter without typing
    anything keeps the whole hand.

    Returns:
        list of int: the positions (1-5) of the cards to replace, in
            ascending order (empty if the user keeps every card).
    """
    # Loop until the user enters a valid selection
    while True:
        text = input(
            "Enter the card numbers to replace (for example: 1, 3, 5),\n"
            "or press Enter to keep your hand: "
        )

        try:
            return parse_selection(text)
        except ValueError as error:
            print(f"Invalid entry: {error}\n")


def replace_cards(hand, deck, positions):
    """
    Replace the chosen cards in a hand with new cards from the deck.

    The hand list is changed in place.

    Args:
        hand (list of Card): the player's current hand.
        deck (Deck): the deck to draw replacement cards from.
        positions (list of int): positions (1-5) of the cards to replace.

    Returns:
        list of tuple: one (old card, new card) pair for each card
            replaced, in the order they were replaced.
    """
    replacements = []

    # Swap each chosen card for the next card from the deck
    for position in positions:
        old_card = hand[position - 1]
        new_card = deck.deal_card()
        hand[position - 1] = new_card
        replacements.append((old_card, new_card))

    return replacements


def display_hand(hand, title):
    """
    Display a hand with each card numbered.

    Args:
        hand (list of Card): the cards to display.
        title (str): the heading to print above the cards.

    Returns:
        None
    """
    print(f"\n{title}")

    # Loop through the cards, numbering them starting at 1
    for number, card in enumerate(hand, start=1):
        print(f"  {number}. {card}")

    print()


def display_draw_results(replacements, hand):
    """
    Display the result of the draw phase.

    Args:
        replacements (list of tuple): (old card, new card) pairs.
        hand (list of Card): the player's final hand.

    Returns:
        None
    """
    # If statement: handle the case where no cards were replaced
    if not replacements:
        print("\nYou kept all of your cards.")
    else:
        print(f"\nYou replaced {len(replacements)} card(s):")
        for old_card, new_card in replacements:
            print(f"  {old_card}  ->  {new_card}")

    display_hand(hand, "Your final hand:")


def raises_value_error(function, *args):
    """
    Check whether calling a function raises a ValueError.

    Args:
        function: the function or method to call.
        *args: the arguments to pass to the function.

    Returns:
        bool: True if a ValueError was raised, otherwise False.
    """
    try:
        function(*args)
    except ValueError:
        return True
    return False


def run_tests():
    """
    Test the Deck class, parse_selection, and replace_cards.

    Each check is (description, actual result, expected result). The
    function prints PASS or FAIL for every check and a final summary.

    Returns:
        bool: True if every check passed, otherwise False.
    """
    # Deck used to check dealing: an unshuffled deck starts 2, 3, 4...
    deck = Deck()
    full_names = [str(card) for card in deck.cards]
    top_card = str(deck.deal_card())
    cards_after_one = len(deck)

    # Deck used to check dealing a hand
    hand_deck = Deck()
    hand = hand_deck.deal_hand()

    # Deck used to check shuffling
    shuffled = Deck()
    shuffled.shuffle()

    # Deck and hand used to check replacing cards
    swap_deck = Deck()
    swap_hand = swap_deck.deal_hand()
    swaps = replace_cards(swap_hand, swap_deck, [1, 3])
    swap_names = [str(card) for card in swap_hand]
    leftover = [str(card) for card in swap_deck.cards]
    keep_deck = Deck()
    keep_hand = keep_deck.deal_hand()

    # A deck with no cards left, used to check the empty-deck error
    empty = Deck()
    empty.cards = []

    checks = [
        ("new deck has 52 cards", len(Deck()), 52),
        ("all 52 cards are different", len(set(full_names)), 52),
        ("first card of a new deck", top_card, "2 of Clubs"),
        ("deal_card removes one card", cards_after_one, 51),
        ("deal_hand returns 5 cards", len(hand), 5),
        ("deck has 47 cards after dealing a hand", len(hand_deck), 47),
        ("shuffle keeps 52 cards", len(shuffled), 52),
        ("shuffle keeps the same cards",
         sorted(str(card) for card in shuffled.cards), sorted(full_names)),
        ("dealing from an empty deck raises ValueError",
         raises_value_error(empty.deal_card), True),
        ("'1, 3, 5' selects 1, 3, 5", parse_selection("1, 3, 5"), [1, 3, 5]),
        ("'5 3 1' is sorted to 1, 3, 5", parse_selection("5 3 1"),
         [1, 3, 5]),
        ("'2,4' works without spaces", parse_selection("2,4"), [2, 4]),
        ("empty text selects nothing", parse_selection(""), []),
        ("'1,,3' ignores the extra comma", parse_selection("1,,3"), [1, 3]),
        ("'0' raises ValueError", raises_value_error(parse_selection, "0"),
         True),
        ("'6' raises ValueError", raises_value_error(parse_selection, "6"),
         True),
        ("'-1' raises ValueError",
         raises_value_error(parse_selection, "-1"), True),
        ("'a' raises ValueError", raises_value_error(parse_selection, "a"),
         True),
        ("'1.5' raises ValueError",
         raises_value_error(parse_selection, "1.5"), True),
        ("'2, 2' raises ValueError",
         raises_value_error(parse_selection, "2, 2"), True),
        ("replace_cards swaps positions 1 and 3", swap_names,
         ["7 of Clubs", "3 of Clubs", "8 of Clubs", "5 of Clubs",
          "6 of Clubs"]),
        ("replace_cards returns the old and new cards",
         [(str(old), str(new)) for old, new in swaps],
         [("2 of Clubs", "7 of Clubs"), ("4 of Clubs", "8 of Clubs")]),
        ("replace_cards uses 2 cards from the deck", len(swap_deck), 45),
        ("replaced cards are not in the deck",
         "2 of Clubs" in leftover or "4 of Clubs" in leftover, False),
        ("replace_cards with no positions changes nothing",
         (replace_cards(keep_hand, keep_deck, []), len(keep_deck)),
         ([], 47)),
    ]

    # Accumulators: count the checks that passed and failed
    passed = 0
    failed = 0

    # Loop through every check and compare the result to expected
    for description, actual, expected in checks:
        if actual == expected:
            passed += 1
            print(f"PASS  {description}")
        else:
            failed += 1
            print(f"FAIL  {description}")
            print(f"      expected: {expected!r}")
            print(f"      actual:   {actual!r}")

    print(f"\n{passed} passed, {failed} failed, {len(checks)} total.")
    return failed == 0


def main():
    """Play five-card draw: deal, ask for discards, draw, and show results."""
    print("Five-Card Draw Poker")

    again = "y"

    # Loop until the user chooses to stop playing
    while again == "y":
        deck = Deck()
        deck.shuffle()
        hand = deck.deal_hand()

        display_hand(hand, "Your hand:")

        positions = get_discards()
        replacements = replace_cards(hand, deck, positions)
        display_draw_results(replacements, hand)

        again = input("Play again? (y/n): ").strip().lower()
        print()

    print("Thanks for playing!")


# Run the tests with "--test", otherwise play the game
if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    else:
        main()
