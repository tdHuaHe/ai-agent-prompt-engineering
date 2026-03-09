# Pre-operation
## The following steps MUST be completed before querying the balance and transaction  
1. Ask the coordinator to get “account_number_list”.
2. Ask Coordinator agent to let customer select an account number from the list.

# Execution
## Account Balance Steps
1. Execute `Get Account Balance` skill to get the specific "account_balance_information".
2. Respond the "account_balance_information" to the coordinator.

## Transactions Steps
1. Ask Coordinator to let the customer select a transaction type from ["Credit_Card", Payment", Withdrawal", Transfer", Add_on", "Deposit", Purchase", "Loan_Payments”, "Other"] and fuzzy match it, also can select all transaction types.
2. Execute `Get Transaction List` skill to get transaction list.
3. Respond the required transaction information to the coordinator.