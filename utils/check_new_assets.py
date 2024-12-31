import json

MONITOR_ACCOUNT = "7TL5PKBGPH4W7LEZW5SW5BGC4TH32XVFV5NVTXE4HTTPVK2JUJODCVTHSU"
APPLICATION_ID = 2020762574

# Check new tokens on Rug Ninja 
def check_new_assets(algod_client):
    """
    Checks the latest block for a call to the specified application and returns the asset ID if found.
    """
    # Get the latest block
    try:
        # Get the status to fetch the latest round number
        status = algod_client.status()
        last_round = status['last-round']
        
        # Fetch block info for the latest round
        block = algod_client.block_info(last_round)
        
        if 'block' in block and 'txns' in block['block']:
            for txn in block['block']['txns']:

                # Check if the transaction type is 'acfg' (Asset Config)
                if txn['txn']['type'] == 'acfg':
                    if txn['txn']['snd'] == MONITOR_ACCOUNT:
                        print("txn:" + txn['txn'])
                    print(f"Asset Config transaction found.")
                    return txn['txn']['xaid']
        else:
            print("No transactions found in the block.")
        return None 
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return None


def print_block_info(algod_client):
    """
    Prints the latest block information.
    """
    status = algod_client.status()
    last_round = status['last-round']
    block_info = algod_client.block_info(last_round)
    print(json.dumps(block_info, indent=4))
    print(block_info)

