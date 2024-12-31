from utils.connect_wallet import connect_wallet
from utils.tinyman_swap import get_swap_txs



def main():
    algod_client, address, private_key = connect_wallet()

    input_amount = 1000000  # Amount of asset_in to swap (e.g., 1 ALGO)
    asset_in = 0  # Asset ID for ALGO (or any other asset you want to swap)
    asset_out = 2494786278  # Asset ID for the asset you want to receive in exchange for asset_in
    params = algod_client.suggested_params()
    
    # Perform the swap and print the result
    tx_id = get_swap_txs(algod_client, private_key, address, input_amount, asset_in, asset_out, params)
    print(f"Transaction ID: {tx_id}")
    
    if tx_id != 'failed':
        print(f"Transaction successful! Transaction ID: {tx_id}")
    else:
        print("Swap failed.")


if __name__ == "__main__":
    main()