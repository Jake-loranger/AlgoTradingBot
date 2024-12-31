from algosdk import transaction

def send_algo(algod_client, sender_address, private_key, receiver_address, amount, note):
    try:
        params = algod_client.suggested_params()
        txn = transaction.PaymentTxn(sender_address, params, receiver_address, amount, None, note)
        signed_txn = txn.sign(private_key)
        txid = algod_client.send_transaction(signed_txn)
        print(f"Transaction sent with ID: {txid}")
        return txid
    except Exception as e:
        print(f"Error sending transaction: {e}")


