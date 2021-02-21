import logging

logger = logging.getLogger(__name__)

def validate_solidity_type_instance(value, solidity_type):
    # Raising exceptions instead of using asserts/invariants because asserts can be disabled
    if value < 0:
        raise ValueError(f"{value} is not a {solidity_type}.")

    if value > SOLIDITY_TYPE_MAXIMA[solidity_type]:
        raise ValueError(f"{value} is not a {solidity_type}.")

def validate_and_parse_address(address):
    """ Warns if addresses are not checksummed """
    try:
        checksummed_address = get_address(address)  # TODO @ethersproject/address.getAddress

        if address != checksummed_address:
            logger.warn(f"{address} is not checksummed.")

        return checksummed_address
    except Exception as e:
        raise ValueError(f"{address} is not a valid address")

# TODO
def sqrt(y):
    pass
