from src.utxo_manager import UTXOManager
from src.transaction import Transaction
from src.validator import validate_transaction
from src.mempool import Mempool
from src.Block import mine_block
from tests.test_scenarios import run_tests

# Initialize Components
ledger = UTXOManager()
mempool = Mempool()
# Created a simple wrapper so test_scenarios.py can still call validator.validate_transaction() before tx
class ValidatorAdapter:
    def validate_transaction(self, tx):
        # Calls the standalone function using the global ledger and mempool
        return validate_transaction(tx, ledger, mempool)

validator = ValidatorAdapter()

def initialize_genesis():
    print("--- Initializing Genesis UTXOs ---")
    genesis_utxos = [
        ("Alice", 50.0),
        ("Bob", 30.0),
        ("Charlie", 20.0),
        ("David", 10.0),
        ("Eve", 5.0)
    ]
    for i, (owner, amount) in enumerate(genesis_utxos):
        ledger.add_utxo("genesis", i, amount, owner)
    print("\n--- Genesis UTXO Set ---")
    for i, (owner, amount) in enumerate(genesis_utxos):
        print(f"UTXO ('genesis', {i}) → Owner: {owner}, Amount: {amount}")

    print("Genesis block initialized.\n")

def create_transaction():
    print("\n--- Create New Transaction ---")
    sender = input("Enter sender: ")
    print(f"Available balance: {ledger.get_balance(sender)}")
    
    recipient = input("Enter recipient: ")
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.")
        return

    # 1. Gather Inputs (Simplistic "greedy" coin selection)
    sender_utxos = ledger.get_utxos_for_owner(sender)
    input_sum = 0.0
    selected_inputs = []
    
    for utxo in sender_utxos:
        if input_sum >= amount:
            break
        selected_inputs.append({
            "prev_tx": utxo["tx_id"],
            "index": utxo["output_index"],
            "owner": sender
        })
        input_sum += utxo["amount"]

    if input_sum < amount:
        print("Insufficient funds.")
        return

    # 2. Create Outputs
    outputs = [{"address": recipient, "amount": amount}]
    
    # Calculate Change (Simple fixed fee of 0.001 for demo)
    fee = 0.001
    change = input_sum - amount - fee
    if change > 0:
        outputs.append({"address": sender, "amount": change})

    # 3. Create & Validate
    tx = Transaction(selected_inputs, outputs)
    tx_dict = tx.to_dict()
    
    success, msg = mempool.add_transaction(tx_dict, ledger)
    
    if success:
        print(f"Transaction Valid & Added! Fee: {tx_dict['fee']:.5f}")
        print(f"Transaction ID: {tx_dict['tx_id']}")
    else:
        print(f"Transaction Rejected: {msg}")

def view_utxos():
    print("\n--- Current UTXO Set ---")
    for key, data in ledger.utxo_set.items():
        print(f"{key}: {data}")

def run_mining():
    miner = input("Enter miner name: ")
    result = mine_block(miner, mempool, ledger)
    print(result['message'])
    if result['success']:
        print(f"Miner {miner} earned {result['total_fees']} in fees.")

def main():
    initialize_genesis()
    
    while True:
        print("\n=== Bitcoin Transaction Simulator ===")
        print("1. Create new transaction")
        print("2. View UTXO set")
        print("3. View mempool")
        print("4. Mine block")
        print("5. Run test scenarios")
        print("6. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            create_transaction()
        elif choice == '2':
            view_utxos()
        elif choice == '3':
            print(f"Mempool contains {len(mempool.transactions)} transactions.")
        elif choice == '4':
            run_mining()
        elif choice == '5':
          run_tests(ledger, mempool, validator, "Miner1")
        elif choice == '6':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()