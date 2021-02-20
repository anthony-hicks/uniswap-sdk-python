# TODO: Don't lock in to infura
from web3.auto.infura import w3

TOKEN_DECIMALS_CACHE = {
    CHAIN.MAINNET: {
        '0xE0B7927c4aF23765Cb51314A0E0521A9645F0E2A': 9  // DGD
    }
}

# TODO: Prob don't need a class
class Fetcher:

    # TODO: Type annotations
    # TODO: default provider/get_network
    def fetch_token_data(chain_id, address, provider=None, symbol=None, name=None):
        # Check if number of decimals is already in the cache TODO
        # else
        if False:
            pass
        else:
            TOKEN_DECIMALS_CACHE[chain_id][address] = w3.eth.contract(address, abi=ABI['ERC20']).functions.decimals().call()
        decimals = TOKEN_DECIMALS_CACHE[chain_id][address]

        return Token(chain_id, address, decimals, symbol, name)

    # TODO: default provider/network
    def fetch_pair_data(token_a, token_b, provider=None):
        address = Pair.get_address(token_a, token_b)
        reserves = w3.eth.contract(address, abi=ABI['IUniswapV2Pair']).functions.getReserves().call()

        # TODO: sortBefore? Why can't we just return a, b? Why would we want to ret b, a?
        return Pair(TokenAmount(token_a, reserves[0]), TokenAmount(token_b, reserves[1]))
