from enum import Enum

class ChainId(Enum):
    MAINNET = 1
    ROPSTEN = 3
    RINKEBY = 4
    GÖRLI = 5
    KOVAN = 42

class SolidityType(Enum):
    uint8 = 'uint8'
    uint256 = 'uint256'

SOLIDITY_TYPE_MAXIMA = {
    SolidityType.uint8: 0xFF,
    SolidityType.uint256: 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
}
