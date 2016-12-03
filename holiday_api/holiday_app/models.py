from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# /api/v1/recipient/{pk}/gift/{pk}


class HolidayUser(AbstractUser):
    """
    Our custom user.
    """

    added = models.DateTimeField(auto_now_add=True)
    # identical to date_joined field inherited.


class Recipient(models.Model):
    """
    An object representing the gift recipient.
    """

    TYPE = (
        ('friend', 'friend'),
        ('family', 'family')
    )

    # the name of the recipient.
    name = models.CharField(max_length=256)

    relation = models.CharField(max_length=16, choices=TYPE)

    # the person giving the gift (it's a many recipients to one user relationship)
    giver = models.ForeignKey('HolidayUser', related_name='recipients')

    class Meta:
        unique_together = ('name', 'relation', 'giver')


class Gift(models.Model):
    """
    The gift itself.
    """

    STATUS = (
        ('idea', 'idea'),
        ('bought', 'bought'),
        ('have', 'have'),
        ('shipped', 'shipped'),
        ('wrapped', 'wrapped')
    )

    status = models.CharField(max_length=16, choices=STATUS)

    item = models.CharField(max_length=256)
    notes = models.TextField(max_length=2048, default='')

    # https://github.com/django-money/django-money
    # it's broken in 1.10.1, I don't know if it's been updated.
    cost = models.DecimalField(max_digits=6, decimal_places=2)

    recipient = models.ForeignKey('Recipient', related_name='gifts')
