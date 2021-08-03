import json

from django.db import models

from payment_processor import constants

# Create your models here.


class Payment(models.Model):
    currency = models.CharField(
        max_length=12, choices=constants.SUPPORTED_CURRENCY, default='bitcoin')
    payment_id = models.CharField(max_length=6)
    wallet_address = models.TextField(null=True)
    # TODO: need to check BTC and DOGE tx whether they return in atomic, if yes
    # we should convert and if no we should preserve precision
    amount_received = models.FloatField(null=True)
    tx_ids = models.TextField(null=True)
    raw_tx_data = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    monero_account_index = models.IntegerField(null=True)
    # TODO: Maybe it should not saved in plaintext
    ethereum_account_password = models.CharField(default='', max_length=36)

    def get_tx_ids_as_json(self):
        return json.loads(self.tx_ids)

    def __str__(self) -> str:
        return f'{self.currency} - {self.payment_id}'
