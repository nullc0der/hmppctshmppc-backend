import json
from typing import List, Optional, Dict

import requests
from requests.auth import HTTPBasicAuth

from django.conf import settings

# REGTEST PORT: 19001
# REGTEST PASSWORD: ZAxUSf9sTx51aet8Az2e5U3LiUX6dFXcWRu2WGn0VDw=


class BitcoinAPIWrapper(object):
    def __init__(
            self, daemon_host_url: str, username: str, password: str) -> None:
        self.daemon_host_url: str = daemon_host_url
        self.auth: HTTPBasicAuth = HTTPBasicAuth(username, password)
        self.wallet_is_loaded = False

    def call_rpc_api(
            self, method_name: str, params: List = []) -> Dict:
        data = json.dumps({
            "jsonrpc": "1.0", "id": 1,
            "method": method_name, "params": params
        })
        res = requests.post(self.daemon_host_url, data, auth=self.auth)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        return {"success": False, "data": res.content}

    def check_wallet_loaded(self):
        res = self.call_rpc_api('getbalance')
        if res['success']:
            self.wallet_is_loaded = True

    def load_wallet(self):
        res = self.call_rpc_api('loadwallet', [settings.BITCOIN_WALLET_NAME])
        if res['success']:
            self.wallet_is_loaded = True

    def unload_wallet(self):
        res = self.call_rpc_api('unloadwallet', [settings.BITCOIN_WALLET_NAME])
        if res['success']:
            self.wallet_is_loaded = False

    def get_balance(self) -> Optional[float]:
        if self.wallet_is_loaded:
            res = self.call_rpc_api('getbalance')
            if res['success']:
                return res['data']['result']

    def get_new_address(self) -> Optional[str]:
        if self.wallet_is_loaded:
            res = self.call_rpc_api('getnewaddress')
            if res['success']:
                return res['data']['result']

    def list_transactions(self, address: str) -> Optional[List]:
        if self.wallet_is_loaded:
            # TODO: Change confirmation to 6 once test done
            res = self.call_rpc_api(
                'listreceivedbyaddress',
                [
                    settings.BITCOIN_MIN_CONFIRMATION_NEEDED, False, False,
                    address
                ]
            )
            if res['success']:
                return res['data']['result']
