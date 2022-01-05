import json

from django.db import models

from ekatagp.models import PaymentForm

# Create your models here.


class StatsSnapshot(models.Model):
    payment_form = models.OneToOneField(PaymentForm, on_delete=models.CASCADE)
    stats = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def get_stats_as_json(self):
        return json.loads(self.stats)


class AccessToken(models.Model):
    stats_snapshot = models.OneToOneField(
        StatsSnapshot, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)
    used_count = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
