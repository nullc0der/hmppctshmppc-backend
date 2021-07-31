import json

import requests
from typing import Dict, List, Union
from requests.auth import HTTPBasicAuth


class JSONRPCBase(object):
    def __init__(
            self, daemon_host_url: str, username: str,
            password: str, json_rpc_version: str = "1.0") -> None:
        self.daemon_host_url: str = daemon_host_url
        self.auth: HTTPBasicAuth = HTTPBasicAuth(username, password)
        self.json_rpc_version = json_rpc_version

    def call_rpc_api(
            self, method_name: str,
            params: Union[List, Dict]) -> Dict:
        data = json.dumps({
            "jsonrpc": self.json_rpc_version, "id": 1,
            "method": method_name, "params": params
        })
        res = requests.post(self.daemon_host_url, data, auth=self.auth)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        return {"success": False, "data": res.content}
