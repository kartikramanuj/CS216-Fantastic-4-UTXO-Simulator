import hashlib
import json


class Transaction:

    def __init__(self, inputs, outputs):
       
        self.inputs = inputs
        self.outputs = outputs
        self.tx_id = self._generate_tx_id()

    def _generate_tx_id(self):
        
        tx_data = {
            "inputs": self.inputs,
            "outputs": self.outputs
        }

        tx_string = json.dumps(tx_data, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def __repr__(self):
        return f"Transaction(tx_id={self.tx_id})"