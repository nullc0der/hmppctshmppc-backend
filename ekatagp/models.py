import json

from django.db import models

# Create your models here.


class PaymentForm(models.Model):
    form_id = models.CharField(max_length=100, default='')
    created_on = models.DateTimeField()
    is_payment_success = models.BooleanField(default=False)
    payment_payload = models.TextField()

    def get_payment_payload_as_json(self):
        return json.loads(self.payment_payload)
