from django.contrib import admin
from ledger.models import Transaction
from django.utils.translation import ugettext_lazy as _


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['agent_from', 'agent_to', 'amount', 'batch_id', 'transaction_type', 'reason', 'from_deposit',
                    'date_created']

    def agent_from(self, instance):
        return instance.agent_from

    agent_from.short_description = _("Money from")

    def agent_to(self, instance):
        return instance.agent_to

    agent_to.short_description = _("Money to")

    def reason(self, instance):
        return instance.reason

    reason.short_description = _("Reason")

    class Meta:
        model = Transaction


admin.site.register(Transaction, TransactionAdmin)