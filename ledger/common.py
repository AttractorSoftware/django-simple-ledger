from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Sum
from ledger.models import Transaction
from ledger.transactions import TRANSACTION_DEPOSIT, TRANSACTION_CREDIT, TRANSACTION_DEBIT, TRANSACTION_WITHDRAW
import time


class TransactionStorage(object):
    def save_transaction(self, transaction):
        raise NotImplementedError

    def get_transactions_from(self, agent):
        raise NotImplementedError

    def get_transactions_to(self, agent):
        raise NotImplementedError

    def get_deposit_transactions_from(self, agent):
        raise NotImplementedError

    def get_credit_transactions_from(self, agent):
        raise NotImplementedError

    def get_withdraw_transactions_from(self, agent):
        raise NotImplementedError

    def get_debit_transactions_from(self, agent):
        raise NotImplementedError


class SimpleTransactionStorage(TransactionStorage):
    transactions = list()

    def __init__(self):
        self.transactions = list()

    def save_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions_from(self, agent):
        result = list()
        for transaction in self.transactions:
            if transaction.agent_from == agent:
                result.append(transaction)
        return result

    def get_transactions_to(self, agent):
        result = list()
        for transaction in self.transactions:
            if transaction.agent_to == agent:
                result.append(transaction)
        return result

    def filter(self, transactions, transaction_type):
        result = list()
        for transaction in transactions:
            if transaction.transaction_type == transaction_type:
                result.append(transaction)
        return result

    def sum(self, transactions):
        result = 0
        for transaction in transactions:
            result += transaction.amount
        return result

    def get_transactions(self):
        return self.transactions


class DatabaseTransactionStorage(TransactionStorage):
    def save_transaction(self, transaction):
        db_transaction = Transaction()
        db_transaction.agent_from = transaction.agent_from
        db_transaction.agent_to = transaction.agent_to
        db_transaction.amount = transaction.amount
        db_transaction.batch_id = transaction.batch_id
        db_transaction.transaction_type = transaction.transaction_type
        db_transaction.reason = transaction.reason
        db_transaction.from_deposit = getattr(transaction, 'from_deposit', False)
        db_transaction.save()

    def get_transactions_from(self, agent):
        return Transaction.objects.filter(agent_from_id=agent.pk,
                                          agent_from_content_type=ContentType.objects.get_for_model(agent))

    def get_transactions_to(self, agent):
        return Transaction.objects.filter(agent_to_id=agent.pk,
                                          agent_to_content_type=ContentType.objects.get_for_model(agent))

    def filter(self, transactions, transaction_type, **kwargs):
        return transactions.filter(transaction_type=transaction_type, **kwargs)

    def sum(self, transactions):
        if not len(transactions):
            return 0
        return transactions.aggregate(Sum('amount'))['amount__sum']


class Ledger(object):
    storage = None

    def __init__(self):
        self.storage = None

    def add_batch(self, transaction_lists, custom_batch_id=None):
        batch_id = int(time.time())
        if custom_batch_id:
            batch_id = custom_batch_id
        for transaction in transaction_lists:
            self.add_transaction(transaction, batch_id)

    def add_transaction(self, transaction, custom_batch_id=None):
        batch_id = int(time.time())
        if not transaction:
            raise ValueError("Empty transaction is not allowed")
        if custom_batch_id:
            batch_id = custom_batch_id

        transaction.batch_id = batch_id
        self.storage.save_transaction(transaction)

    def get_transactions_from(self, agent):
        return self.storage.get_transactions_from(agent)

    def get_transactions_to(self, agent):
        return self.storage.get_transactions_to(agent)

    def get_sum_for(self, agent, transaction_type, **kwargs):
        return self.storage.sum(self.storage.filter(self.get_transactions_from(agent), transaction_type, **kwargs))

    @property
    def transactions(self):
        return self.storage.get_transactions()


class AccountManager(object):
    ledger = None

    def __init__(self, ledger_object=None):
        self.ledger = None
        if ledger_object:
            self.ledger = ledger_object

    def get_agent_from_balance(self, agent):
        transactions = self.ledger.get_transactions_from(agent)
        balance = 0
        for transaction in transactions:
            if transaction.transaction_type == TRANSACTION_DEPOSIT:
                balance += transaction.amount
            elif transaction.transaction_type == TRANSACTION_CREDIT:
                balance -= transaction.amount
            elif transaction.transaction_type == TRANSACTION_DEBIT:
                balance += transaction.amount
            elif transaction.transaction_type == TRANSACTION_WITHDRAW:
                balance -= transaction.amount
        return balance

    def get_receivable_balance(self, agent):
        transactions = self.ledger.get_transactions_to(agent)
        balance = 0
        for transaction in transactions:
            if transaction.transaction_type == TRANSACTION_CREDIT:
                balance += transaction.amount
            elif transaction.transaction_type == TRANSACTION_DEBIT:
                balance -= transaction.amount
        return balance

    def get_agent_to_balance(self, agent):
        balance = 0
        transactions = self.ledger.get_transactions_to(agent)
        for transaction in transactions:
            if transaction.transaction_type == TRANSACTION_DEBIT:
                balance += transaction.amount
            elif transaction.transaction_type == TRANSACTION_WITHDRAW:
                balance -= transaction.amount
            elif transaction.transaction_type == TRANSACTION_DEPOSIT:
                balance += transaction.amount
        return balance

    def get_balance(self, agent):
        to_balance = self.get_agent_to_balance(agent)
        from_balance = self.get_agent_from_balance(agent)
        return to_balance + from_balance

    def get_total_by(self, client, transaction_type, **kwargs):
        return self.ledger.get_sum_for(client, transaction_type, **kwargs)


ledger = Ledger()
ledger.storage = DatabaseTransactionStorage()
account_manager = AccountManager()
account_manager.ledger = ledger
import decimal

class ClientAccount(object):
    client = None

    def __init__(self):
        self.client = None

    @property
    def debit(self):
        return account_manager.get_total_by(self.client, TRANSACTION_DEBIT)

    @property
    def credit(self):
        return account_manager.get_total_by(self.client, TRANSACTION_CREDIT)

    @property
    def deposit(self):
        return account_manager.get_total_by(self.client, TRANSACTION_DEPOSIT) - account_manager.get_total_by(
            self.client, TRANSACTION_DEBIT, from_deposit=True)

    @property
    def total(self):
        return self.debit

    @property
    def debt(self):
        debt = self.debit - self.credit
        if debt < 0:
            return abs(debt)
        else:
            return debt
