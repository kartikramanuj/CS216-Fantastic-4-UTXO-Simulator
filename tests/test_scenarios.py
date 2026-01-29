import sys
import os

# Allow importing from src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from transaction import Transaction


def test_user_transaction():
   

    prev_tx = input("Enter previous transaction ID: ")
    index = int(input("Enter output index: "))
    owner = input("Enter owner name: ")

    amount = float(input("Enter amount to send: "))
    receiver = input("Enter receiver address: ")
    change = float(input("Enter change amount: "))

    inputs = [
        {"prev_tx": prev_tx, "index": index, "owner": owner}
    ]

    outputs = [
        {"amount": amount, "address": receiver},
        {"amount": change, "address": owner}
    ]

    tx = Transaction(inputs, outputs)

    print("\nTransaction created successfully!")
    print(tx)
    print("Transaction ID:", tx.tx_id)


if __name__ == "__main__":
    test_user_transaction()
