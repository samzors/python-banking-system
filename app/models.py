from dataclasses import dataclass
from typing import Optional


@dataclass
class Account:
    """Represents a bank account."""

    id: Optional[int]
    name: str
    account_number: str
    balance: int
    created_at: Optional[str] = None


@dataclass
class Transaction:
    """Represents a bank transaction."""

    id: Optional[int]
    account_number: str
    transaction_type: str
    amount: int
    description: Optional[str] = None
    created_at: Optional[str] = None