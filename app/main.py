from app.database import initialize_database
from app.services import BankService


def format_money(amount):
    """Format amount as Nigerian Naira."""
    return f"₦{amount:,.2f}"


def create_account():
    print("\n========== CREATE ACCOUNT ==========")

    name = input("Full Name: ").strip()
    pin = input("Create 4-digit PIN: ").strip()

    try:
        initial_deposit = int(
            input("Initial Deposit (₦): ").strip()
        )

        account_number = BankService.create_account(
            name,
            pin,
            initial_deposit
        )

        print("\n✅ Account created successfully!")
        print(f"Account Number: {account_number}")
        print(f"Initial Balance: {format_money(initial_deposit)}")

    except ValueError as error:
        print(f"\n❌ {error}")


def check_balance():
    print("\n========== ACCOUNT BALANCE ==========")

    account_number = input(
        "Account Number: "
    ).strip()

    pin = input("PIN: ").strip()

    if not BankService.authenticate(
        account_number,
        pin
    ):
        print("\n❌ Invalid account number or PIN.")
        return

    account = BankService.get_account(
        account_number
    )

    print("\n----- ACCOUNT -----")
    print(f"Name: {account[1]}")
    print(f"Account Number: {account[2]}")
    print(f"Balance: {format_money(account[3])}")


def deposit():
    print("\n========== DEPOSIT ==========")

    account_number = input(
        "Account Number: "
    ).strip()

    try:
        amount = int(
            input("Amount (₦): ").strip()
        )

        new_balance = BankService.deposit(
            account_number,
            amount
        )

        print("\n✅ Deposit successful!")
        print(
            f"New Balance: {format_money(new_balance)}"
        )

    except ValueError as error:
        print(f"\n❌ {error}")


def withdraw():
    print("\n========== WITHDRAW ==========")

    account_number = input(
        "Account Number: "
    ).strip()

    pin = input("PIN: ").strip()

    try:
        amount = int(
            input("Amount (₦): ").strip()
        )

        new_balance = BankService.withdraw(
            account_number,
            pin,
            amount
        )

        print("\n✅ Withdrawal successful!")
        print(
            f"New Balance: {format_money(new_balance)}"
        )

    except ValueError as error:
        print(f"\n❌ {error}")


def transfer():
    print("\n========== TRANSFER ==========")

    sender = input(
        "Your Account Number: "
    ).strip()

    pin = input("Your PIN: ").strip()

    recipient = input(
        "Recipient Account Number: "
    ).strip()

    try:
        amount = int(
            input("Amount (₦): ").strip()
        )

        new_balance = BankService.transfer(
            sender,
            pin,
            recipient,
            amount
        )

        print("\n✅ Transfer successful!")
        print(
            f"New Balance: {format_money(new_balance)}"
        )

    except ValueError as error:
        print(f"\n❌ {error}")

def change_pin():
    print("\n========== CHANGE PIN ==========")

    account_number = input(
        "Account Number: "
    ).strip()

    old_pin = input(
        "Current PIN: "
    ).strip()

    new_pin = input(
        "New 4-digit PIN: "
    ).strip()

    confirm_pin = input(
        "Confirm New PIN: "
    ).strip()

    if new_pin != confirm_pin:
        print("\n❌ New PINs do not match.")
        return

    try:
        BankService.change_pin(
            account_number,
            old_pin,
            new_pin
        )

        print("\n✅ PIN changed successfully!")

    except ValueError as error:
        print(f"\n❌ {error}")


def delete_account():
    print("\n========== DELETE ACCOUNT ==========")

    account_number = input(
        "Account Number: "
    ).strip()

    pin = input("PIN: ").strip()

    confirmation = input(
        "Type DELETE to confirm: "
    ).strip()

    if confirmation != "DELETE":
        print("\n❌ Account deletion cancelled.")
        return

    try:
        BankService.delete_account(
            account_number,
            pin
        )

        print("\n✅ Account deleted successfully.")

    except ValueError as error:
        print(f"\n❌ {error}")


def search_account():
    print("\n========== SEARCH ACCOUNT ==========")

    account_number = input(
        "Account Number: "
    ).strip()

    try:
        account = BankService.search_account(
            account_number
        )

        print("\n----- ACCOUNT FOUND -----")
        print(f"Name: {account[1]}")
        print(f"Account Number: {account[2]}")
        print(f"Balance: {format_money(account[3])}")
        print(f"Created: {account[4]}")

    except ValueError as error:
        print(f"\n❌ {error}")
        
def transaction_history():
    print("\n========== TRANSACTION HISTORY ==========")

    account_number = input(
        "Account Number: "
    ).strip()

    pin = input("PIN: ").strip()

    if not BankService.authenticate(
        account_number,
        pin
    ):
        print("\n❌ Invalid account number or PIN.")
        return

    transactions = BankService.get_transactions(
        account_number
    )

    if not transactions:
        print("\nNo transactions found.")
        return

    print()

    for transaction in transactions:
        (
            transaction_id,
            transaction_type,
            amount,
            description,
            created_at
        ) = transaction

        print(
            f"[{created_at}] "
            f"{transaction_type} | "
            f"{format_money(amount)}"
        )

        print(f"  {description}")
        print()


def show_menu():
    print("""
╔══════════════════════════════════════╗
║       PYTHON BANK MANAGEMENT         ║
╠══════════════════════════════════════╣
║  1. Create Account                   ║
║  2. Check Balance                    ║
║  3. Deposit Money                    ║
║  4. Withdraw Money                   ║
║  5. Transfer Money                   ║
║  6. Transaction History              ║
║  7. Search Account                   ║
║  8. Change PIN                       ║
║  9. Delete Account                   ║
║ 10. Exit                             ║
╚══════════════════════════════════════╝
""")

def main():
    initialize_database()

    print("\nWelcome to Python Bank Management System")

    while True:
        show_menu()

        choice = input(
            "Select an option: "
        ).strip()

        if choice == "1":
            create_account()

        elif choice == "2":
            check_balance()

        elif choice == "3":
            deposit()

        elif choice == "4":
            withdraw()

        elif choice == "5":
            transfer()

        elif choice == "6":
            transaction_history()

        elif choice == "7":
            search_account()

        elif choice == "8":
            change_pin()

        elif choice == "9":
            delete_account()

        elif choice == "10":
            print("\nThank you for using Python Bank.")
            print("Goodbye! 👋")
            break

        else:
            print(
                "\n❌ Invalid option. "
                "Please select 1-10."
            )


if __name__ == "__main__":
    main()