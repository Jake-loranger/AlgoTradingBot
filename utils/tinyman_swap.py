from algosdk.v2client.algod import AlgodClient
from algosdk.transaction import (
    OnComplete, ApplicationCallTxn, assign_group_id,
    wait_for_confirmation, AssetTransferTxn, PaymentTxn
)
from algosdk import mnemonic
from algosdk.account import address_from_private_key
from tinyman.v2.pools import Pool as TinymanV2Pool
from tinyman.v2.client import TinymanV2MainnetClient

TINYMAN_ROUTER = 1002541853

# algod_client = AlgodClient("", 'https://mainnet-api.4160.nodely.dev')
# MNEMONIC_PHRASE = "carpet youth lend gadget pink absorb daring salad small web velvet skin cake camp bring kite patrol rice circle fitness accuse census mesh above title"

# pk = mnemonic.to_private_key(MNEMONIC_PHRASE) 
# address = address_from_private_key(pk)

def get_pool_address(algod_client, user_address, asset_1, asset_2):
    """Retrieve the pool address and pool token asset for the given assets."""
    client = TinymanV2MainnetClient(algod_client=algod_client, user_address=user_address)
    v2_pool = TinymanV2Pool(client=client, asset_a=asset_1, asset_b=asset_2, fetch=True)
    return v2_pool.address, v2_pool.pool_token_asset

def get_swap_txs(algod_client, private_key, user_address, input_amount, asset_in, asset_out, params):
    """Prepare the transactions for selling via Tinyman."""
    pool_address, lp_asset = get_pool_address(algod_client, user_address, asset_in, asset_out)
    lp_asset_id = lp_asset.id

   

    if asset_in == 0:
        asset_in_txn = PaymentTxn(
            sender=user_address,
            sp=params,
            receiver=pool_address,
            amt=input_amount
        )
    
    else:
         asset_in_txn = AssetTransferTxn(
            sender=user_address,
            sp=params,
            receiver=pool_address,
            amt=input_amount,
            index=asset_in
        )
    
    params.flat_fee = True
    params.fee = 10_000
    minimum_buy_or_sell = (1).to_bytes(4, 'big')

    application_call = ApplicationCallTxn(
        sender=user_address,
        index=TINYMAN_ROUTER,
        app_args=[b'swap', b'fixed-input', minimum_buy_or_sell],
        sp=params,
        on_complete=OnComplete.NoOpOC,
        foreign_assets=[asset_in, asset_out, lp_asset_id],
        accounts=[pool_address],
    )
    
    txs = [asset_in_txn, application_call]
    assign_group_id(txs)
    signed_txs = [tx.sign(private_key) for tx in txs]

    try:
        tx_id = algod_client.send_transactions(signed_txs)
        print(tx_id)
        wait_for_confirmation(algod_client, tx_id)
        return tx_id
    
    except Exception as e:
        return 'failed'
    


# def main():
#     input_amount = 1000000  # Amount of asset_in to swap (e.g., 1 ALGO)
#     asset_in = 0  # Asset ID for ALGO (or any other asset you want to swap)
#     asset_out = 2494786278  # Asset ID for the asset you want to receive in exchange for asset_in
#     params = algod_client.suggested_params()  # Get the current suggested transaction parameters
    
#     # Perform the swap and print the result
#     tx_id = get_swap_txs(address, input_amount, asset_in, asset_out, params)
#     print(f"Transaction ID: {tx_id}")
    
#     if tx_id != 'failed':
#         print(f"Transaction successful! Transaction ID: {tx_id}")
#     else:
#         print("Swap failed.")

# if __name__ == "__main__":
#     main()