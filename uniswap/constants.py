from enum import Enum

class SolidityType(Enum):
    uint8 = 'uint8'
    uint256 = 'uint256'

SOLIDITY_TYPE_MAXIMA = {
    SolidityType.uint8: 0xFF,
    SolidityType.uint256: 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
}
