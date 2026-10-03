import unittest

from app.database import initialize_database, get_connection
from app.services import BankService


class TestBankService(unittest.TestCase):

    # Store every account created during testing
    test_accounts = []

    @classmethod
    def setUpClass(cls):
        initialize_database()
        cls.test_accounts = []

    def create_test_account(
        self,
        name,
        pin="1234",
        balance=50000
    ):
        """Create and track a test account."""

        account = BankService.create_account(
            name,
            pin,
            balance
        )

        self.__class__.test_accounts.append(
            account
        )

        return account

    def test_create_account(self):
        account = self.create_test_account(
            "Test Create"
        )

        info = BankService.get_account(account)

        self.assertIsNotNone(account)
        self.assertIsNotNone(info)

        print(
            f"\nCreated account: {account}"
        )

    def test_authentication(self):
        account = self.create_test_account(
            "Test Authentication"
        )

        self.assertTrue(
            BankService.authenticate(
                account,
                "1234"
            )
        )

        self.assertFalse(
            BankService.authenticate(
                account,
                "9999"
            )
        )

    def test_deposit(self):
        account = self.create_test_account(
            "Test Deposit",
            balance=50000
        )

        balance = BankService.deposit(
            account,
            10000
        )

        self.assertEqual(
            balance,
            60000
        )

    def test_withdrawal(self):
        account = self.create_test_account(
            "Test Withdrawal",
            balance=50000
        )

        balance = BankService.withdraw(
            account,
            "1234",
            5000
        )

        self.assertEqual(
            balance,
            45000
        )

    def test_transfer_between_two_accounts(self):
        sender = self.create_test_account(
            "Test Sender",
            "1234",
            50000
        )

        receiver = self.create_test_account(
            "Test Receiver",
            "5678",
            10000
        )

        sender_balance = BankService.transfer(
            sender,
            "1234",
            receiver,
            15000
        )

        sender_info = BankService.get_account(
            sender
        )

        receiver_info = BankService.get_account(
            receiver
        )

        # Sender:
        # 50,000 - 15,000 = 35,000
        self.assertEqual(
            sender_balance,
            35000
        )

        self.assertEqual(
            sender_info[3],
            35000
        )

        # Receiver:
        # 10,000 + 15,000 = 25,000
        self.assertEqual(
            receiver_info[3],
            25000
        )

        print(
            "\nTransfer test passed:"
        )

        print(
            "Sender balance:",
            sender_info[3]
        )

        print(
            "Receiver balance:",
            receiver_info[3]
        )

    def test_negative_deposit(self):
        account = self.create_test_account(
            "Test Negative Deposit"
        )

        with self.assertRaises(ValueError):
            BankService.deposit(
                account,
                -5000
            )

    def test_zero_deposit(self):
        account = self.create_test_account(
            "Test Zero Deposit"
        )

        with self.assertRaises(ValueError):
            BankService.deposit(
                account,
                0
            )

    def test_insufficient_funds(self):
        account = self.create_test_account(
            "Test Insufficient Funds",
            balance=5000
        )

        with self.assertRaises(ValueError):
            BankService.withdraw(
                account,
                "1234",
                10000
            )

    def test_invalid_pin(self):
        account = self.create_test_account(
            "Test Invalid PIN"
        )

        with self.assertRaises(ValueError):
            BankService.withdraw(
                account,
                "9999",
                1000
            )

    def test_invalid_account_transfer(self):
        sender = self.create_test_account(
            "Test Invalid Transfer",
            balance=50000
        )

        with self.assertRaises(ValueError):
            BankService.transfer(
                sender,
                "1234",
                "9999999999",
                5000
            )

    def test_same_account_transfer(self):
        account = self.create_test_account(
            "Test Same Account"
        )

        with self.assertRaises(ValueError):
            BankService.transfer(
                account,
                "1234",
                account,
                5000
            )

    def test_invalid_deposit_amount(self):
        account = self.create_test_account(
            "Test Invalid Deposit"
        )

        with self.assertRaises(ValueError):
            BankService.deposit(
                account,
                "abc"
            )

    def test_invalid_withdrawal_amount(self):
        account = self.create_test_account(
            "Test Invalid Withdrawal"
        )

        with self.assertRaises(ValueError):
            BankService.withdraw(
                account,
                "1234",
                "abc"
            )

    @classmethod
    def tearDownClass(cls):
        """Remove all accounts created during testing."""

        with get_connection() as connection:
            cursor = connection.cursor()

            for account in cls.test_accounts:

                # Delete transaction history
                # belonging to the test account.
                cursor.execute(
                    """
                    DELETE FROM transactions
                    WHERE account_number = ?
                    """,
                    (account,)
                )

                # Delete the test account.
                cursor.execute(
                    """
                    DELETE FROM accounts
                    WHERE account_number = ?
                    """,
                    (account,)
                )

            connection.commit()

        print(
            "\n✅ Test data cleaned up."
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )