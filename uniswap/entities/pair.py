from collections import defaultdict

from abi import ABI
from contracts import IUniswapV2Factory

PAIR_ADDRESS_CACHE = defaultdict(dict)

# TODO: I don't like having to do .functions.
class Pair:
    def __init__(self, amount_a, amount_b):
        self.liquidity_token = Token(
            amount_a.token.chain_id,
            Pair.get_address(amount_a.token, amount_b.token),
            18,
            'UNI-V2',
            'Uniswap V2'
        )
        self.token_amounts = (amount_a, amount_b)

    @staticmethod
    def get_address(token_a, token_b):
        tokens = [token_a, token_b] if token_a.sorts_before(token_b) else [token_b, token_a]  # does safety checks

        if False:
            pass # TODO: Check cache
        else:
            # TODO
            pair = w3.eth.contract(
                address=IUniswapV2Factory.functions.getPair(tokens[0].address, tokens[1].address).call(),
                abi=ABI['IUniswapV2Pair']
            )
            PAIR_ADDRESS_CACHE[tokens[0].address][tokens[1].address] = pair.address
            return pair.address

    def involves_token(self, token):
        return token in (self.token0, self.token1)

    def token0_price(self):
        return Price(self.token0, self.token1, self.token_amounts[0].raw, self.token_amounts[1].raw)

    def token1_price(self):
        return Price(self.token1, self.token0, self.token_amounts[1].raw, self.token_amounts[0].raw)

    def price_of(self, token):
        # invariant(this.involvesToken(token), 'TOKEN') TODO
        return self.token0_price if token == self.token0 else self.token1_price

    # TODO: properties
    def chain_id(self):
        return self.token0.chain_id

    # TODO: Use pair.a, pair.b interface instead of token0, token1
    # TODO: Use pair.amounts instead of pair.token_amounts
    def token0(self):
        return self.token_amounts[0].token

    def token1(self):
        return self.token_amounts[1].token

    def reserve0(self):
        return self.token_amounts[0]

    def reserve1(self):
        return self.token_amounts[1]

    def reserve_of(self, token):
        # invariant(this.involvesToken(token), 'TOKEN')
        return self.reserve0 if token == self.token0 else self.reserve1

    def get_output_amount(self, input_amount):
        # invariant(this.involvesToken(inputAmount.token), 'TOKEN')
        # if (JSBI.equal(this.reserve0.raw, ZERO) || JSBI.equal(this.reserve1.raw, ZERO))
        #   throw new InsufficientReservesError()

        input_reserve = self.reserve_of(input_amount.token)
        output_reserve = self.reserve_of(self.token1 if input_amount.token == self.token0 else self.token0)

        # const inputAmountWithFee = JSBI.multiply(inputAmount.raw, _997)
        # const numerator = JSBI.multiply(inputAmountWithFee, outputReserve.raw)
        # const denominator = JSBI.add(JSBI.multiply(inputReserve.raw, _1000), inputAmountWithFee)
        # const outputAmount = new TokenAmount(
        # inputAmount.token.equals(this.token0) ? this.token1 : this.token0,
        # JSBI.divide(numerator, denominator)
        # )
        # if (JSBI.equal(outputAmount.raw, ZERO)) {
        # throw new InsufficientInputAmountError()
        # }
        # return [outputAmount, new Pair(inputReserve.add(inputAmount), outputReserve.subtract(outputAmount))]

    def get_input_amount(self, output_amount):
        # invariant(this.involvesToken(outputAmount.token), 'TOKEN')
        # if (
        # JSBI.equal(this.reserve0.raw, ZERO) ||
        # JSBI.equal(this.reserve1.raw, ZERO) ||
        # JSBI.greaterThanOrEqual(outputAmount.raw, this.reserveOf(outputAmount.token).raw)
        # ) {
        # throw new InsufficientReservesError()
        # }

        # const outputReserve = this.reserveOf(outputAmount.token)
        # const inputReserve = this.reserveOf(outputAmount.token.equals(this.token0) ? this.token1 : this.token0)
        # const numerator = JSBI.multiply(JSBI.multiply(inputReserve.raw, outputAmount.raw), _1000)
        # const denominator = JSBI.multiply(JSBI.subtract(outputReserve.raw, outputAmount.raw), _997)
        # const inputAmount = new TokenAmount(
        # outputAmount.token.equals(this.token0) ? this.token1 : this.token0,
        # JSBI.add(JSBI.divide(numerator, denominator), ONE)
        # )
        # return [inputAmount, new Pair(inputReserve.add(inputAmount), outputReserve.subtract(outputAmount))]

    def get_liquidity_minted(self, total_supply, token_amount_a, token_amount_b):
        # invariant(totalSupply.token.equals(this.liquidityToken), 'LIQUIDITY')
        # const tokenAmounts = tokenAmountA.token.sortsBefore(tokenAmountB.token) // does safety checks
        # ? [tokenAmountA, tokenAmountB]
        # : [tokenAmountB, tokenAmountA]
        # invariant(tokenAmounts[0].token.equals(this.token0) && tokenAmounts[1].token.equals(this.token1), 'TOKEN')

        # let liquidity: JSBI
        # if (JSBI.equal(totalSupply.raw, ZERO)) {
        # liquidity = JSBI.subtract(sqrt(JSBI.multiply(tokenAmounts[0].raw, tokenAmounts[1].raw)), MINIMUM_LIQUIDITY)
        # } else {
        # const amount0 = JSBI.divide(JSBI.multiply(tokenAmounts[0].raw, totalSupply.raw), this.reserve0.raw)
        # const amount1 = JSBI.divide(JSBI.multiply(tokenAmounts[1].raw, totalSupply.raw), this.reserve1.raw)
        # liquidity = JSBI.lessThanOrEqual(amount0, amount1) ? amount0 : amount1
        # }
        # if (!JSBI.greaterThan(liquidity, ZERO)) {
        # throw new InsufficientInputAmountError()
        # }
        # return new TokenAmount(this.liquidityToken, liquidity)

    def get_liquidity_value(self, token, total_supply, liquidity, fee_on=False, k_last=None):
        # invariant(this.involvesToken(token), 'TOKEN')
        # invariant(totalSupply.token.equals(this.liquidityToken), 'TOTAL_SUPPLY')
        # invariant(liquidity.token.equals(this.liquidityToken), 'LIQUIDITY')
        # invariant(JSBI.lessThanOrEqual(liquidity.raw, totalSupply.raw), 'LIQUIDITY')

        # let totalSupplyAdjusted: TokenAmount
        # if (!feeOn) {
        # totalSupplyAdjusted = totalSupply
        # } else {
        # invariant(!!kLast, 'K_LAST')
        # const kLastParsed = parseBigintIsh(kLast)
        # if (!JSBI.equal(kLastParsed, ZERO)) {
        #     const rootK = sqrt(JSBI.multiply(this.reserve0.raw, this.reserve1.raw))
        #     const rootKLast = sqrt(kLastParsed)
        #     if (JSBI.greaterThan(rootK, rootKLast)) {
        #     const numerator = JSBI.multiply(totalSupply.raw, JSBI.subtract(rootK, rootKLast))
        #     const denominator = JSBI.add(JSBI.multiply(rootK, FIVE), rootKLast)
        #     const feeLiquidity = JSBI.divide(numerator, denominator)
        #     totalSupplyAdjusted = totalSupply.add(new TokenAmount(this.liquidityToken, feeLiquidity))
        #     } else {
        #     totalSupplyAdjusted = totalSupply
        #     }
        # } else {
        #     totalSupplyAdjusted = totalSupply
        # }
        # }

        # return new TokenAmount(
        # token,
        # JSBI.divide(JSBI.multiply(liquidity.raw, this.reserveOf(token).raw), totalSupplyAdjusted.raw)
        # )
