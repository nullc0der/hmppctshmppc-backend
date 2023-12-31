import json

from django.utils.crypto import get_random_string
from django.utils.timezone import timedelta, now

from ekatagp.models import PaymentForm

from core_api.models import StatsSnapshot, AccessToken


def get_unique_access_token():
    access_token = get_random_string(length=32)
    if AccessToken.objects.filter(token=access_token):
        return get_unique_access_token()
    return access_token


def create_stats_snapshot(payment_form_id: str):
    payment_form = PaymentForm.objects.get(form_id=payment_form_id)
    stats = {
        'total_payment_count': 1,
        'bitcoin_payment_count': 0,
        'cardano_payment_count': 0,
        'dogecoin_payment_count': 0,
        'ethereum_payment_count': 0,
        'monero_payment_count': 0,
        'polkadot_payment_count': 0,
    }
    for p in PaymentForm.objects.filter(is_payment_success=True):
        payment_payload = p.get_payment_payload_as_json()
        currency_name = payment_payload['currency_name']
        stats['total_payment_count'] += 1
        stats[f'{currency_name}_payment_count'] += 1
    StatsSnapshot.objects.create(
        payment_form=payment_form, stats=json.dumps(stats))


def get_or_create_access_token(stats_snapshot: StatsSnapshot) -> str:
    access_token, created = AccessToken.objects.get_or_create(
        stats_snapshot=stats_snapshot)
    if created:
        access_token.token = get_unique_access_token()
        access_token.save()
    return access_token.token


def clean_access_token():
    for access_token in AccessToken.objects.all():
        if access_token.created_on + timedelta(days=3) < now():
            access_token.delete()
