from ..constants import ChainId

from .currency import Currency, ETHER
from .token import Token, WETH
from .pair import Pair
from .fractions.price import Price

class Route:

    def __init__(self, pairs, input, output=None):
        if len(pairs) == 0:
            raise ValueError('PAIRS')

        if any(pair.chain_id != pairs[0].chain_id for pair in pairs):
            raise ValueError('CHAIN_IDS')

        if (not isinstance(input, Token) or not pairs[0].involves_token(input)) and (input is not ETHER or not pairs[0].involves_token(WETH[pairs[0].chain_id])):
            raise ValueError('INPUT')

        if (output is not None) and (not isinstance(output, Token) or not pairs[-1].involves_token(output)) and (output is not ETHER or not pairs[-1].involves_token(WETH[pairs[0].chain_id])):
            raise ValueError('OUTPUT')

        path = [input if isinstance(input, Token) else WETH[pairs[0].chain_id]]
        for i, pair in enumerate(pairs):
            current_input = path[i]

            # TODO: Could use pair.involves_token here
            if current_input != pair.token0 and current_input != pair.token1:
                raise Exception('PATH')

            output = pair.token1 if current_input == pair.token0 else pair.token0
            path.append(output)

        self._pairs = pairs
        self._path = path
        self._mid_price = Price.from_route(self)
        self._input = input
        self._output = output or path[-1]

    @property
    def pairs(self):
        return self._pairs

    @property
    def path(self):
        return self._path

    @property
    def mid_price(self):
        return self._mid_price

    @property
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output

    @property
    def chain_id(self):
        return self.pairs[0].chain_id
