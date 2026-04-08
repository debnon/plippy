from decimal import Decimal

import pytest

from StandardUser import StandardUser


def test_deposit_increases_funds() -> None:
    user = StandardUser("ben")

    user.deposit(Decimal("100.96"))

    assert user.funds == Decimal("100.96")


@pytest.mark.parametrize("amount", [Decimal("0"), Decimal("-1.00")])
def test_deposit_rejects_non_positive_values(amount: Decimal) -> None:
    user = StandardUser("ben")

    with pytest.raises(ValueError, match="greater than 0"):
        user.deposit(amount)


def test_get_name_returns_name() -> None:
    user = StandardUser("ben")

    assert user.getName() == "ben"