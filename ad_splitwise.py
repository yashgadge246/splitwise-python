import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


friends = []
expenses_df = pd.DataFrame(columns=["payer", "amount", "category", "split_between"])


def add_friends():
    global friends
    n = int(input("Kitne dost add karna hai? "))
    for i in range(n):
        name = input(f"Friend {i+1} ka naam: ").strip()
        if name and name not in friends:
            friends.append(name)
    print("✅ Friends list updated:", friends)


def add_expense():
    global expenses_df
    if not friends:
        print("❌ Pehle friends add karo!")
        return

    payer = input("Kisne pay kiya? ").strip()
    if payer not in friends:
        print("❌ Invalid payer.")
        return

    try:
        amount = float(input("Kitna kharcha hua? "))
    except ValueError:
        print("❌ Invalid amount.")
        return

    category = input("Category (e.g. Food, Travel, Shopping): ").strip() or "General"
    raw = input("Kin logon ke beech split karna hai? (comma separated, blank = sab): ").split(",")
    split_between = [x.strip() for x in raw if x.strip()]
    if not split_between:
        split_between = friends.copy()

    new_entry = pd.DataFrame([{
        "payer": payer,
        "amount": amount,
        "category": category,
        "split_between": split_between
    }])
    expenses_df = pd.concat([expenses_df, new_entry], ignore_index=True)
    print("✅ Expense added successfully!")


def calculate_balances():
    balances = {f: 0.0 for f in friends}
    for _, row in expenses_df.iterrows():
        payer = row["payer"]
        amount = row["amount"]
        split = row["split_between"]
        share = amount / len(split)
        balances[payer] += amount
        for p in split:
            balances[p] -= share
    return pd.Series(balances, name="Balance")


def show_summary():
    if expenses_df.empty:
        print("❌ Abhi tak koi expense add nahi hua.")
    else:
        print("\n===== EXPENSE SUMMARY =====")
        print(expenses_df)


def visualize_category_expense():
    if expenses_df.empty:
        print("❌ No expenses to plot.")
        return
    plt.figure(figsize=(6,4))
    sns.barplot(data=expenses_df, x="category", y="amount", estimator=sum, ci=None)
    plt.title("Total Expense by Category")
    plt.ylabel("Amount (Rs)")
    plt.show()


def visualize_per_person_expense():
    if expenses_df.empty:
        print("❌ No expenses yet.")
        return

    person_expense = {f: 0.0 for f in friends}
    for _, row in expenses_df.iterrows():
        split = row["split_between"]
        share = row["amount"] / len(split)
        for s in split:
            person_expense[s] += share

    df = pd.DataFrame(list(person_expense.items()), columns=["Friend", "Total Expense"])
    plt.figure(figsize=(6,4))
    sns.barplot(data=df, x="Friend", y="Total Expense")
    plt.title("Per Person Actual Expense")
    plt.show()


def visualize_balances():
    if expenses_df.empty:
        print("❌ No expenses yet.")
        return

    balances = calculate_balances().reset_index()
    balances.columns = ["Friend", "Balance"]
    plt.figure(figsize=(6,4))
    sns.barplot(data=balances, x="Friend", y="Balance", hue=(balances["Balance"] > 0))
    plt.title("Balances (Positive = Receivable, Negative = Payable)")
    plt.axhline(0, color='black', linewidth=1)
    plt.show()



def menu():
    print("\n===== SPLITWISE MENU =====")
    print("1. Add Friends")
    print("2. Add Expense")
    print("3. Show Expense Summary")
    print("4. Visualize Expense by Category")
    print("5. Visualize Per Person Expense")
    print("6. Visualize Balances")
    print("7. Exit")

def main():
    while True:
        menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_friends()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            visualize_category_expense()
        elif choice == "5":
            visualize_per_person_expense()
        elif choice == "6":
            visualize_balances()
        elif choice == "7":
            print("👋 Exiting Splitwise... Bye!")
            break
        else:
            print("❌ Invalid choice, please try again.")


main()
