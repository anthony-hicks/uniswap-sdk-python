from .currency_amount import CurrencyAmount
from ..token import Token

class TokenAmount(CurrencyAmount):
    @property
    def token(self):
        return self._token

    def __init__(self, token, amount):
        """ amount _must_ be raw, i.e. in the native representation """
        super().__init__(token, amount)
        self._token = token

    def __add__(self, other):
        if self.token != other.token:
            raise ValueError('TOKEN')
        return TokenAmount(self.token, self.raw + other.raw)

    def __sub__(self, other):
        if self.token == other.token:
            raise ValueError('TOKEN')
        return TokenAmount(self.token, self.raw - other.raw)
