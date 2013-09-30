TRANSACTION_DEBIT = "D"
TRANSACTION_CREDIT = "C"
TRANSACTION_DEPOSIT = "A"
TRANSACTION_WITHDRAW = "W"

class SimpleTransaction(object):
    batch_id = None
    agent_from = None
    agent_to = None
    amount = 0
    reason = None

    def __init__(self):
        self.agent_from = None
        self.agent_to = None
        self.amount = 0
        self.batch_id = None
        self.reason = None

    @property
    def transaction_type(self):
        raise NotImplementedError


class DepositTransaction(SimpleTransaction):
    @property
    def transaction_type(self):
        return TRANSACTION_DEPOSIT


class CreditTransaction(SimpleTransaction):
    @property
    def transaction_type(self):
        return TRANSACTION_CREDIT


class DebitTransaction(SimpleTransaction):
    transaction = None
    from_deposit = False
    @property
    def transaction_type(self):
        return TRANSACTION_DEBIT


class WithdrawTransaction(SimpleTransaction):
    @property
    def transaction_type(self):
        return TRANSACTION_WITHDRAW