from typing import Dict, Optional, Any
from django.apps import AppConfig
from django.conf import settings

# from payment_processor.daemon_api_wrapper.bitcoin import BitcoinAPIWrapper
from payment_processor.daemon_api_wrapper.dogecoin import DogeCoinAPIWrapper
from payment_processor.daemon_api_wrapper.monero import MoneroAPIWrapper
# from payment_processor.daemon_api_wrapper.ethereum import EthereumAPIWrapper

# NOTE: In future we might modify the daemons to listen on zmq and process
# raw tx data from there, also look at txnotify feature at daemons, I think
# with this feature we can capture the hash, check the payment address, match
# to db and update the payment, then frontend can just poll the db and check
# its status 🎉


class PaymentProcessorConfig(AppConfig):
    name = 'payment_processor'

    def __init__(self, app_name: str, app_module: Optional[Any]) -> None:
        super().__init__(app_name, app_module)
        self.api_wrappers: Dict = {}

    def ready(self) -> None:
        # self.api_wrappers['bitcoin'] = BitcoinAPIWrapper(
        #     settings.BITCOIN_DAEMON_HOST,
        #     settings.BITCOIN_WALLET_RPC_USERNAME,
        #     settings.BITCOIN_WALLET_RPC_PASSWORD)
        # self.api_wrappers['bitcoin'].check_wallet_loaded()
        self.api_wrappers['dogecoin'] = DogeCoinAPIWrapper(
            settings.DOGECOIN_DAEMON_HOST,
            settings.DOGECOIN_WALLET_RPC_USERNAME,
            settings.DOGECOIN_WALLET_RPC_PASSWORD
        )
        self.api_wrappers['dogecoin'].check_wallet_loaded()
        self.api_wrappers['monero'] = MoneroAPIWrapper(
            settings.MONERO_DAEMON_HOST,
            settings.MONERO_WALLET_RPC_USERNAME,
            settings.MONERO_WALLET_RPC_PASSWORD
        )
        self.api_wrappers['monero'].check_wallet_loaded()
        # self.api_wrappers['ethereum'] = EthereumAPIWrapper(
        #     settings.ETHEREUM_DAEMON_HOST)
