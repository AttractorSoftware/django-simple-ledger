from django.test import TestCase
from ledger.tests.stub import LedgerClient, LedgerService
from ledger.transactions import DepositTransaction, CreditTransaction, DebitTransaction, TRANSACTION_DEPOSIT, TRANSACTION_CREDIT, TRANSACTION_DEBIT, WithdrawTransaction, TRANSACTION_WITHDRAW


class TestTransaction(TestCase):
    client = None
    service_provider = None

    def setUp(self):
        self.client = LedgerClient("Azamat")
        self.service_provider = LedgerService("Dentist")

    def test_credit_transaction(self):
        transaction = DepositTransaction()
        transaction.agent_from = self.client
        transaction.agent_to = self.service_provider
        transaction.amount = 200
        self.assertEqual(self.client, transaction.agent_from)
        self.assertEqual(self.service_provider, transaction.agent_to)
        self.assertEqual(200, transaction.amount)
        self.assertEqual(TRANSACTION_DEPOSIT, transaction.transaction_type)

    def test_dept_transaction(self):
        transaction = CreditTransaction()
        transaction.agent_from = self.client
        transaction.agent_to = self.service_provider
        transaction.amount = 200
        self.assertEqual(self.client, transaction.agent_from)
        self.assertEqual(self.service_provider, transaction.agent_to)
        self.assertEqual(200, transaction.amount)
        self.assertEqual(TRANSACTION_CREDIT, transaction.transaction_type)

    def test_payment_transaction(self):
        credit_transaction = CreditTransaction()
        credit_transaction.agent_from = self.client
        credit_transaction.agent_to = self.service_provider
        credit_transaction.amount = 200
        debit_transaction = DebitTransaction()
        debit_transaction.agent_from = self.client
        debit_transaction.agent_to = self.service_provider
        debit_transaction.transaction = credit_transaction
        debit_transaction.amount = 200
        self.assertEqual(credit_transaction.agent_from, debit_transaction.agent_from)
        self.assertEqual(credit_transaction.agent_to, debit_transaction.agent_to)
        self.assertEqual(200, debit_transaction.amount)
        self.assertEqual(TRANSACTION_DEBIT, debit_transaction.transaction_type)

    def test_withdrawal_trasaction(self):
        transaction = WithdrawTransaction()
        self.assertEqual(TRANSACTION_WITHDRAW, transaction.transaction_type)


