from src.transaction import Transaction

def build_simulated_chain(chain_label):
    """
    It can help the user build a chain list interactively.
    To  simulate 'previous' blocks as dummies, and define the 'tip' (latest block) fully.
    """
    print(f"\n Building {chain_label}")
    
    # 1. Determine Chain Length (The Calculation Source)
    while True:
        try:
            total_blocks = int(input(f"No. of blocks total in {chain_label}: "))
            if total_blocks < 1:
                print("Chain must have at least 1 block.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    # 2. Define the 'Tip' (The latest block used for tie-breakers)
    print(f"Enter details for the LATEST block (Block #{total_blocks}):")
    miner = input(f"  -Miner Name: ")
    while True:
        try:
            tx_count = int(input(f"  - Transaction Count: "))
            fees = float(input(f"  - Total Fees: "))
            break
        except ValueError:
            print("  - Error: Please enter numbers for count and fees.")

    # 3. Construct the Chain List
    # We fill the previous blocks with dummy data since they don't affect the tip comparison
    chain = []
    for i in range(total_blocks - 1):
        chain.append({'miner': 'old_miner', 'tx_count': 0, 'fees': 0})
    
    # Append the tip (the one we care about)
    chain.append({'miner': miner, 'tx_count': tx_count, 'fees': fees})
    
    return chain

def resolve_fork(chain_a, chain_b):
    len_a, len_b = len(chain_a), len(chain_b)
    tip_a, tip_b = chain_a[-1], chain_b[-1]
    
    print(f"Comparing: Chain A ({len_a} blocks) vs Chain B ({len_b} blocks)")

    # Rule 0: Longest Chain
    if len_a > len_b: return "Winner: Chain A (Longest Chain)"
    if len_b > len_a: return "Winner: Chain B (Longest Chain)"

    # Tie-Breakers
    if tip_a['tx_count'] > tip_b['tx_count']: return "Winner: Chain A (More Txs)"
    if tip_b['tx_count'] > tip_a['tx_count']: return "Winner: Chain B (More Txs)"
    if tip_a['fees'] > tip_b['fees']: return "Winner: Chain A (Higher Fee)"
    if tip_b['fees'] > tip_a['fees']: return "Winner: Chain B (Higher Fee)"
    
    return "Winner: Chain A (Miner Name)" if tip_a['miner'] < tip_b['miner'] else "Winner: Chain B (Miner Name)"

def run_tests(ledger, mempool, validator, miner_address):

   while True:
    print("   SELECT TEST SCENARIO")
    print("1. Double-Spend Attack (Section 10.1)")
    print("2. Race Attack / First-Seen (Section 10.2)")
    print("3. Fork Selection Rules (Section 10.4)")
    print("4. Return to Main Menu")
        
    choice = input("\nEnter choice: ")
    #  Double-Spending Prevention
    if choice == '1':
            print("\nRunning Test 1: Double-Spending Prevention...")
            # Setup
            mempool.transactions.clear(); mempool.spent_utxos.clear()
            alice_utxos = ledger.get_utxos_for_owner("Alice")
            if not alice_utxos: print("Alice has no funds!"); continue
            
            utxo = alice_utxos[0]
            inp = [{"prev_tx": utxo['tx_id'], "index": utxo['output_index'], "owner": "Alice"}]
            
            # Step 1: Valid Tx (Alice -> Bob)
            
            tx1 = Transaction(inp, [{"address": "Bob", "amount": 10.0}])
            success, msg = mempool.add_transaction(tx1.to_dict(), ledger)
            
            if success:
                print(f"TX1 : Alice -> Bob (10 BTC)    - VALID ({msg})")
            else:
                print(f"TX1 Failed: {msg}")
            
            # Step 2: Invalid Tx (Double Spend: Alice -> Charlie)
            tx2 = Transaction(inp, [{"address": "Charlie", "amount": 10.0}])
            success2, msg2 = mempool.add_transaction(tx2.to_dict(), ledger)
            
            if not success2:
                print(f"TX2 : Alice -> Charlie (10 BTC) - REJECTED")
                print(f"Error : {msg2}")
            else:
                print("FAIL: TX2 was accepted!")

        #  SCENARIO 2: RACE ATTACK 
    elif choice == '2':
            print("\nRunning Test 2: Race Attack (First-Seen Rule)...")
            # Setup
            mempool.transactions.clear(); mempool.spent_utxos.clear()
            alice_utxos = ledger.get_utxos_for_owner("Alice")
            utxo = alice_utxos[0]
            inp = [{"prev_tx": utxo['tx_id'], "index": utxo['output_index'], "owner": "Alice"}]
            
            # Step 1: Low Fee Tx (First seen)
            tx_low = Transaction(inp, [{"address": "Bob", "amount": 10.0}])
            
        
            success, msg = mempool.add_transaction(tx_low.to_dict(), ledger)
            if success:
                print("TX1 (Low Fee)  : Broadcast 1st - ENTERED MEMPOOL")

            # Step 2: High Fee Tx (Attempt to replace)
            tx_high = Transaction(inp, [{"address": "Charlie", "amount": 5.0}]) # Less amount = Higher Fee
            
           
            success2, msg2 = mempool.add_transaction(tx_high.to_dict(), ledger)
            
            if not success2:
                print("TX2 (High Fee) : Broadcast 2nd - REJECTED (Rule: First-Seen)")
                print(f"Error : {msg2}")
            else:
                print("FAIL: TX2 replaced TX1!")

        #  SCENARIO 3: FORK SELECTION 
    elif choice == '3':
            print("\nRunning Test 3: Fork Selection...")
            sub_choice = input("Use custom chains? (yes/no): ")
            if sub_choice.lower() == 'yes':
                c1 = build_simulated_chain("Chain A")
                c2 = build_simulated_chain("Chain B")
                print(f"Result: {resolve_fork(c1, c2)}")
            else:
                # Default Demo
                c_long = [{}, {}, {}] # Length 3
                c_short = [{}, {'miner': 'Rich', 'tx_count': 100, 'fees': 100}] # Length 2
                print("\nScenario: Chain A (Len 3) vs Chain B (Len 2, High Fees)")
                print(f"Result: {resolve_fork(c_long, c_short)}")

    elif choice == '4':
            mempool.transactions.clear(); mempool.spent_utxos.clear()
            break