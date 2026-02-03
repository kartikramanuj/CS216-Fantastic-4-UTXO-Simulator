# Bitcoin UTXO & Transaction Simulator

**CS 216: Introduction to Blockchain - Assignment 1**
**Team: FANTASTIC-4**

**Team Members:**
- Ramanuj Kartik(240041030) - UTXO Manager , Test Scenarios & documentation
- Sana Tejasri(240041033)   - Mempool & CLI  
- Vaghasiya Parl(240041037) - Transaction & validator
- Sakshya Singh(240021015)  - Block Mining & documentation

A Python-based simulator demonstrating the core mechanics of Bitcoin's **UTXO (Unspent Transaction Output)** model, transaction validation, Mempool management, and mining logic.

This project is designed for the **CS 216: Introduction to Blockchain** assignment 1 to simulate real-world blockchain behaviors like **Double-Spending Prevention**, **Race Attacks**, and **Fork Resolution**.

---

## Project Structure

The project follows a modular architecture separating core logic from test scenarios.

```text
CS216-FANTASTIC-4UTXO-SIMULATOR/
│
├── src/  
│   ├── __init__.py           # to connect it with tests folder
│   ├── main.py               # CLI Entry Point
│   ├── utxo_manager.py       # Manages the Global Ledger (State)
│   ├── mempool.py            # Manages Pending Transactions (Gatekeeper)
│   ├── validator.py          # Validation Rules & Fee Calculation
│   ├── transaction.py        # Transaction Data Structure
│   └── Block.py              # Mining Logic
│
├── tests/                    # Simulation Scenarios
│   ├── __init__.py           # to connect it with src(specially for main.py)
│   └── test_scenarios.py     # Double-Spend, Race Attack, & Fork Tests
│
├── requirements.txt          # to mention all the dependencies
├── sample_output.txt         # To view the outputs(quickly)
└── README.md                 # Project Documentation
```

---

## Simulator Features

1. Interactive CLI :
 - The main menu allows you to manually control the blockchain:
 - Create Transaction: Send coins between users (Alice, Bob, etc.).
 - View UTXOs: See the current state of the ledger.
 - View Mempool: Check pending transactions waiting to be mined.
 - Mine Block: Confirm pending transactions and earn mining fees.

2. Automated Test Scenarios (Option 5 in the menue)
 *  The simulator includes pre-built scenarios to demonstrate blockchain security features:
   - Scenario 1: Double-Spending Prevention (Section 10.1)
   - Action: Alice tries to spend the exact same UTXO in two different transactions.
   - Result: The Mempool detects the UTXO is already "locked" by the first transaction and 
           rejects the second one immediately.

   - Scenario 2: Race Attack / First-Seen Rule (Section 10.2)
   - Action: A low-fee transaction is broadcast first. Immediately after, a high-fee 
             replacement is sent.
   - Result: The system enforces the First-Seen Rule. The high-fee transaction is rejected 
             because the input was already seen in the mempool.

   - Scenario 3: Fork Selection Rules (Section 10.4)
   - Action: Simulates two competing chains (Chain A vs. Chain B).
   - Logic: The simulator decides the winner based on the "Longest Chain" rule. If lengths
             are equal, it ties-breaks using Transaction Count, Fees, and Miner Name.

Interactive Mode: You can manually input chain lengths and fees to test edge cases.

3. Technical Implementation Details
 - Integrated Mempool Architecture
 - This simulator uses an Integrated Validation approach. The Mempool class acts as a strict
    gatekeeper.

 - Validation: When add_transaction() is called, the mempool internally calls validator.
   validate_transaction().

 - Security: This ensures it is impossible to add an invalid transaction to the mempool.

 - Fee Prioritization: If the mempool is full, it automatically evicts the transaction with
   the lowest fee.

4. Fee Calculation

Fees are implied, just like in Bitcoin:
Fee = Sum(Inputs) - Sum(Outputs)

The validator automatically calculates this fee and attaches it to the transaction metadata for miners to prioritize.

---

## How to Run Main.py

Steps:
1. write on terminal : cd CS216-FANTASTIC-4UTXO-SIMULATOR
2. write on terminal : python -m src.main
3. choose the feature and give inputs accordingly

---

# Modifications Made 
1. Mempool Prioritization: Changed from FIFO to fee-based sorting
2. Enhanced Security: Moved double-spend prevention to mempool (more realistic)
3. Simplified Validator: Reduced complexity, focused on core rules
4. Adapter Pattern: Updated main.py for new validate_transaction(tx, ledger, mempool)  
   signature
5. Module Connectivity: Added __init__.py files for proper imports

# Further improvements
1. Implement SHA-256 Hashing
2. Link Blocks with Hashes.
3. Handle Chain Reorganization: 
4. Implement Proof-of-Work

