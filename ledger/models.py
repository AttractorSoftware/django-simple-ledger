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
    agent_from_content_type = models.ForeignKey(ContentType, related_name='agent_from_type', verbose_name=_('From object type'))
    agent_from_id = models.PositiveIntegerField(verbose_name=_('From object id'))
    agent_from = generic.GenericForeignKey('agent_from_content_type', 'agent_from_id')

    agent_to_content_type = models.ForeignKey(ContentType, related_name='agent_to_type', verbose_name=_("To object type"))
    agent_to_id = models.PositiveIntegerField(verbose_name=_("To object id"))
    agent_to = generic.GenericForeignKey('agent_to_content_type', 'agent_to_id')

    reason_content_type = models.ForeignKey(ContentType, related_name='payment_reason', null=True, verbose_name=_("Reason object type"))
    reason_id = models.PositiveIntegerField(null=True, verbose_name=_("Reason object id"))
    reason = generic.GenericForeignKey('reason_content_type', 'reason_id')

    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Amount of money"))
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=2, verbose_name=_("Transaction type"))
    batch_id = models.CharField(max_length=255, verbose_name=_("ID of batch transaction"))
    date_created = models.DateTimeField(auto_now=True, auto_now_add=True, blank=True, verbose_name=_("Date created"))

    transaction = models.ForeignKey('self', null=True, blank=True, related_name='reasoning_transaction',
                                    verbose_name=_("Related trasaction"))
    from_deposit = models.BooleanField(default=False, verbose_name=_("From deposit"), blank=True)

    class Meta:
        verbose_name = _("Ledger transaction")
        verbose_name_plural = _("Ledger transactions")