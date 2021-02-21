def validate_solidity_type_instance(value, solidity_type):
    # Raising exceptions instead of using asserts/invariants because asserts can be disabled
    if value < 0:
        raise ValueError(f"{value} is not a {solidity_type}.")

    if value > SOLIDITY_TYPE_MAXIMA[solidity_type]:
        raise ValueError(f"{value} is not a {solidity_type}.")
