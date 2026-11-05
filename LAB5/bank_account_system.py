"""Bank account management module providing ledger operations and auditing."""

import hashlib
import os
import secrets
from typing import Any, Dict, List, Optional

account_data: Dict[str, Dict[str, Any]] = {}


def create_account(
    acc_id: str,
    name: str,
    initial_deposit: float = 0.0,
    transactions: Optional[List[str]] = None,
) -> bool:
    """Create a new bank account with an initial deposit.

    Args:
        acc_id: Unique account identifier.
        name: Name of the account owner.
        initial_deposit: Starting balance.
        transactions: Optional list of prior transactions.

    Returns:
        bool: True if created, False if account already exists.
    """
    if acc_id in account_data:
        return False
    if transactions is None:
        transactions = []
    account_data[acc_id] = {"name": name, "balance": float(initial_deposit)}
    transactions.append(
        f"Created {acc_id} with initial balance {initial_deposit}"
    )
    return True


def deposit(acc_id: str, amount: float) -> bool:
    """Deposit a positive amount into an account.

    Args:
        acc_id: Target account identifier.
        amount: Amount to deposit.

    Returns:
        bool: True if deposit succeeded, False otherwise.
    """
    if amount <= 0:
        return False
    try:
        account_data[acc_id]["balance"] += amount
        return True
    except KeyError:
        return False


def withdraw(acc_id: str, amount: float, apply_fee: bool = False) -> bool:
    """Withdraw an amount from an account.

    Args:
        acc_id: Target account identifier.
        amount: Amount to withdraw.
        apply_fee: Whether standard service fee applies.

    Returns:
        bool: True if withdrawal succeeded, False otherwise.
    """
    service_fee = 2.50 if apply_fee else 0.0
    if acc_id not in account_data:
        return False
    total_deduction = amount + service_fee
    if account_data[acc_id]["balance"] < total_deduction:
        return False
    account_data[acc_id]["balance"] -= total_deduction
    return True


def compute_bonus(acc_id: str, rate_or_multiplier: Any = 0.05) -> float:
    """Compute promotional bonus for an account safely without eval().

    Args:
        acc_id: Target account identifier.
        rate_or_multiplier: Multiplier float or multiplier expression.

    Returns:
        float: Calculated bonus amount.
    """
    bal = account_data[acc_id]["balance"]
    if isinstance(rate_or_multiplier, (int, float)):
        return bal * float(rate_or_multiplier)
    if isinstance(rate_or_multiplier, str):
        cleaned = (
            rate_or_multiplier.replace("bal", "").replace("*", "").strip()
        )
        try:
            factor = float(cleaned)
            return bal * factor
        except ValueError:
            return 0.0
    return 0.0


def get_hash(pin: str) -> str:
    """Compute a SHA-256 hash digest for a given PIN string.

    Args:
        pin: PIN or password string.

    Returns:
        str: Hexadecimal SHA-256 digest.
    """
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def generate_temp_pin() -> int:
    """Generate a cryptographically secure 4-digit temporary PIN.

    Returns:
        int: Random integer between 1000 and 9999 inclusive.
    """
    return secrets.randbelow(9000) + 1000


def backup_data(filename: str = "backup.txt") -> None:
    """Write current account data to a backup file and log status safely.

    Args:
        filename: Destination path for the backup file.
    """
    with open(filename, "w", encoding="utf-8") as backup_file:
        backup_file.write(str(account_data))
    print(f"Backup complete: {filename}")


def main() -> None:
    """Main execution entry point demonstrating banking features."""
    admin_token = os.getenv("ADMIN_AUTH_TOKEN", "LOCAL_DEV_DEFAULT_TOKEN")
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", "bal * 0.05"))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()
    print("Token initialized:", admin_token)


if __name__ == "__main__":
    main()
