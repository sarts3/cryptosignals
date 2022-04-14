from django.db import models
from django.utils import timezone

from datetime import datetime, timedelta


class Price(models.Model):
    coin = models.CharField(max_length=8, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )

    @classmethod
    def create_new(cls, coin, price):
        return cls(coin=coin, price=price).save()


class Job(models.Model):
    coin = models.CharField(max_length=8, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    @property
    def is_active(self):
        return True if (not self.expired_at or self.expired_at < timezone.now()) else False

    @classmethod
    def create_new(cls, coin, expired_at=None):
        return cls(coin=coin, expired_at=expired_at).save()

class Alarm(models.Model):
    coin = models.CharField(max_length=8, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()


    @classmethod
    def create_new(cls, coin, duration_in_minutes=60):
        return cls(coin=coin, expired_at=(timezone.now()+timedelta(minutes=duration_in_minutes))).save()

    @classmethod
    def is_active(cls, coin):
        return Alarm.objects.filter(coin=coin, expired_at__gt=timezone.now())
