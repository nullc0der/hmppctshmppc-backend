import json
from decimal import Decimal
from typing import Any, Dict, List, Tuple, Union, Optional

import requests

from django.conf import settings
from django.utils.timezone import now, timedelta
from django.utils.crypto import get_random_string
from django.apps import apps
from django.core.cache import cache

from payment_processor.models import Payment
from payment_processor.constants import TX_FIELDS_TO_CHECK, TX_FIELDS_TO_SAVE
from payment_processor.daemon_api_wrapper.monero import from_atomic
from payment_processor.daemon_api_wrapper.ethereum import from_wei_to_eth

payment_processor_configs = apps.get_app_config('payment_processor')


def get_unique_payment_id() -> str:
    payment_id = get_random_string(length=6)
    if Payment.objects.filter(payment_id=payment_id):
        return get_unique_payment_id()
    return payment_id


def get_wallet_address(address_data: Any, currency: str) -> str:
    if currency == 'monero':
        return address_data['address']
    if currency == 'ethereum':
        return address_data[0]
    return address_data


def create_payment(currency: str) -> Dict[str, str]:
    api_wrapper = payment_processor_configs.api_wrappers[currency]
    wallet_address = api_wrapper.get_new_address()
    if wallet_address:
        payment = Payment(
            currency=currency,
            payment_id=get_unique_payment_id(),
            wallet_address=get_wallet_address(wallet_address, currency),
            monero_account_index=None
            if currency != 'monero' else wallet_address['account_index'],
            ethereum_account_password=''
            if currency != 'ethereum' else wallet_address[1]
        )
        payment.save()
        return {
            'payment_id': payment.payment_id,
            'wallet_address': payment.wallet_address,
            'per_usd_amount': get_per_usd_currency_amount(currency)
        }
    return {
        'payment_id': '',
        'wallet_address': '',
        'per_usd_amount': 0
    }


def check_payment_valid(payment_results: List, currency: str) -> bool:
    fields = TX_FIELDS_TO_CHECK[currency]
    for payment_result in payment_results:
        for field in fields:
            if not payment_result.get(field):
                return False
        if currency != 'ethereum':
            if not payment_result['confirmations'] >= \
                    settings.__dict__['_wrapped'].__dict__[
                        f'{currency.upper()}_MIN_CONFIRMATION_NEEDED']:
                return False
    # if payment_result[0].get(fields[0]) and payment_result[0].get(fields[1])\
    #         and payment_result[0].get(fields[2]):
    #     if payment_result[0]['confirmations'] >=\
    #             settings.__dict__['_wrapped'].__dict__[
    #                 f'{currency.upper()}_MIN_CONFIRMATION_NEEDED']:
    #         return True
    return True


def convert_payment_amount(
        amount: Union[float, int], currency: str) -> Union[float, Decimal]:
    if currency == 'monero':
        return from_atomic(amount)
    if currency == 'ethereum':
        return from_wei_to_eth(amount)
    return amount


def compare_payment_address(
        payment_result: Dict, payment_address: str, currency: str) -> bool:
    if currency == 'ethereum':
        return payment_result['to'] == payment_address
    return payment_result['address'] == payment_address


def get_payment_amount_and_txid(
        payment_results: List,
        currency: str, payment_address: str) -> Tuple[float, List]:
    fields = TX_FIELDS_TO_SAVE[currency]
    amount = 0
    txids_list = []
    for payment_result in payment_results:
        if compare_payment_address(payment_result, payment_address, currency):
            amount += convert_payment_amount(
                payment_result.get(fields[0]), currency)
            txids = payment_result.get(fields[1])
            if isinstance(txids, list):
                txids_list += txids
            else:
                txids_list.append(txids)
    return (amount, txids_list)


def check_payment(payment: Payment) -> bool:
    if not payment.tx_ids:
        api_wrapper = \
            payment_processor_configs.api_wrappers[payment.currency]
        result = api_wrapper.list_transactions(
            payment.wallet_address
            if payment.currency != 'monero' else payment.monero_account_index)
        if result and check_payment_valid(result, payment.currency):
            amount, txids = get_payment_amount_and_txid(
                result, payment.currency, payment.wallet_address)
            payment.amount_received = amount
            payment.tx_ids = json.dumps(txids)
            payment.raw_tx_data = json.dumps(result)
            payment.save()
            return True
        return False
    return True


def clean_unused_payments():
    for payment in Payment.objects.filter(tx_ids__isnull=True):
        if payment.created_on + timedelta(days=3) < now():
            payment.delete()


def sync_currency_price():
    """
    This function will sync and cache the coin prices from coingecko api
    """
    data = {}
    for currency in ['bitcoin', 'dogecoin', 'monero']:
        res = requests.get(
            'https://api.coingecko.com/api/v3/simple/'
            f'price?ids={currency}&vs_currencies=usd')
        if res.status_code == 200:
            data[currency] = res.json().get(currency, {})
    cache.set('currency_price', data, None)


def get_per_usd_currency_amount(currency_name: str) -> Optional[float]:
    currency_prices = cache.get('currency_price')
    if currency_prices:
        currency_price = currency_prices[currency_name].get('usd')
        if currency_price:
            return "%.6f" % (1 / currency_price)
