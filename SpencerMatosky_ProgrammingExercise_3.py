"""
expense_analyzer.py

A simple console application that collects a list of monthly expenses
from the user (each with an expense type and an amount) and then uses
functools.reduce to calculate and display the total expense, the highest
expense, and the lowest expense. The highest and lowest expenses are
labeled with their expense type.
"""

from functools import reduce


def get_expenses():
    """
    Prompt the user for a list of monthly expenses.

    For each expense the user is asked for the type of expense (for
    example, "Rent") and the amount. The user types "done" when asked
    for the expense type to finish entering expenses. Amounts must be
    valid non-negative numbers, and at least one expense is required.

    Returns:
        list of tuple: each tuple is (expense_type (str), amount (float)).
    """
    expenses = []

    print("Enter your monthly expenses. Type 'done' when finished.\n")

    # Loop until the user is finished and has entered at least one expense
    while True:
        expense_type = input("Expense type (or 'done'): ").strip()

        # If statement: check whether the user wants to stop entering data
        if expense_type.lower() == "done":
            if expenses:
                break
            print("Please enter at least one expense first.\n")
            continue

        if expense_type == "":
            print("Expense type cannot be blank.\n")
            continue

        # Get and validate the amount for this expense
        try:
            amount = float(input(f"Amount for {expense_type}: $"))
        except ValueError:
            print("Please enter a valid number for the amount.\n")
            continue

        if amount < 0:
            print("Amount cannot be negative.\n")
            continue

        expenses.append((expense_type, amount))
        print(f"Added {expense_type}: ${amount:,.2f}\n")

    return expenses


def calculate_total(expenses):
    """
    Calculate the total of all expenses using reduce.

    Args:
        expenses (list of tuple): (expense_type, amount) pairs.

    Returns:
        float: the sum of every expense amount.
    """
    # Lambda adds each expense's amount (index 1) to the running total
    return reduce(lambda total, expense: total + expense[1], expenses, 0)


def find_highest(expenses):
    """
    Find the highest expense using reduce.

    Args:
        expenses (list of tuple): (expense_type, amount) pairs.

    Returns:
        tuple: the (expense_type, amount) pair with the largest amount.
    """
    # Lambda keeps whichever of the two expenses has the larger amount
    return reduce(
        lambda high, expense: expense if expense[1] > high[1] else high,
        expenses,
    )


def find_lowest(expenses):
    """
    Find the lowest expense using reduce.

    Args:
        expenses (list of tuple): (expense_type, amount) pairs.

    Returns:
        tuple: the (expense_type, amount) pair with the smallest amount.
    """
    # Lambda keeps whichever of the two expenses has the smaller amount
    return reduce(
        lambda low, expense: expense if expense[1] < low[1] else low,
        expenses,
    )


def display_results(total, highest, lowest):
    """
    Display the expense analysis results.

    Args:
        total (float): the total of all expenses.
        highest (tuple): (expense_type, amount) of the highest expense.
        lowest (tuple): (expense_type, amount) of the lowest expense.

    Returns:
        None
    """
    print("\n--- Monthly Expense Summary ---")
    print(f"Total expenses:   ${total:,.2f}")
    print(f"Highest expense:  {highest[0]} (${highest[1]:,.2f})")
    print(f"Lowest expense:   {lowest[0]} (${lowest[1]:,.2f})")


def main():
    """Run the monthly expense analyzer from start to finish."""
    expenses = get_expenses()

    # Use reduce-based functions to analyze the collected expenses
    total = calculate_total(expenses)
    highest = find_highest(expenses)
    lowest = find_lowest(expenses)

    display_results(total, highest, lowest)


# Only run main() when this file is executed directly, not when imported
if __name__ == "__main__":
    main()
