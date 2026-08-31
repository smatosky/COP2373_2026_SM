"""
SpencerMatosky_ProgrammingExercise_1.py

A simple  application that pre-sells a limited number of movie
tickets. Each buyer may purchase up to 4 tickets, and no more than 20
tickets total may be sold. The program prompts each buyer for a ticket
quantity, displays the number of tickets remaining after each purchase,
and repeats until the full allotment has been sold. Once sold out, the
program displays the total number of buyers who purchased tickets.
"""

# Maximum number of tickets a single buyer may purchase in one transaction
MAX_TICKETS_PER_BUYER = 4

# Total number of tickets available for the entire pre-sale
TOTAL_TICKETS_AVAILABLE = 20


def get_ticket_request(remaining_tickets):
    """
    Prompt the user (buyer) for the number of tickets they want to buy.

    Keeps asking until a valid whole number is entered that is:
      - at least 1
      - no more than MAX_TICKETS_PER_BUYER
      - no more than the number of tickets still remaining

    Args:
        remaining_tickets (int): number of tickets still available to sell.

    Returns:
        int: a validated number of tickets the buyer wishes to purchase.
    """
    # Loop until we receive valid input from the buyer
    while True:
        # Get raw input from the user and attempt to convert to an integer
        raw_input_value = input(
            f"Tickets remaining: {remaining_tickets}. "
            f"How many tickets would you like to buy "
            f"(1-{min(MAX_TICKETS_PER_BUYER, remaining_tickets)})? "
        )

        try:
            requested_tickets = int(raw_input_value)
        except ValueError:
            # Input was not a whole number
            print("Please enter a valid whole number.\n")
            continue

        # Validate the requested amount using if/elif/else checks
        if requested_tickets < 1:
            print("You must purchase at least 1 ticket.\n")
        elif requested_tickets > MAX_TICKETS_PER_BUYER:
            print(
                f"You may not purchase more than "
                f"{MAX_TICKETS_PER_BUYER} tickets at a time.\n"
            )
        elif requested_tickets > remaining_tickets:
            print(
                f"Only {remaining_tickets} ticket(s) remain. "
                f"Please request a smaller amount.\n"
            )
        else:
            # Input passed all checks, return it to the caller
            return requested_tickets


def display_purchase_summary(buyer_number, tickets_bought, remaining_tickets):
    """
    Display a summary of a single buyer's purchase.

    Args:
        buyer_number (int): the sequential number of this buyer (1st, 2nd, ...).
        tickets_bought (int): number of tickets this buyer purchased.
        remaining_tickets (int): number of tickets left after the purchase.

    Returns:
        None
    """
    print(f"Buyer #{buyer_number} purchased {tickets_bought} ticket(s).")
    print(f"Tickets remaining: {remaining_tickets}\n")


def main():
    """Run the cinema ticket pre-sale program from start to finish."""
    print("Welcome to the cinema ticket pre-sale!")
    print(f"{TOTAL_TICKETS_AVAILABLE} tickets are available.\n")

    # Accumulators: track running totals as the sale progresses
    tickets_sold = 0
    buyer_count = 0

    # Main sales loop - continues until every ticket has been sold
    while tickets_sold < TOTAL_TICKETS_AVAILABLE:
        tickets_remaining = TOTAL_TICKETS_AVAILABLE - tickets_sold

        # Get a validated ticket request from the current buyer
        requested_tickets = get_ticket_request(tickets_remaining)

        # Update accumulators with this buyer's purchase
        tickets_sold += requested_tickets
        buyer_count += 1

        # Show the buyer a summary of their purchase and tickets left
        display_purchase_summary(
            buyer_count,
            requested_tickets,
            TOTAL_TICKETS_AVAILABLE - tickets_sold,
        )

    # All tickets have been sold - report final totals
    print("All tickets have been sold!")
    print(f"Total number of buyers: {buyer_count}")


# Only run main() when this file is executed directly, not when imported
if __name__ == "__main__":
    main()
