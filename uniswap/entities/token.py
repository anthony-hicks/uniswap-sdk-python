from ..constants import ChainId
from ..utils import validate_and_parse_address
from .currency import Currency

def create_weth_token(chain_id, address):
    return Token(chain_id, address, 18, 'WETH', 'Wrapped Ether')

WETH = {
    ChainId.MAINNET: create_weth_token(ChainId.MAINNET, '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'),
    ChainId.ROPSTEN: create_weth_token(ChainId.ROPSTEN, '0xc778417E063141139Fce010982780140Aa0cD5Ab'),
    ChainId.RINKEBY: create_weth_token(ChainId.RINKEBY, '0xc778417E063141139Fce010982780140Aa0cD5Ab'),
    ChainId.GÖRLI: create_weth_token(ChainId.GÖRLI, '0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6'),
    ChainId.KOVAN: create_weth_token(ChainId.KOVAN, '0xd0A1E359811322d97991E03f863a0C30C2cF029C')
}

def currency_equals(currency_a, currency_b):
    """ Compares two currencies for equality """
    if isinstance(currency_a, Token) and isinstance(currency_b, Token):
        return currency_a == currency_b
    elif isinstance(currency_a, Token):
        return False
    elif isinstance(currency_b, Token):
        return False
    else:
        return currency_a == currency_b

class Token(Currency):

    def __init__(self, chain_id, address, decimals, symbol=None, name=None):
        super().__init__(decimals, symbol, name)
        self.chain_id = chain_id
        self.address = validate_and_parse_address(address)

    @property
    def chain_id(self):
        return self._chain_id

    @property
    def address(self):
        return self._address

    def __eq__(self, other):
        if self is other:
            return True

        return self.chain_id == other.chain_id and self.address == other.address

    def sorts_before(self, other):
        """ Returns true if the address of this token sorts before the address of the other token

        Args:
            other (Token): Other token to compare

        Throws:
            if the tokens have the same address
            if the tokens are on different chains
        """
        if self.chain_id != other.chain_id:
            raise ValueError('CHAIN_IDS')

        if self.address == other.address:
            raise ValueError('ADDRESSES')

        return self.address.lower() < other.address.lower()
