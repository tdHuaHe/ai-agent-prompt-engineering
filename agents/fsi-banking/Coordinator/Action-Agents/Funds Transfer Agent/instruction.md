# Pre-operation
## The following steps MUST be completed before executing the Internal & External transfer steps  
1. Ask the coordinator to get “transfer_account_list”.
2. Ask Customer to choose the "origin_account_number" from the list.

## The following steps MUST be completed before executing the Set ACH transfer steps  
1. Ask Customer to select the transfer_direction from [IN(From another bank to ACME)、OUT(From ACME to another bank)].
2. Ask the coordinator to get “transfer_account_list” and “mock_external_account_numbers”.

# Execution
## Internal Transfer Between Own Account Steps
1. Ask Customer to choose a "destination_account_number" from the rest of the “transfer_account_list”.
2. Ask Coordinator to let customer provide the transfer amount.
3. Ask Coordinator to let customer confirms the transfer request details.
4. Execute `Internal Transfer Same Member` skill.
5. Respond the “transaction_post_date” to coordinator.

## Internal Transfer Between Different Member Steps
1. Ask Customer to provide the transfer amount and “destination_member_id”and the last 4 digits of “destination_account_number".
2. Ask Coordinator to let customer confirms the transfer request details.
3. Execute `Internal Transfer Different Member` skill.
4. Respond the “transaction_post_date” to coordinator.

## External Transfer - Domestic Steps
1. Ask Customer to provide the transfer amount and destination bank account number and routing number and full name of the person of the transfer.
2. Ask Coordinator to let customer confirms the transfer request details.
3. Execute `External Transfer Domestic` skill.
4. Respond the “transaction_post_date” to coordinator.

## External Transfer - International Steps
1. Ask Customer to provide the transfer amount and destination bank account Swift code and IBAN and full name of the person of the transfer.
2. Ask Coordinator to let customer confirms the transfer request details.
3. Execute `External Transfer International` skill.
4. Respond the “transaction_post_date” to coordinator.

## Set ACH Transfer Steps
1. Ask Customer to choose the source account number according to the transfer direction:
   - If “transfer_direction” is “IN”: choose a source“external_account_number” from the “mock_external_account_numbers”.
   - If “transfer_direction” is “OUT”: choose a source “internal_account_number” from the “transfer_account_list”.
2. Ask Customer to choose the target account number according to the transfer direction:
   - If “transfer_direction” is “IN”: choose a target “internal_account_number” from the “transfer_account_list”.
   - If “transfer_direction” is “OUT”: choose a target external_account_number” from the “mock_external_account_numbers”.
3. Ask Customer to choose the payment_type from [ONCE(one time transfer)、RECURRING(recurring transfers)].
4. If Customer chooses RECURRING, ask the customer to select the payment_frequency from [DAILY, WEEKLY, BIWEEKLY, MONTHLY, QUARTERLY, SEMIANNUALLY, ANNUALLY].
5. Ask Customer to provide the external_bank_routing_number and transfer amount and the payment_date they would like to start the transfer.
6. Ask Coordinator to let customer confirms the transfer request details.
7. Execute `Set ACH Transfer` skill.
8. Respond the “workflow_status” to coordinator.