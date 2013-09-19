from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from ledger.transactions import TRANSACTION_DEBIT, TRANSACTION_DEPOSIT, TRANSACTION_CREDIT, TRANSACTION_WITHDRAW

TRANSACTION_TYPES = ((TRANSACTION_DEBIT, _("Debit")),
                     (TRANSACTION_DEPOSIT, _("Deposit")),
                     (TRANSACTION_CREDIT, _("Credit")),
                     (TRANSACTION_WITHDRAW, _("Withdraw")))


class Transaction(models.Model):
    agent_from_content_type = models.ForeignKey(ContentType, related_name='agent_from_type')
    agent_from_id = models.PositiveIntegerField()
    agent_from = generic.GenericForeignKey('agent_from_content_type', 'agent_from_id')

    agent_to_content_type = models.ForeignKey(ContentType, related_name='agent_to_type')
    agent_to_id = models.PositiveIntegerField()
    agent_to = generic.GenericForeignKey('agent_to_content_type', 'agent_to_id')

    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Amount of money"))
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=2, verbose_name=_("Transaction type"))
    batch_id = models.CharField(max_length=255, verbose_name=_("ID of batch transaction"))
    date_created = models.DateTimeField(auto_now=True, auto_now_add=True, blank=True, verbose_name=_("Date created"))

    transaction = models.ForeignKey('self', null=True, blank=True, related_name='reasoning_transaction',
                                    verbose_name=_("Related trasaction"))

