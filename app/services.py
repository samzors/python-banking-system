import random

from .database import get_connection
from .security import hash_pin, verify_pin


class BankService:
    """Business logic for the banking application."""

    @staticmethod
    def generate_account_number():
        """Generate a unique 10-digit account number."""

        with get_connection() as connection:
            cursor = connection.cursor()

            while True:
                account_number = str(
                    random.randint(1000000000, 9999999999)
                )

                cursor.execute(
                    """
                    SELECT 1
                    FROM accounts
                    WHERE account_number = ?
                    """,
                    (account_number,)
                )

                if cursor.fetchone() is None:
                    return account_number

    @staticmethod
    def validate_pin(pin):
        """Validate a 4-digit PIN."""

        pin = str(pin)

        return pin.isdigit() and len(pin) == 4

    @staticmethod
    def create_account(name, pin, initial_deposit=0):
        """Create a new bank account."""

        name = name.strip()

        if not name:
            raise ValueError("Name cannot be empty.")

        if not BankService.validate_pin(pin):
            raise ValueError("PIN must be exactly 4 digits.")

        try:
            initial_deposit = int(initial_deposit)
        except (ValueError, TypeError):
            raise ValueError(
                "Initial deposit must be a valid amount."
            )

        if initial_deposit < 0:
            raise ValueError(
                "Initial deposit cannot be negative."
            )

        account_number = BankService.generate_account_number()
        pin_hash = hash_pin(str(pin))

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO accounts
                (name, account_number, pin_hash, balance)
                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    account_number,
                    pin_hash,
                    initial_deposit
                )
            )

            if initial_deposit > 0:
                cursor.execute(
                    """
                    INSERT INTO transactions
                    (
                        account_number,
                        transaction_type,
                        amount,
                        description
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        account_number,
                        "DEPOSIT",
                        initial_deposit,
                        "Initial deposit"
                    )
                )

            connection.commit()

        return account_number

    @staticmethod
    def get_account(account_number):
        """Get account information."""

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    account_number,
                    balance,
                    created_at
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            return cursor.fetchone()

    @staticmethod
    def authenticate(account_number, pin):
        """Verify account number and PIN."""

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT pin_hash
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            result = cursor.fetchone()

        if not result:
            return False

        return verify_pin(
            str(pin),
            result[0]
        )

    @staticmethod
    def deposit(account_number, amount):
        """Deposit money into an account."""

        try:
            amount = int(amount)
        except (ValueError, TypeError):
            raise ValueError(
                "Amount must be a valid number."
            )

        if amount <= 0:
            raise ValueError(
                "Deposit amount must be greater than zero."
            )

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT balance
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            account = cursor.fetchone()

            if not account:
                raise ValueError("Account not found.")

            new_balance = account[0] + amount

            cursor.execute(
                """
                UPDATE accounts
                SET balance = ?
                WHERE account_number = ?
                """,
                (
                    new_balance,
                    account_number
                )
            )

            cursor.execute(
                """
                INSERT INTO transactions
                (
                    account_number,
                    transaction_type,
                    amount,
                    description
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    account_number,
                    "DEPOSIT",
                    amount,
                    "Cash deposit"
                )
            )

            connection.commit()

        return new_balance

    @staticmethod
    def withdraw(account_number, pin, amount):
        """Withdraw money from an account."""

        if not BankService.authenticate(
            account_number,
            pin
        ):
            raise ValueError("Incorrect PIN.")

        try:
            amount = int(amount)
        except (ValueError, TypeError):
            raise ValueError(
                "Amount must be a valid number."
            )

        if amount <= 0:
            raise ValueError(
                "Withdrawal amount must be greater than zero."
            )

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT balance
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            account = cursor.fetchone()

            if not account:
                raise ValueError("Account not found.")

            balance = account[0]

            if amount > balance:
                raise ValueError("Insufficient funds.")

            new_balance = balance - amount

            cursor.execute(
                """
                UPDATE accounts
                SET balance = ?
                WHERE account_number = ?
                """,
                (
                    new_balance,
                    account_number
                )
            )

            cursor.execute(
                """
                INSERT INTO transactions
                (
                    account_number,
                    transaction_type,
                    amount,
                    description
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    account_number,
                    "WITHDRAWAL",
                    amount,
                    "Cash withdrawal"
                )
            )

            connection.commit()

        return new_balance

    @staticmethod
    def transfer(from_account, pin, to_account, amount):
        """Transfer money between two accounts."""

        if from_account == to_account:
            raise ValueError(
                "Cannot transfer to the same account."
            )

        if not BankService.authenticate(
            from_account,
            pin
        ):
            raise ValueError("Incorrect PIN.")

        try:
            amount = int(amount)
        except (ValueError, TypeError):
            raise ValueError(
                "Amount must be a valid number."
            )

        if amount <= 0:
            raise ValueError(
                "Transfer amount must be greater than zero."
            )

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT balance
                FROM accounts
                WHERE account_number = ?
                """,
                (from_account,)
            )

            sender = cursor.fetchone()

            if not sender:
                raise ValueError(
                    "Sender account not found."
                )

            cursor.execute(
                """
                SELECT balance
                FROM accounts
                WHERE account_number = ?
                """,
                (to_account,)
            )

            recipient = cursor.fetchone()

            if not recipient:
                raise ValueError(
                    "Recipient account not found."
                )

            sender_balance = sender[0]

            if amount > sender_balance:
                raise ValueError(
                    "Insufficient funds."
                )

            new_sender_balance = (
                sender_balance - amount
            )

            new_recipient_balance = (
                recipient[0] + amount
            )

            cursor.execute(
                """
                UPDATE accounts
                SET balance = ?
                WHERE account_number = ?
                """,
                (
                    new_sender_balance,
                    from_account
                )
            )

            cursor.execute(
                """
                UPDATE accounts
                SET balance = ?
                WHERE account_number = ?
                """,
                (
                    new_recipient_balance,
                    to_account
                )
            )

            cursor.execute(
                """
                INSERT INTO transactions
                (
                    account_number,
                    transaction_type,
                    amount,
                    description
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    from_account,
                    "TRANSFER_OUT",
                    amount,
                    f"Transfer to {to_account}"
                )
            )

            cursor.execute(
                """
                INSERT INTO transactions
                (
                    account_number,
                    transaction_type,
                    amount,
                    description
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    to_account,
                    "TRANSFER_IN",
                    amount,
                    f"Transfer from {from_account}"
                )
            )

            connection.commit()

        return new_sender_balance

    @staticmethod
    def get_transactions(account_number):
        """Return transaction history."""

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    transaction_type,
                    amount,
                    description,
                    created_at
                FROM transactions
                WHERE account_number = ?
                ORDER BY id DESC
                """,
                (account_number,)
            )

            return cursor.fetchall()

    @staticmethod
    def change_pin(account_number, old_pin, new_pin):
        """Change an account PIN."""

        if not BankService.authenticate(
            account_number,
            old_pin
        ):
            raise ValueError("Incorrect current PIN.")

        if not BankService.validate_pin(new_pin):
            raise ValueError(
                "New PIN must be exactly 4 digits."
            )

        if str(old_pin) == str(new_pin):
            raise ValueError(
                "New PIN cannot be the same as the old PIN."
            )

        new_pin_hash = hash_pin(str(new_pin))

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE accounts
                SET pin_hash = ?
                WHERE account_number = ?
                """,
                (
                    new_pin_hash,
                    account_number
                )
            )

            connection.commit()

        return True

    @staticmethod
    def delete_account(account_number, pin):
        """Delete an account after PIN authentication."""

        if not BankService.authenticate(
            account_number,
            pin
        ):
            raise ValueError("Incorrect PIN.")

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            if cursor.rowcount == 0:
                raise ValueError("Account not found.")

            connection.commit()

        return True

    @staticmethod
    def search_account(account_number):
        """Search for an account."""

        account = BankService.get_account(
            account_number
        )

        if not account:
            raise ValueError("Account not found.")

        return account