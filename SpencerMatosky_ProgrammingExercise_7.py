"""
sentence_counter.py

A simple console application that lets the user enter a paragraph,
splits it into individual sentences, and displays each sentence along
with the total number of sentences. Sentences that begin with a number
(such as "2024 was a great year.") are handled correctly, and periods
inside decimal numbers (3.50) or after common abbreviations (Dr.) are
not treated as the end of a sentence. Running the file with the argument
--test runs a built-in set of test cases against the splitting function.
"""

import re
import sys

# A sentence break is whitespace that follows ., !, or ? (optionally
# followed by a closing quote or parenthesis) and comes before a capital
# letter or a digit. Allowing a digit lets a new sentence start with a
# number, while requiring whitespace after the punctuation keeps decimals
# such as 3.50 in one piece.
SENTENCE_BREAK = re.compile(
    r"(?:(?<=[.!?])|(?<=[.!?][\"')\u201d\u2019]))"
    r"\s+"
    r"(?=[\"'(\u201c\u2018]?[A-Z0-9])"
)

# Lowercase abbreviations whose period does not end a sentence
ABBREVIATIONS = {
    "mr.", "mrs.", "ms.", "dr.", "prof.", "sr.", "jr.", "st.", "vs.",
    "e.g.", "i.e.",
}

# Matches a list marker such as "1." or "12." (digits followed by a period)
LIST_MARKER = re.compile(r"\d+\.")


def get_paragraph():
    """
    Prompt the user to enter a paragraph.

    The user may type or paste one or more lines. A blank line finishes
    the input. The lines are joined into a single string separated by
    spaces. The user is asked again if nothing is entered.

    Returns:
        str: the paragraph text entered by the user (never empty).
    """
    lines = []

    print("Enter a paragraph. Press Enter on a blank line to finish.")

    # Loop until the user has entered text and then a blank line
    while True:
        line = input().strip()

        # If statement: a blank line ends the input once text exists
        if line == "":
            if lines:
                break
            print("Please enter at least one line of text.")
            continue

        lines.append(line)

    return " ".join(lines)


def split_sentences(paragraph):
    """
    Split a paragraph into a list of individual sentences.

    A sentence ends at ., !, or ? when followed by whitespace and then a
    capital letter or a digit, so sentences that begin with a number are
    split correctly. A possible break is skipped when the text before it
    ends with a known abbreviation (such as "Dr.") or is only a list
    marker (such as "1.").

    Args:
        paragraph (str): the paragraph text to split.

    Returns:
        list of str: the sentences in order (empty if there is no text).
    """
    sentences = []
    start = 0

    # Check each possible break point found by the regular expression
    for match in SENTENCE_BREAK.finditer(paragraph):
        candidate = paragraph[start:match.start()].strip()
        words = candidate.split()
        last_word = words[-1] if words else ""

        # Skip breaks that follow an abbreviation, such as "Dr."
        if last_word.lower() in ABBREVIATIONS:
            continue

        # Skip breaks that follow a list marker alone, such as "1."
        if LIST_MARKER.fullmatch(candidate):
            continue

        sentences.append(candidate)
        start = match.end()

    # Whatever remains after the last break is the final sentence
    final_sentence = paragraph[start:].strip()
    if final_sentence:
        sentences.append(final_sentence)

    return sentences


def display_sentences(sentences):
    """
    Display each sentence on its own numbered line and the total count.

    Args:
        sentences (list of str): the sentences to display.

    Returns:
        None
    """
    print("\n--- Sentences ---")

    # Loop through the sentences, numbering them starting at 1
    for number, sentence in enumerate(sentences, start=1):
        print(f"{number}. {sentence}")

    print(f"\nTotal number of sentences: {len(sentences)}")


def run_tests():
    """
    Test split_sentences with a variety of paragraphs.

    Each test case is (paragraph, expected list of sentences). The
    function prints PASS or FAIL for every case and a final summary.

    Returns:
        bool: True if every test case passed, otherwise False.
    """
    test_cases = [
        ("Hello world. This is a test.",
         ["Hello world.", "This is a test."]),
        ("2024 was a great year. 3 stores opened. 100 people came.",
         ["2024 was a great year.", "3 stores opened.", "100 people came."]),
        ("It cost $3.50 today. Pi is 3.14 exactly.",
         ["It cost $3.50 today.", "Pi is 3.14 exactly."]),
        ("Dr. Smith arrived. He sat down.",
         ["Dr. Smith arrived.", "He sat down."]),
        ("Is it done? Yes! 5 minutes ago.",
         ["Is it done?", "Yes!", "5 minutes ago."]),
        ('He said "Go home." 7 people left.',
         ['He said "Go home."', "7 people left."]),
        ("1. Buy milk. 2. Buy eggs.",
         ["1. Buy milk.", "2. Buy eggs."]),
        ("No ending punctuation here",
         ["No ending punctuation here"]),
        ("   ", []),
    ]

    # Accumulators: count the test cases that passed and failed
    passed = 0
    failed = 0

    # Loop through every test case and compare the result to expected
    for paragraph, expected in test_cases:
        actual = split_sentences(paragraph)
        if actual == expected:
            passed += 1
            result = "PASS"
        else:
            failed += 1
            result = "FAIL"
        print(f"{result}  {paragraph!r} -> {len(actual)} sentence(s)")
        if actual != expected:
            print(f"      expected: {expected}")
            print(f"      actual:   {actual}")

    print(f"\n{passed} passed, {failed} failed, {len(test_cases)} total.")
    return failed == 0


def main():
    """Get a paragraph, split it into sentences, and display the results."""
    print("Sentence Counter\n")

    again = "y"

    # Loop until the user chooses to stop
    while again == "y":
        paragraph = get_paragraph()
        sentences = split_sentences(paragraph)
        display_sentences(sentences)

        again = input("\nEnter another paragraph? (y/n): ").strip().lower()
        print()

    print("Goodbye!")


# Run the tests with "--test", otherwise run the interactive program
if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    else:
        main()
