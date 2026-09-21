"""
Spam Score Checker - Programming Exercise 2
------------------
The user enters an email message. The program scans it for 30 words/phrases
that are commonly found in spam, adds one point to the "spam score" for every
occurrence, rates how likely the message is to be spam, and reports which
words/phrases caused points to be added.

"""

import re

# ---------------------------------------------------------------------------
# The 30 spam words / phrases, grouped by theme
# ---------------------------------------------------------------------------
SPAM_PHRASES = [
    # Urgency and pressure
    "act now",
    "limited time",
    "urgent",
    "final notice",
    "last chance",
    "one time only",
    # Money and "too good to be true" promises
    "free",
    "guaranteed",
    "risk-free",
    "make money fast",
    "get rich quick",
    "earn extra cash",
    "cash bonus",
    "double your money",
    "no credit check",
    "no hidden fees",
    "no obligation",
    "cheap",
    # Prizes and flattery
    "winner",
    "congratulations",
    "you have been selected",
    "dear friend",
    # Pushy calls to action
    "click here",
    "buy now",
    "order now",
    # Health / adult products and exaggerated claims
    "lose weight fast",
    "weight loss drugs",
    "unbelievable results",
    # Phishing and credibility tricks
    "verify your account",
    "this is not spam",
]

# Score ranges -> likelihood rating: (minimum score, rating)
# The list is checked from the highest threshold down.
RATING_LEVELS = [
    (7, "VERY HIGH - this is almost certainly spam"),
    (5, "HIGH - this is very likely spam"),
    (3, "MODERATE - this message is suspicious"),
    (1, "LOW - probably legitimate, but be cautious"),
    (0, "VERY LOW - this looks like a normal message"),
]


def scan_message(message):
    """
    Scan the message for every spam phrase.

    Returns (score, found) where `found` maps each phrase that appeared to
    the number of times it appeared. Each occurrence adds one point.

    Phrases are checked longest-first, and each match is blanked out of the
    text once counted. That way "risk-free" is not ALSO counted as "free".
    """
    text = message.lower()
    found = {}

    for phrase in sorted(SPAM_PHRASES, key=len, reverse=True):
        # (?<!\w) and (?!\w) make sure we match whole words only, so "free"
        # does not match inside "freedom" or "carefree".
        pattern = re.compile(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)")
        text, count = pattern.subn(" ", text)
        if count > 0:
            found[phrase] = count

    score = sum(found.values())
    return score, found


def rate_likelihood(score):
    """Convert a numeric spam score into a likelihood rating."""
    for minimum, rating in RATING_LEVELS:
        if score >= minimum:
            return rating
    return RATING_LEVELS[-1][1]


def display_results(score, found):
    """Print the score, the likelihood rating, and the offending phrases."""
    print()
    print("=" * 50)
    print("SPAM ANALYSIS RESULTS")
    print("=" * 50)
    print(f"Spam score : {score}")
    print(f"Likelihood : {rate_likelihood(score)}")

    if found:
        print("\nWords/phrases that added to the score:")
        for phrase, count in sorted(found.items(), key=lambda item: -item[1]):
            times = "time" if count == 1 else "times"
            print(f'  - "{phrase}"  ({count} {times})')
    else:
        print("\nNo spam words or phrases were found.")
    print("=" * 50)


def get_message():
    """
    Read a (possibly multi-line) email message from the user.
    The user types END on a line by itself to finish.
    """
    print("Enter or paste your email message below.")
    print("When you are done, type END on a line by itself and press Enter.\n")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:  # input ended (e.g., piped in from a file)
            break
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def main():
    print("=== Email Spam Score Checker ===\n")

    while True:
        message = get_message()

        if message.strip() == "":
            print("\nNo message was entered.")
        else:
            score, found = scan_message(message)
            display_results(score, found)

        try:
            again = input("\nCheck another message? (y/n): ").strip().lower()
        except EOFError:
            break
        if again != "y":
            break
        print()

    print("Goodbye!")


if __name__ == "__main__":
    main()