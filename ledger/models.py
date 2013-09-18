from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models


# Create your models here.
class Transaction(models.Model):
    agent_from_content_type = models.ForeignKey(ContentType, related_name='agent_from_type')
    agent_from_id = models.PositiveIntegerField()
    agent_from = generic.GenericForeignKey('agent_from_content_type', 'agent_from_id')

    agent_to_content_type = models.ForeignKey(ContentType, related_name='agent_to_type')
    agent_to_id = models.PositiveIntegerField()
    agent_to = generic.GenericForeignKey('agent_to_content_type', 'agent_to_id')

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=2)
    batch_id = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True, auto_now_add=True, blank=True)

    transaction = models.ForeignKey('self', null=True, blank=True, related_name='reasoning_transaction')

