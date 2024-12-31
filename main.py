from utils.check_new_assets import check_new_assets, print_block_info
from utils.connect_wallet import connect_wallet
from utils.tinyman_swap import get_swap_txs


def main():
    # Connect to wallet
    algod_client, address, private_key = connect_wallet()

    while True:
        # Check for new asset ID
        assetId = check_new_assets(algod_client)
        

        if assetId is None:
            print("No new asset found. Retrying...")
            continue  # Check again for a new asset

        # Perform the swap if a valid asset ID is found
        try:
            params = algod_client.suggested_params()
            tx_id = get_swap_txs(algod_client, private_key, address, 100000, assetId, 0, params)
            
            if tx_id == 'failed':
                print("Swap failed. Retrying...")
            else:
                print(f"Swap successful! Transaction ID: {tx_id}")
        
        except Exception as e:
            print(f"An error occurred: {e}")

        # Pause or exit logic can be added here if needed
        print("Checking for the next new asset...")


if __name__ == "__main__":
    main()
