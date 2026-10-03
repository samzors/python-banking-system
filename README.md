Python Banking System

A command-line banking application built with Python and SQLite.

This project demonstrates core Python programming concepts, database management, authentication, transaction processing, validation, error handling, and automated testing using Python's built-in "unittest" framework.

Features

- Create bank accounts
- Generate unique 10-digit account numbers
- Secure 4-digit PIN authentication
- PIN hashing and verification
- Deposit money
- Withdraw money
- Transfer money between two accounts
- View account information
- View transaction history
- Change account PIN
- Delete bank accounts
- Search for accounts
- Input validation
- Error handling
- SQLite database storage
- Automated testing
- Automatic test-data cleanup

Technologies

- Python 3
- SQLite
- unittest
- SQL
- Object-Oriented Programming

Project Structure

python-banking-system/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── security.py
│   └── services.py
│
├── run.py
├── requirement.txt
├── test_database.py
├── test_services.py
├── .gitignore
├── README.md
└── bank.db

«"bank.db" is used locally and is excluded from GitHub through ".gitignore".»

How the Application Works

The application separates responsibilities into different modules.

Database

"database.py" handles the SQLite database connection and initialization.

Security

"security.py" handles PIN hashing and verification.

Services

"services.py" contains the main banking business logic, including:

- Account creation
- Deposits
- Withdrawals
- Transfers
- Authentication
- PIN changes
- Account deletion
- Account searches
- Transaction history

Main Application

"main.py" contains the application's user interface and banking operations.

Entry Point

"run.py" starts the banking application.

Installation

Clone the repository:

git clone https://github.com/YOUR-USERNAME/python-banking-system.git

Move into the project directory:

cd python-banking-system

Run the application:

python run.py

Running the Tests

The project uses Python's built-in "unittest" framework, so pytest is not required.

Run the service tests:

python test_services.py

Run the database tests:

python test_database.py

You can also run unittest directly:

python -m unittest

Automated Testing

The service test suite currently contains 13 automated tests covering:

- Account creation
- PIN authentication
- Deposits
- Withdrawals
- Transfers between two accounts
- Negative deposits
- Zero deposits
- Insufficient funds
- Invalid PIN
- Invalid recipient account
- Same-account transfers
- Invalid deposit amounts
- Invalid withdrawal amounts

The tests also automatically remove the accounts and transactions they create.

Example successful test result:

Ran 13 tests in 3.398s

OK

✅ Test data cleaned up.

Example Transfer Test

The automated transfer test creates two accounts:

Sender:
Initial balance: ₦50,000

Receiver:
Initial balance: ₦10,000

It then transfers:

₦15,000

Expected result:

Sender balance:   ₦35,000
Receiver balance: ₦25,000

The test confirms both balances automatically.

Security

PINs are not stored as plain text.

The project uses hashing and verification functions to protect account PINs.

The local SQLite database is also excluded from version control using ".gitignore".

Error Handling

The application validates common banking errors, including:

- Empty account names
- Invalid PIN formats
- Negative deposits
- Zero deposits
- Invalid transaction amounts
- Incorrect PINs
- Insufficient funds
- Non-existent accounts
- Transfers to the same account

Future Improvements

Possible future versions may include:

- Web-based interface
- REST API
- Admin dashboard
- User authentication system
- Email notifications
- Transaction receipts
- Improved database architecture
- PostgreSQL support
- Role-based access control
- Deployment to a cloud platform

Learning Goals

This project was built to strengthen practical Python development skills, including:

- Python functions
- Classes and object-oriented programming
- Exception handling
- SQLite databases
- SQL queries
- Password/PIN hashing
- Modular application design
- Automated testing
- Git and GitHub workflow

Author

Samuel Tombari Zorkuru

Python Developer | Frontend Developer | Student

Built as a practical Python software engineering project.

License

This project is intended for educational and portfolio purposes.