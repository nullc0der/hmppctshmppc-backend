import json
from decimal import Decimal
from typing import List, Optional, Dict

import requests
from requests.auth import HTTPDigestAuth

from django.conf import settings

PICONERO = Decimal('0.000000000001')


def from_atomic(amount: int) -> Decimal:
    return (Decimal(amount) * PICONERO).quantize(PICONERO)


class MoneroAPIWrapper(object):
    def __init__(
            self, daemon_host_url: str, username: str, password: str) -> None:
        self.daemon_host_url: str = daemon_host_url
        self.auth: HTTPDigestAuth = HTTPDigestAuth(username, password)
        self.wallet_is_loaded = False

    def call_rpc_api(
            self, method_name: str, params: Dict = {}) -> Dict:
        data = json.dumps({
            "jsonrpc": "2.0", "id": 1,
            "method": method_name, "params": params
        })
        res = requests.post(self.daemon_host_url, data, auth=self.auth)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        return {"success": False, "data": res.content}

    def check_wallet_loaded(self):
        res = self.call_rpc_api('get_balance', {'account_index': 0})
        if res['success']:
            self.wallet_is_loaded = True

    def load_wallet(self):
        res = self.call_rpc_api(
            'open_wallet',
            {
                "filename": settings.MONERO_WALLET_NAME,
                "password": settings.MONERO_WALLET_PASSWORD
            }
        )
        if res['success']:
            self.wallet_is_loaded = True

    def unload_wallet(self):
        res = self.call_rpc_api('close_wallet')
        if res['success']:
            self.wallet_is_loaded = False

    def get_balance(self, account_index: int = 0) -> Optional[Decimal]:
        if self.wallet_is_loaded:
            res = self.call_rpc_api(
                'get_balance', {'account_index': account_index})
            if res['success']:
                return from_atomic(res['data']['result']['balance'])

    def get_new_address(self) -> Optional[Dict]:
        if self.wallet_is_loaded:
            res = self.call_rpc_api('create_account')
            if res['success']:
                return res['data']['result']

    def list_transactions(
            self, account_index: int = 0) -> Optional[List]:
        if self.wallet_is_loaded:
            res = self.call_rpc_api(
                'get_transfers', {'in': True, 'account_index': account_index})
            if res['success'] and res['data']['result']:
                return res['data']['result']['in']
