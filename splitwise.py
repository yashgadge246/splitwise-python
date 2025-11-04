#### ----------- SPLITWISE PROGRAM -----------

# Friends List
friends = []

# Contributions Table (who paid for whom)
contributions = {}

# Expenses by Category
category_expenses = {}

# Balances (final settlement calculation ke liye)
balances = {}

# Expense History
expense_history = []

# ------------------- FUNCTIONS -------------------

def add_friends():
    """Friends list input/update"""
    global friends, contributions, balances
    n = int(input("Kitne dost add karna hai? "))
    for i in range(n):
        name = input(f"Friend {i+1} ka naam: ").strip()
        if name and name not in friends:
            friends.append(name)

    # Initialize/expand contributions
    for payer in friends:
        if payer not in contributions:
            contributions[payer] = {}
        for receiver in friends:
            if receiver not in contributions[payer]:
                contributions[payer][receiver] = 0.0

    # Initialize/expand balances
    balances = {f: balances.get(f, 0.0) for f in friends}

    print("\n✅ Friends list update ho gayi:", friends)


def add_expense():
    if not friends:
        print("❌ Pehle friends add karo!")
        return

    payer = input("Kisne pay kiya? ").strip()
    while payer not in friends:
        print("❌ Galat naam! Kripya sahi naam dijiye.")
        payer = input("Kisne pay kiya? ").strip()

    try:
        amount = float(input("Kitna kharcha hua? "))
        if amount <= 0:
            print("❌ Amount positive hona chahiye.")
            return
    except ValueError:
        print("❌ Galat amount.")
        return

    category = input("Expense category (e.g., travel, food, shopping): ").strip() or "General"

    raw = input("Kin logon ke beech split karna hai? (comma separated, blank = sab) ").split(",")
    split_between = [p.strip() for p in raw if p.strip()]
    if not split_between:
        split_between = friends.copy()

    # ✅ Only valid friends in split; warn for invalid
    valid_split = []
    for person in split_between:
        if person in friends:
            valid_split.append(person)
        else:
            print(f"⚠️ {person} friend list me nahi hai, skip kiya.")

    if not valid_split:  # agar saare invalid the to sab pe split
        valid_split = friends.copy()

    share = amount / len(valid_split)

    # ---- Update contributions (payer ne kiske liye pay kiya) ----
    for person in valid_split:
        contributions[payer][person] += share

    # ---- ✅ Correct balance updates (no double counting) ----
    balances[payer] += amount
    for person in valid_split:
        balances[person] -= share

    # Category wise expense track
    category_expenses[category] = category_expenses.get(category, 0.0) + amount

    # Expense history save
    expense_history.append({
        "payer": payer,
        "amount": amount,
        "category": category,
        "split_between": valid_split
    })

    print(f"✅ {amount:.2f} Rs added for {category}, paid by {payer}, split between {', '.join(valid_split)}")


def show_contributions_table():
    if not friends:
        print("❌ Friends list empty hai.")
        return
    print("\n===== CONTRIBUTIONS TABLE =====")
    header = "        " + "".join(f"{name:12}" for name in friends)
    print(header)
    for payer in friends:
        row = f"{payer:8}"
        for receiver in friends:
            row += f"{contributions[payer][receiver]:12.2f}"
        print(row)


def show_balances():
    if not balances:
        print("❌ Koi balance nahi mila.")
        return

    # Round to 2 decimals to avoid tiny float residues
    rounded = {p: round(bal, 2) for p, bal in balances.items()}

    print("\n===== BALANCES =====")
    for person, bal in rounded.items():
        if bal > 0:
            print(f"{person} should RECEIVE {bal:.2f}")
        elif bal < 0:
            print(f"{person} should PAY {-bal:.2f}")
        else:
            print(f"{person} is SETTLED")

    # Settlement Suggestion (greedy)
    print("\n===== SETTLEMENT SUGGESTIONS =====")
    payers = sorted([(p, -amt) for p, amt in rounded.items() if amt < 0], key=lambda x: x[1], reverse=True)
    receivers = sorted([(p, amt) for p, amt in rounded.items() if amt > 0], key=lambda x: x[1], reverse=True)

    i, j = 0, 0
    while i < len(payers) and j < len(receivers):
        payer, pay_amt = payers[i]
        receiver, rec_amt = receivers[j]
        amount = round(min(pay_amt, rec_amt), 2)
        if amount > 0:
            print(f"{payer} -> {receiver}: {amount:.2f}")
        payers[i] = (payer, round(pay_amt - amount, 2))
        receivers[j] = (receiver, round(rec_amt - amount, 2))
        if payers[i][1] <= 0:
            i += 1
        if receivers[j][1] <= 0:
            j += 1


def show_category_expenses():
    if not category_expenses:
        print("❌ Abhi tak koi category expense add nahi hua.")
        return
    print("\n===== CATEGORY EXPENSES =====")
    for cat, amt in category_expenses.items():
        print(f"{cat:12}: {amt:.2f}")


def show_per_person_expense():
    """
    Yahan 'actual kharcha' (share ke hisaab se) dikhayenge:
    kis friend ka is trip par total cost kitna bana.
    """
    if not friends:
        print("❌ Friends list empty hai.")
        return
    if not expense_history:
        print("❌ Abhi tak koi expense add nahi hua.")
        return

    # Actual cost per person based on shares
    actual_cost = {f: 0.0 for f in friends}
    for e in expense_history:
        share = e["amount"] / len(e["split_between"])
        for person in e["split_between"]:
            if person in actual_cost:
                actual_cost[person] += share

    total = sum(category_expenses.values())
    print("\n===== PER PERSON ACTUAL EXPENSE =====")
    print(f"Total Trip Expense: {total:.2f}\n")
    for f in friends:
        print(f"{f:10} ka kharcha: {actual_cost[f]:.2f}")


def show_history():
    if not expense_history:
        print("❌ Abhi tak koi expense add nahi hua.")
        return
    print("\n===== EXPENSE HISTORY =====")
    for i, e in enumerate(expense_history, 1):
        print(f"{i}. {e['payer']} paid {e['amount']:.2f} for {e['category']} (split: {', '.join(e['split_between'])})")


# ------------------- MAIN PROGRAM -------------------

def menu():
    print("\n===== SPLITWISE MENU =====")
    print("1. Add Friends")
    print("2. Add Expense")
    print("3. Show Contributions Table")
    print("4. Show Balances + Settlements")
    print("5. Show Category Expenses")
    print("6. Show Per Person Expense")
    print("7. Show Expense History")
    print("8. Exit")


def main():
    while True:
        menu()
        choice = input("Enter choice: ")
        
        if choice == "1":
            add_friends()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            show_contributions_table()
        elif choice == "4":
            show_balances()
        elif choice == "5":
            show_category_expenses()
        elif choice == "6":
            show_per_person_expense()
        elif choice == "7":
            show_history()
        elif choice == "8":
            print("Exiting Splitwise... Bye!")
            break
        else:
            print("❌ Invalid choice, try again!")

# Run Program
main()
