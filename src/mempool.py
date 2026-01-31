from validator import validate_transaction

class Mempool:
    def __init__(self, max_size=50):
        self.transactions = []         
        self.spent_utxos = set()       
        self.max_size = max_size

    def add_transaction(self, tx, utxo_manager):
        valid, result = validate_transaction(tx, utxo_manager, self)
        if not valid:
            return False, result
        
        fee = result 

        for inp in tx["inputs"]:
            utxo_key = (inp["prev_tx"], inp["index"])
            if utxo_key in self.spent_utxos:
                return False, f"UTXO {utxo_key} already spent in mempool"

        tx["fee"] = fee
        self.transactions.append(tx)

        for inp in tx["inputs"]:
            self.spent_utxos.add((inp["prev_tx"], inp["index"]))

        if len(self.transactions) > self.max_size:
            self._evict_lowest_fee_tx()

        return True, "Transaction added to mempool"

    def _evict_lowest_fee_tx(self):
        lowest_tx = min(self.transactions, key=lambda t: t["fee"])
        self.remove_transaction(lowest_tx["tx_id"])

    def remove_transaction(self, tx_id):
        for tx in self.transactions:
            if tx["tx_id"] == tx_id:
                for inp in tx["inputs"]:
                    utxo_key = (inp["prev_tx"], inp["index"])
                    if utxo_key in self.spent_utxos:
                        self.spent_utxos.remove(utxo_key)

                self.transactions.remove(tx)
                return

    def get_top_transactions(self, n):
        sorted_txs = sorted(
            self.transactions,
            key=lambda t: t["fee"],
            reverse=True
        )
        return sorted_txs[:n]

    def clear(self):
        self.transactions.clear()
        self.spent_utxos.clear()
