def mine_block(miner_address: str, mempool, utxo_manager, num_txs=5):
    """
    mine_block() simulates the mining of a block in our local Bitcoin-like simulator.

    USE OF THIS FUNCTION:
    - It confirms transactions from the mempool (unconfirmed pool)
    - It permanently updates the UTXO set (blockchain state)
    - It gives the miner the collected transaction fees as reward
    - It removes confirmed transactions from the mempool

    Steps followed (as mentioned in assignment):
    1) Select top transactions from mempool
    2) Update UTXO set (remove spent inputs, add new outputs)
    3) Add miner fee as a special UTXO
    4) Remove mined transactions from mempool
    """

    # Select top N transactions from mempool.
    # These are usually chosen based on highest fee first.
    selected_txs = mempool.get_top_transactions(num_txs)

    # If there are no transactions, mining cannot be done.
    if not selected_txs:
        return {
            "success": False,
            "message": "No transactions in mempool to mine.",
            "selected_count": 0,
            "total_fees": 0.0
        }

    # total_fees stores the total fees collected from all transactions in this block.
    total_fees = 0.0

    # mined_tx_ids keeps track of which transaction IDs got successfully mined.
    mined_tx_ids = []

    def calculate_fee(tx):
        """
        calculate_fee() calculates transaction fee using:
        fee = Sum(inputs) - Sum(outputs)

        WHY THIS IS NEEDED:
        - Miners earn fees for including transactions
        - Mempool sorting is usually by highest fee
        - The simulation also gives miner the total fees after mining

        Returns:
        - Fee (float) if inputs exist
        - -1.0 if any input UTXO does not exist (invalid tx)
        """
        input_sum = 0.0
        output_sum = 0.0

        # Add all input amounts by reading them from UTXO set.
        # Each input refers to an existing UTXO (prev_tx, index).
        for inp in tx["inputs"]:
            prev_tx = inp["prev_tx"]
            idx = inp["index"]

            # If UTXO does not exist, transaction is invalid.
            if not utxo_manager.exists(prev_tx, idx):
                return -1.0

            # Read amount from the UTXO set and sum it.
            amount, _ = utxo_manager.utxo_set[(prev_tx, idx)]
            input_sum += amount

        # Add all output amounts directly from transaction outputs.
        for out in tx["outputs"]:
            output_sum += out["amount"]

        # Fee = input_sum - output_sum
        return input_sum - output_sum

    # Process each selected transaction and apply it to the UTXO set.
    for tx in selected_txs:
        tx_id = tx["tx_id"]

        # Compute the fee for this transaction.
        fee = calculate_fee(tx)

        # If fee calculation returned -1.0, it means some input UTXO was missing.
        # That transaction cannot be mined.
        if fee < 0:
            continue

        # Remove (spend) all the input UTXOs because they are now used.
        # This prevents double-spending permanently (confirmed state).
        for inp in tx["inputs"]:
            utxo_manager.remove_utxo(inp["prev_tx"], inp["index"])

        # Add all outputs as new UTXOs because outputs create fresh spendable coins.
        # Each output gets an index (0, 1, 2, ...).
        for out_index, out in enumerate(tx["outputs"]):
            utxo_manager.add_utxo(
                tx_id=tx_id,
                index=out_index,
                amount=out["amount"],
                owner=out["address"]
            )

        # Add this transaction’s fee into the total fees.
        total_fees += fee

        # Store the mined transaction ID so it can be removed from mempool later.
        mined_tx_ids.append(tx_id)

    # Miner reward in this simulator = total transaction fees from the mined transactions.
    # We store this as a special UTXO owned by the miner.
    if total_fees > 0:
        utxo_manager.add_utxo(
            tx_id="miner_reward",
            index=len(mined_tx_ids),
            amount=total_fees,
            owner=miner_address
        )

    # Remove all mined transactions from mempool since they are now confirmed in a block.
    for tx_id in mined_tx_ids:
        mempool.remove_transaction(tx_id)

    # Return summary of mining results (useful for printing output in main.py)
    return {
        "success": True,
        "message": "Block mined successfully!",
        "selected_count": len(mined_tx_ids),
        "total_fees": total_fees,
        "miner": miner_address,
        "mined_tx_ids": mined_tx_ids
    }
