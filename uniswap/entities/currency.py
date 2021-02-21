from ..utils import validate_solidity_type_instance
from ..constants import SolidityType

class Currency:
    """ A currency is any fungible financial instrument on Ethereum, including Ether and all ERC20 tokens.

    The only instance of the base class `Currency` is Ether.
    """

    def __init__(self, decimals, symbol=None, name=None):
        validate_solidity_type_instance(decimals, SolidityType.uint8)

        self._decimals = decimals
        self._symbol = symbol
        self._name = name

    @property
    def decimals(self):
        return self._decimals

    @property
    def symbol(self):
        return self._symbol

    @property
    def name(self):
        return self._name

# The only instance of the base class `Currency`
ETHER = Currency(decimals=18, symbol='ETH', name='Ether')
