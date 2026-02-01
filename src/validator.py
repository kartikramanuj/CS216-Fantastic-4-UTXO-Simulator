# src/validator.py

def validate_transaction(tx, utxo_manager, mempool):
    """
    Validates a transaction and calculates the fee.
    Returns: (is_valid: bool, result: float|str)
    """
    input_sum = 0.0
    output_sum = 0.0

    # 1. Validate Inputs
    for inp in tx["inputs"]:
        key = (inp["prev_tx"], inp["index"])
        
        # Check Ledger (UTXO Set)
        if key not in utxo_manager.utxo_set:
            return False, f"Input {key} does not exist or already spent in Ledger."
        
        # Check Mempool (Double Spend Prevention)
        # We access 'mempool' passed as argument, no import needed!
        if key in mempool.spent_utxos:
            return False, f"Input {key} is already pending in Mempool."

        # Verify Owner
        utxo = utxo_manager.utxo_set[key]
        if utxo["owner"] != inp["owner"]:
            return False, f"Sender is not the owner of input {key}."
        
        input_sum += utxo["amount"]

    # 2. Validate Outputs
    for out in tx["outputs"]:
        if out["amount"] <= 0:
            return False, "Output amount must be positive."
        output_sum += out["amount"]

    # 3. Calculate Fee
    if output_sum > input_sum:
        return False, "Insufficient inputs for outputs."
    
    fee = input_sum - output_sum
    
    # Return True and the Fee (as required by your Mempool code)
    return True, fee