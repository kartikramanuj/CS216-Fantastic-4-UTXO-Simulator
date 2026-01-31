class UTXOManager:
    def __init__(self):
        
        self.utxo_set = {}

    def add_utxo(self, tx_id: str, index: int, amount: float, owner: str):
       
        key = (tx_id, index)
        self.utxo_set[key] = {'amount': amount, 'owner': owner}

    def remove_utxo(self, tx_id: str, index: int):
        
        key = (tx_id, index)
        if key in self.utxo_set:
            del self.utxo_set[key]
        else:
           
            print(f"Warning: Attempted to remove non-existent UTXO {key}")

    def get_balance(self, owner: str) -> float:
       
        balance = 0.0
        for utxo_data in self.utxo_set.values():
            if utxo_data['owner'] == owner:
                balance += utxo_data['amount']
        return balance

    def exists(self, tx_id: str, index: int) -> bool:
       
        return (tx_id, index) in self.utxo_set

    def get_utxos_for_owner(self, owner: str) -> list:
       
        owned_utxos = []
        for (tx_id, idx), data in self.utxo_set.items():
            if data['owner'] == owner:
                owned_utxos.append({
                    'tx_id': tx_id,
                    'output_index': idx,
                    'amount': data['amount']
                })
        return owned_utxos
    
ledger = UTXOManager()

ledger.add_utxo(tx_id="genesis", index=0, amount=50.0, owner="Alice")
ledger.add_utxo(tx_id="genesis", index=1, amount=30.0, owner="Bob")
ledger.add_utxo(tx_id="genesis", index=2, amount=20.0, owner="Charlie")
ledger.add_utxo(tx_id="genesis", index=3, amount=10.0, owner="David")
ledger.add_utxo(tx_id="genesis", index=4, amount=5.0, owner="Eve")