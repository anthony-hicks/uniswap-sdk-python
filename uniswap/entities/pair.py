from collections import defaultdict

from .fractions.token_amount import TokenAmount

from ..constants import MINIMUM_LIQUIDITY, ChainId
from ..utils import sqrt

from abi import ABI
from contracts import IUniswapV2Factory


PAIR_ADDRESS_CACHE = defaultdict(dict)

class Pair:

    @property
    def liquidity_token(self):
        return self._liquidity_token

    def __init__(self, amount_a, amount_b):
        token_amounts = [amount_a, amount_b] if amount_a.token.sorts_before(amount_b.token) else [amount_b, amount_a]

        self.liquidity_token = Token(
            token_amounts[0].token.chain_id,
            Pair.get_address(token_amounts[0].token, token_amounts[1].token),
            18,
            'UNI-V2',
            'Uniswap V2'
        )
        self._token_amounts = token_amounts

    @staticmethod
    def get_address(token_a, token_b):
        tokens = [token_a, token_b] if token_a.sorts_before(token_b) else [token_b, token_a]  # does safety checks

        try:
            pair = PAIR_ADDRESS_CACHE[tokens[0].address][tokens[1].address]
        except KeyError:
            # TODO: Original used ethersproject/address::getCreate2Address with keccak256 from ethersproject/solidity
            pair = w3.eth.contract(
                address=IUniswapV2Factory.functions.getPair(tokens[0].address, tokens[1].address).call(),
                abi=ABI['IUniswapV2Pair']
            )
            PAIR_ADDRESS_CACHE[tokens[0].address][tokens[1].address] = pair.address

        return pair.address

    def involves_token(self, token):
        """ Returns true if the token is either token0 or token1

        Args:
            token (Token): token to check
        """
        return token == self.token0 or token == self.token1

    def token0_price(self):
        """ Returns the current mid price of the pair in terms of token0, i.e. the ratio of reserve1 to reserve0 """
        return Price(self.token0, self.token1, self._token_amounts[0].raw, self._token_amounts[1].raw)

    def token1_price(self):
        """ Returns the current mid price of the pair in terms of token1, i.e. the ratio of reserve0 to reserve1 """
        return Price(self.token1, self.token0, self._token_amounts[1].raw, self._token_amounts[0].raw)

    def price_of(self, token):
        """ Returns the price of the given token in terms of the other token in the pair.

        Args:
            token (Token): token to return price of
        """
        if not self.involves_token(token):
            raise ValueError('TOKEN')

        return self.token0_price if token == self.token0 else self.token1_price

    @property
    def chain_id(self):
        return self.token0.chain_id

    # TODO: Use pair.a, pair.b interface instead of token0, token1
    # TODO: Use pair.amounts instead of pair._token_amounts
    @property
    def token0(self):
        return self._token_amounts[0].token

    @property
    def token1(self):
        return self._token_amounts[1].token

    @property
    def reserve0(self):
        return self._token_amounts[0]

    @property
    def reserve1(self):
        return self._token_amounts[1]

    def reserve_of(self, token):
        if not self.involves_token(token):
            raise ValueError('TOKEN')

        return self.reserve0 if token == self.token0 else self.reserve1

    def get_output_amount(self, input_amount):
        if not self.involves_token(input_amount.token):
            raise ValueError('TOKEN')

        if self.reserve0.raw == 0 or self.reserve1.raw == 0:
            raise InsufficientReservesError()

        input_reserve = self.reserve_of(input_amount.token)
        output_reserve = self.reserve_of(self.token1 if input_amount.token == self.token0 else self.token0)

        input_amount_with_fee = input_amount.raw * 997
        numerator = input_amount_with_fee * output_reserve.raw
        denominator = (input_reserve.raw * 1000) + input_amount_with_fee

        output_amount = TokenAmount(
            self.token1 if input_amount.token == self.token0 else self.token0,
            numerator / denominator
        )

        if output_amount == 0:
            raise InsufficientInputAmountError()

        return [output_amount, Pair(input_reserve + input_amount, output_reserve - output_amount)]

    def get_input_amount(self, output_amount):
        if not self.involves_token(output_amount.token):
            raise ValueError('TOKEN')

        if self.reserve0.raw == 0 or self.reserve1.raw == 0 or output_amount.raw > self.reserve_of(output_amount.token).raw:
            raise InsufficientReservesError()

        output_reserve = self.reserve_of(output_amount.token)
        input_reserve = self.reserve_of(self.token1 if output_amount.token == self.token0 else self.token0)

        numerator = (input_reserve.raw * output_amount.raw) * 1000
        denominator = (output_reserve.raw - output_amount.raw) * 997

        input_amount = TokenAmount(
            self.token1 if output_amount.token == self.token0 else self.token0,
            (numerator/denominator) + 1
        )
        return [input_amount, Pair(input_reserve + input_amount, output_reserve - output_amount)]

    def get_liquidity_minted(self, total_supply, token_amount_a, token_amount_b):
        if not total_supply.token == self.liquidity_token:
            raise ValueError('LIQUIDITY')

        token_amounts = [token_amount_a, token_amount_b] if token_amount_a.token.sorts_before(token_amount_b.token) else [token_amount_b, token_amount_a]

        if token_amounts[0].token != self.token0 or token_amounts[1].token != self.token1:
            raise ValueError('TOKEN')

        if total_supply.raw == 0:
            liquidity = sqrt(token_amounts[0].raw * token_amounts[1].raw) - MINIMUM_LIQUIDITY
        else:
            amount0 = (token_amounts[0].raw * total_supply.raw) / self.reserve0.raw
            amount1 = (token_amounts[1].raw * total_supply.raw) / self.reserve1.raw
            liquidity = amount0 if amount0 <= amount1 else amount1

        if liquidity <= 0:
            raise InsufficientInputAmountError()

        return TokenAmount(self.liquidity_token, liquidity)

    def get_liquidity_value(self, token, total_supply, liquidity, fee_on=False, k_last=None):
        if not self.involves_token(token):
            raise ValueError('TOKEN')

        if not total_supply.token == self.liquidity_token:
            raise ValueError('TOTAL_SUPPLY')

        if not liquidity.token == self.liquidity_token:
            raise ValueError('LIQUIDITY')

        if liquidity.raw > total_supply.raw:
            raise ValueError('LIQUIDITY')

        if not fee_on:
            total_supply_adjusted = total_supply
        else:
            if not k_last:
                raise ValueError('K_LAST')

            if k_last != 0:
                root_k = sqrt(self.reserve0.raw * self.reserve1.raw)
                root_k_last = sqrt(k_last)

                if root_k > root_k_last:
                    numerator = total_supply.raw * (root_k - root_k_last)
                    denominator = (root_k * 5) + root_k_last

                    fee_liquidity = numerator / denominator
                    total_supply_adjusted = total_supply + TokenAmount(self.liquidity_token, fee_liquidity)
                else:
                    total_supply_adjusted = total_supply
            else:
                total_supply_adjusted = total_supply

        return TokenAmount(token, (liquidity.raw * self.reserve_of(token).raw) / total_supply_adjusted.raw)
