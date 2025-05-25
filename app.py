# app.py
from flask import Flask, render_template, request
import random
# Create a new Flask app
app = Flask(__name__)
# Game configuration
ROWS = 3
COLS = 3
MAX_LINES = 3
# Symbols and how often they appear
SYMBOL_COUNT = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}
# Payout value for each symbol
SYMBOL_VALUE = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}
# Function to create a slot spin result
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        for _ in range(count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        current_symbols = all_symbols[:]  # Copy all symbols
        column = []
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)

    return columns

# Function to check if user won
def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []

    # Loop through each line the user bet on
    for line in range(lines):
        first_symbol = columns[0][line]

        # Check if all columns in this row have the same symbol
        for column in columns:
            if column[line] != first_symbol:
                break
        else:  # Only runs if no break occurred
            winnings += values[first_symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines

# Main route for the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form values from user input
        lines = int(request.form["lines"])
        bet = int(request.form["bet"])
        total_bet = lines * bet

        # Generate slot spin and check for winnings
        slots = get_slot_machine_spin(ROWS, COLS, SYMBOL_COUNT)
        winnings, winning_lines = check_winnings(slots, lines, bet, SYMBOL_VALUE)

        # Pass results to result.html
        return render_template("result.html",
                               slots=slots,
                               bet=bet,
                               lines=lines,
                               total_bet=total_bet,
                               winnings=winnings,
                               winning_lines=winning_lines)

    # Show the homepage with the form
    return render_template("index.html", max_lines=MAX_LINES)
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)