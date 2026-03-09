# Execution
## Get Contact Information Steps
1. Use the provided member ID to execute `Get Contact Info` skill to get "contact_name" and "contact_id". 
2. Respond the "contact_name" and "contact_id" to the Coordinator.

## Get Accounts List Steps
1. Use "contact_id" to execute `Get Required Account List` skill to obtain:
  - `account_number_list`
  - `active_loan_accounts`
  - `active_credit_accounts`
  - `available_balance_accounts`
2. Respond the required account number list to the Coordinator.