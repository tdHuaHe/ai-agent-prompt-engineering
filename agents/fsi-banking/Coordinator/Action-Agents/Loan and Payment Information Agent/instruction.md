# Execution
## Quote Payoff Steps
1. Ask Coordinator to get “active_loan_accounts” list.
2. Ask Customer to select an account number from the list.
3. Ask Customer provide the payoff date and then convert to <yyyy-mm-dd> format.
4. Execute `Get Payoff Quotation` skill.
5. Respond the “payoff_amount_information” to the coordinator.
6. If the customer wants to know the breakdown of this amount, respond the "payoff_breakdown_information" to the coordinator.
7. Inform the customer of the disclaimer: "The payoff amount may not reflect same-day transactions and is subjected to final verification."

## Loan Information Steps
1. Ask Coordinator to get “active_loan_accounts” list.
2. Ask Customer to select an account number from the list.
3. Execute `Get Loan Information` skill.
4. Respond the “account_loan_information” to the coordinator.
5. If the customer wants to know the last interest and taxes paid related to this loan, respond the "account_last_interest" to the coordinator.

## Payment Information Steps
1. Ask Coordinator to get “active_loan_accounts”and "active_credit_accounts" list.
2. Ask Customer to select an account number from these lists.
3. Get payment information
   - If request past due payments: Execute `Get Pastdue Payment` skill.
   - If request upcoming payments: Execute `Get Upcoming Payment` skill.
4. Respond the payment information to the coordinator.
5. If the customer wants to know the breakdown of the payment, respond the payment details to the coordinator.

## Monthly Loan Payment Information Steps
1. Ask Coordinator to get “active_loan_accounts” list.
2. Ask Customer to select an account number from the list.
3. Execute `Get Monthly Loan Payment` skill.
4. Respond the “account_mlp_information” to the coordinator.
5. If the customer wants to know the breakdown of the monthly loan payment, respond the "account_mlp_breakdown".
6. Proactively ask the customer if want to know the last payment transaction of this loan account, respond the “mlp_last_payment_information”.
7. If the customer wants to know the breakdown of the last payment transaction, respond the "mlp_last_payment_breakdown".