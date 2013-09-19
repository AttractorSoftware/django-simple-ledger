django-simple-ledger
====================

Application that allow to keep track of financial transactions between different object of the system.
Basically if you have model class the instance of that model can pay money to the instance of the different model.

### Adding transaction

```python
import ledger.common as ledger
from ledger import trasaction
transaction = transaction.DepositTransaction()
trasaction.agent_from = client_object
trasaction.agent_to = service_provider_object # or merchant
transaction.amount = 1000
ledger.ledger.addTransaction(transaction, transaction_id="payment_type") # transaction_id is optional
```