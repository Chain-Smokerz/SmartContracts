from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient
import yaml
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.bcs import Serializer
from aptos_sdk.transactions import (
    EntryFunction,
    TransactionArgument,
    TransactionPayload,
)
from hashlib import sha256


secret_path = "../move/.aptos/config.yaml"
with open(secret_path, "r") as stream:
    pr_key = yaml.safe_load(stream)['profiles']['default']['private_key']

verifier = Account.load_key(pr_key)
public_key = verifier.address()

NODE_URL = "https://fullnode.devnet.aptoslabs.com/v1"
module_addr = "0x750e3394f4551dcf9d61b5152260ddf6c0cdf781064874bb27a66c330072d31d"
module_name = "DNuVModuleTest1"

class DNuVProtoClient(RestClient):
    async def push_otp(self, sender, user, otp_hash):
        user = AccountAddress.from_str(user)
        otp_hash = bytearray.fromhex(otp_hash)
        payload = EntryFunction.natural(
            f"{module_addr}::{module_name}",
            "push_otp",
            [],
            [
                TransactionArgument(user, Serializer.struct),
                TransactionArgument(otp_hash, Serializer.sequence_serializer(Serializer.u8))
            ],
        )
        
        signed_txn = await self.create_bcs_signed_transaction(
            sender, TransactionPayload(payload)
        )
        return await self.submit_bcs_transaction(signed_txn)


async def push_otp(user, otp):
    rest_client = DNuVProtoClient(NODE_URL)
    otp_hash = sha256(otp.encode('utf-8')).hexdigest()
    x = await rest_client.push_otp(verifier, user, otp_hash)
    return x
