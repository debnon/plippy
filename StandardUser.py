from decimal import Decimal


class StandardUser:
    """"User class"""

    name: str = "example"
    funds: Decimal = Decimal("0.00")

    def __init__(self, name: str = name):
        self.name = name

    @staticmethod
    def _validate_positive_amount(value: Decimal, action: str) -> Decimal:
        if value <= 0:
            raise ValueError(f"{action} amount must be greater than 0")
        return value

    def deposit(self, deposit: Decimal) -> Decimal:
        deposit = self._validate_positive_amount(deposit, "Deposit")
        self.funds += deposit
        return deposit
    
    # @classmethod
    def getName(self) -> str:
        return self.name

