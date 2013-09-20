from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Sum
from ledger.models import Transaction
from ledger.transactions import TRANSACTION_DEPOSIT, TRANSACTION_CREDIT, TRANSACTION_DEBIT, TRANSACTION_WITHDRAW
import time


class TransactionStorage(object):
    def saveTransaction(self, transaction):
        raise NotImplementedError

    def getTransactionsFrom(self, agent):
        raise NotImplementedError

    def getTransactionsTo(self, agent):
        raise NotImplementedError

    def getDepositTransactionsFrom(self, agent):
        raise NotImplementedError

    def getCreditTransactionsFrom(self, agent):
        raise NotImplementedError

    def getWithdrawTransactionsFrom(self, agent):
        raise NotImplementedError

    def getDebitTransactionsFrom(self, agent):
        raise NotImplementedError


class SimpleTransactionStorage(TransactionStorage):
    transactions = list()

    def __init__(self):
        self.transactions = list()

    def saveTransaction(self, transaction):
        self.transactions.append(transaction)

    def getTransactionsFrom(self, agent):
        result = list()
        for transaction in self.transactions:
            if transaction.agent_from == agent:
                result.append(transaction)
        return result

    def getTransactionsTo(self, agent):
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
            result+=transaction.amount
        return result

    def get_transactions(self):
        return self.transactions


class DatabaseTransactionStorage(TransactionStorage):
    def saveTransaction(self, transaction):
        db_transaction = Transaction()
        db_transaction.agent_from = transaction.agent_from
        db_transaction.agent_to = transaction.agent_to
        db_transaction.amount = transaction.amount
        db_transaction.batch_id = transaction.batch_id
        db_transaction.transaction_type = transaction.transaction_type
        db_transaction.reason = transaction.reason
        db_transaction.save()

    def getTransactionsFrom(self, agent):
        return Transaction.objects.filter(agent_from_id=agent.pk, agent_from_content_type=ContentType.objects.get_for_model(agent))

    def getTransactionsTo(self, agent):
        return Transaction.objects.filter(agent_to_id=agent.pk, agent_to_content_type=ContentType.objects.get_for_model(agent))

    def filter(self, transactions, transaction_type):
        return transactions.filter(transaction_type=transaction_type)

    def sum(self, transactions):
        if not len(transactions):
            return 0
        return transactions.aggregate(Sum('amount'))['amount__sum']


class Ledger(object):
    storage = None

    def __init__(self):
        self.storage = None

    def addBatch(self, transaction_lists, custom_batch_id=None):
        batch_id = int(time.time())
        if custom_batch_id:
            batch_id = custom_batch_id
        for transaction in transaction_lists:
            self.addTransaction(transaction, batch_id)

    def addTransaction(self, transaction, custom_batch_id=None):
        batch_id = int(time.time())
        if not transaction:
            raise ValueError("Empty transaction is not allowed")
        if custom_batch_id:
            batch_id = custom_batch_id

        transaction.batch_id = batch_id
        self.storage.saveTransaction(transaction)

    def getTransactionsFrom(self, agent):
        return self.storage.getTransactionsFrom(agent)

    def getTransactionsTo(self, agent):
        return self.storage.getTransactionsTo(agent)

    def getSumFor(self, agent, transaction_type):
        return self.storage.sum(self.storage.filter(self.getTransactionsFrom(agent), transaction_type))

    @property
    def transactions(self):
        return self.storage.get_transactions()


class AccountManager(object):
    ledger = None

    def __init__(self, ledger=None):
        self.ledger = None
        if ledger:
            self.ledger = ledger

    def getAgentFromBalance(self, agent):
        transactions = self.ledger.getTransactionsFrom(agent)
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

    def getReceivableBalance(self, agent):
        transactions = self.ledger.getTransactionsTo(agent)
        balance = 0
        for transaction in transactions:
            if transaction.transaction_type == TRANSACTION_CREDIT:
                balance += transaction.amount
            elif transaction.transaction_type == TRANSACTION_DEBIT:
                balance -= transaction.amount
        return balance

    def getAgentToBalance(self, agent):
        balance = 0
        transactions = self.ledger.getTransactionsTo(agent)
        for transaction in transactions:
            if transaction.transaction_type == TRANSACTION_DEBIT:
                balance += transaction.amount
            elif transaction.transaction_type == TRANSACTION_WITHDRAW:
                balance -= transaction.amount
            elif transaction.transaction_type == TRANSACTION_DEPOSIT:
                balance += transaction.amount
        return balance

    def getBalance(self, agent):
        to_balance = self.getAgentToBalance(agent)
        from_balance = self.getAgentFromBalance(agent)
        return to_balance + from_balance

    def getTotalBy(self, client, transaction_type):
        return self.ledger.getSumFor(client, transaction_type)


ledger = Ledger()
ledger.storage = DatabaseTransactionStorage()
account_manager = AccountManager()
account_manager.ledger = ledger
