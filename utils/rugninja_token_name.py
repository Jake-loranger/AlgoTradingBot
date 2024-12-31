from algosdk.v2client.algod import AlgodClient
from algosdk.abi import ABIType
import base64

node_token = ''
node_server = 'https://mainnet-api.4160.nodely.dev'

algod_client = AlgodClient(node_token, node_server)

rug_ninja_app_id = 2020762574

token_holding_box_schema = ABIType.from_string('(address,uint64)')

# Token to check holdings for
target_token_id = 2639168320

application_boxes = algod_client.application_boxes(rug_ninja_app_id)['boxes']

for box in application_boxes:
    try:
        decoded_bytes = base64.b64decode(box['name'])
        decoded_string = decoded_bytes.decode("utf-8")
        print(f"{decoded_string}")
    except UnicodeDecodeError:
        continue  