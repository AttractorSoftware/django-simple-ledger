from django.test import TestCase
from ledger.common import Ledger, SimpleTransactionStorage, AccountManager
from ledger.tests.stub import LedgerService, LedgerClient
from ledger.transactions import CreditTransaction, DebitTransaction, DepositTransaction, WithdrawTransaction, TRANSACTION_DEPOSIT


class TestAccountManager(TestCase):
    client = None
    service_provider = None
    account_manager = None
    ledger = None

    def setUp(self):
        self.client = LedgerClient("Azamat")
        self.service_provider = LedgerService("Dentist")
        self.ledger = Ledger()
        self.ledger.storage = SimpleTransactionStorage()
        self.account_manager = AccountManager()
        self.account_manager.ledger = self.ledger

    def test_get_agent_from_balance(self):
        credit_transaction = CreditTransaction()
        credit_transaction.agent_from = self.client
        credit_transaction.agent_to = self.service_provider
        credit_transaction.amount = 1000

        self.ledger.add_transaction(credit_transaction)
        self.assertEqual(-1000, self.account_manager.get_agent_from_balance(self.client))

    def test_get_receivable_balance(self):
        credit_transaction = CreditTransaction()
        credit_transaction.agent_from = self.client
        credit_transaction.agent_to = self.service_provider
        credit_transaction.amount = 1000

        self.ledger.add_transaction(credit_transaction)

        self.assertEqual(1000, self.account_manager.get_receivable_balance(self.service_provider))

    def test_client_is_billed_and_pays_full(self):
        credit_transaction = CreditTransaction()
        credit_transaction.agent_from = self.client
        credit_transaction.agent_to = self.service_provider
        credit_transaction.amount = 1000

        self.ledger.add_transaction(credit_transaction)

        debit_transaction = DebitTransaction()
        debit_transaction.transaction = credit_transaction
        debit_transaction.amount = 1000
        debit_transaction.agent_from = self.client
        debit_transaction.agent_to = self.service_provider

        self.ledger.add_transaction(debit_transaction)

        self.assertEqual(1000, self.account_manager.get_agent_to_balance(self.service_provider))
        self.assertEqual(0, self.account_manager.get_agent_from_balance(self.client))

    def test_client_pays_by_parts(self):
        credit_transaction = CreditTransaction()
        credit_transaction.agent_from = self.client
        credit_transaction.agent_to = self.service_provider
        credit_transaction.amount = 1000

        self.ledger.add_transaction(credit_transaction)

        debit_transaction = DebitTransaction()
        debit_transaction.transaction = credit_transaction
        debit_transaction.amount = 200
        debit_transaction.agent_from = self.client
        debit_transaction.agent_to = self.service_provider

        self.ledger.add_transaction(debit_transaction)
        self.assertEqual(200, self.account_manager.get_agent_to_balance(self.service_provider))
        self.assertEqual(-800, self.account_manager.get_agent_from_balance(self.client))

        debit_transaction = DebitTransaction()
        debit_transaction.transaction = credit_transaction
        debit_transaction.amount = 800
        debit_transaction.agent_from = self.client
        debit_transaction.agent_to = self.service_provider

        self.ledger.add_transaction(debit_transaction)

        self.assertEqual(1000, self.account_manager.get_agent_to_balance(self.service_provider))
        self.assertEqual(0, self.account_manager.get_receivable_balance(self.service_provider))
        self.assertEqual(0, self.account_manager.get_agent_from_balance(self.client))

        self.assertEqual(0, self.account_manager.get_balance(self.client))
        self.assertEqual(1000, self.account_manager.get_balance(self.service_provider))

    def test_deposits_and_withdraw(self):
        deposit_transaction = DepositTransaction()
        deposit_transaction.amount = 200
        deposit_transaction.agent_from = self.client
        deposit_transaction.agent_to = self.service_provider
        self.ledger.add_transaction(deposit_transaction)
        withdraw_transaction = WithdrawTransaction()
        withdraw_transaction.agent_from = self.client
        withdraw_transaction.agent_to = self.service_provider
        withdraw_transaction.amount = 100
        self.ledger.add_transaction(withdraw_transaction)
        self.assertEqual(100, self.account_manager.get_agent_to_balance(self.service_provider))
        self.assertEqual(100, self.account_manager.get_agent_from_balance(self.client))

        self.assertEqual(100, self.account_manager.get_balance(self.client))
        self.assertEqual(100, self.account_manager.get_balance(self.service_provider))

    def test_get_total_deposit(self):
        deposit_transaction = DepositTransaction()
        deposit_transaction.amount = 200
        deposit_transaction.agent_from = self.client
        deposit_transaction.agent_to = self.service_provider
        self.ledger.add_transaction(deposit_transaction)
        self.assertEqual(200, self.account_manager.get_total_by(self.client, TRANSACTION_DEPOSIT))







