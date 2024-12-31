from dotenv import load_dotenv
import os
from algosdk import mnemonic, account
from algosdk.v2client.algod import AlgodClient

load_dotenv()

def connect_wallet():
    mnemonic_phrase = os.getenv('MNEMONIC_PHRASE')
    if not mnemonic_phrase:
        raise ValueError("MNEMONIC_PHRASE not found in environment variables")
    
    private_key = mnemonic.to_private_key(mnemonic_phrase)
    address = account.address_from_private_key(private_key)
    
    algod_client = AlgodClient("", "https://mainnet-api.4160.nodely.dev")
    
    return algod_client, address, private_key
