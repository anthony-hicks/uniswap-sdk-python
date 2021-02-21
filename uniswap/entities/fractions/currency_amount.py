from ..token import currency_equals
from ..currency import Currency, ETHER

from ...constants import SolidityType
from ...utils import validate_solidity_type_instance
from .fraction import Fraction

class CurrencyAmount(Fraction):

    @property
    def currency(self):
        return self._currency

    @staticmethod
    def ether(amount):
        """ Helper that calls the constructor with the ETHER currency

        Args:
            amount (int): ether amount in wei
        """
        return CurrencyAmount(ETHER, amount)

    def __init__(self, currency, amount):
        """ amount _must_ be raw, i.e. in the native representation """
        validate_solidity_type_instance(amount, SolidityType.uint256)

        super().__init__(amount, 10**currency.decimals)
        self._currency = currency

    @property
    def raw(self):
        return self.numerator

    def __add__(self, other):
        if not currency_equals(self.currency, other.currency):
            raise ValueError('TOKEN')

        return CurrencyAmount(self.currency, self.raw + other.raw)

    def __sub__(self, other):
        if not currency_equals(self.currency, other.currency):
            raise ValueError('TOKEN')

        return CurrencyAmount(self.currency, self.raw - other.raw)

    # TODO
    def to_significant(self):
        pass

    # TODO
    def to_fixed(self):
        pass

    # TODO
    def to_exact(self):
        pass
