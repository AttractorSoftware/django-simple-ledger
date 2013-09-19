from django.test import TestCase
from ledger.common import Ledger, AccountManager, SimpleTransactionStorage
from ledger.tests.stub import LedgerClient, LedgerService
from ledger.transactions import DepositTransaction, CreditTransaction, DebitTransaction


class TestLedger(TestCase):
    client = None
    service_provider = None
    ledger = None

    def setUp(self):
        self.client = LedgerClient("Azamat")
        self.service_provider = LedgerService("Dentist")
        self.ledger = Ledger()
        self.ledger.storage = SimpleTransactionStorage()

    def test_add_empty_transaction(self):

        self.assertRaises(ValueError, self.ledger.addTransaction, transaction=None)
        self.assertRaisesMessage(ValueError, "Empty transaction is not allowed", self.ledger.addTransaction, transaction=None)

    def test_client_pays_advance_payment_to_provider(self):
        transaction = DepositTransaction()
        transaction.amount = 200
        transaction.agent_from = self.client
        transaction.agent_to = self.service_provider

        self.ledger.addTransaction(transaction)
        self.assertEqual(1, len(self.ledger.getTransactionsFrom(self.client)))
        self.assertEqual(1, len(self.ledger.getTransactionsTo(self.service_provider)))

    def test_client_is_billed_and_pays_full(self):
        credit_transaction = CreditTransaction()
        credit_transaction.agent_from = self.client
        credit_transaction.agent_to = self.service_provider
        credit_transaction.amount = 1000

        self.ledger.addTransaction(credit_transaction)

        debit_transaction = DebitTransaction()
        debit_transaction.transaction = credit_transaction
        debit_transaction.amount = 1000
        debit_transaction.agent_from = self.client
        debit_transaction.agent_to = self.service_provider

        self.ledger.addTransaction(debit_transaction)
        self.assertEqual(2, len(self.ledger.getTransactionsFrom(self.client)))
        self.assertEqual(0, len(self.ledger.getTransactionsTo(self.client)))
        self.assertEqual(2, len(self.ledger.getTransactionsTo(self.service_provider)))

    def test_add_batch_transactions(self):
        transactions = list()
        credit_transaction = CreditTransaction()
        credit_transaction.agent_from = self.client
        credit_transaction.agent_to = self.service_provider
        credit_transaction.amount = 1000

        debit_transaction = DebitTransaction()
        debit_transaction.transaction = credit_transaction
        debit_transaction.amount = 1000
        debit_transaction.agent_from = self.client
        debit_transaction.agent_to = self.service_provider
        transactions.append(credit_transaction)
        transactions.append(debit_transaction)
        self.ledger.addBatch(transactions, 'helo')

        self.assertEqual(2, len(self.ledger.getTransactionsFrom(self.client)))
        self.assertEqual(0, len(self.ledger.getTransactionsTo(self.client)))
        self.assertEqual(2, len(self.ledger.getTransactionsTo(self.service_provider)))
        self.assertEqual('helo', self.ledger.getTransactionsTo(self.service_provider)[0].batch_id)










