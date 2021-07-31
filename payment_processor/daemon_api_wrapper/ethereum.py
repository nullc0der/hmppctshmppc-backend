import json
from decimal import Decimal
from typing import List, Dict, Optional, Tuple

import requests

from django.utils.crypto import get_random_string


def from_wei_to_eth(amount: int) -> Decimal:
    return Decimal(int(amount, 16)) / Decimal('1000000000000000000')


class EthereumAPIWrapper(object):
    def __init__(self, daemon_host_url: str) -> None:
        self.daemon_host_url: str = daemon_host_url

    def call_rpc_api(
            self, method_name: str, params: List = []) -> Dict:
        data = json.dumps({
            "jsonrpc": "2.0", "id": 1,
            "method": method_name, "params": params
        })
        res = requests.post(self.daemon_host_url, data)
        data = res.json()
        if data.get('result'):
            return {'success': True, 'data': data}
        return {'success': False, 'data': data}

    def get_new_address(self) -> Optional[Tuple[str, str]]:
        account_password = get_random_string(length=36)
        res = self.call_rpc_api('personal_newAccount', [account_password])
        if res['success']:
            return (res['data']['result'], account_password)

    def get_balance(self, address: str) -> Optional[Decimal]:
        res = self.call_rpc_api('eth_getBalance', [address, 'latest'])
        if res['success']:
            return from_wei_to_eth(res['data']['result'])

    # TODO: On moving to mainnet, get this data from ethscan or similar
    # block explorer and adjust other util functions accordingly
    def list_transactions(self, address: str) -> List:
        txs = []
        if self.get_balance(address):
            res = self.call_rpc_api('eth_getBlockByNumber', ['latest', True])
            if res['success']:
                for tx in res['data']['result']['transactions']:
                    if tx['to'] == address:
                        txs.append(tx)
        return txs
