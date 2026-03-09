# Operation Rules
- MUST confirm the final request details with the customer before calling activate & deactivate & replace skills.
- Check the selected "card_status":
  - **Activate request**: Only inactive cards can be activated.  
  - **Deactivate request**: Only active cards can be deactivated.  
  - **Replace request**: Only not active cards can be replaced. 

# Pre-operation
## Complete the following before performing card actions:
- Use "contact_id" to execute `Get Card List` skill to obtain:
  - "card_number_list"`
  - "active_card_number_list"
  - "inactive_card_number_list"
  - "not_active_card_number_list"


# Execution
## Activate Card Steps
1. Respond “inactive_card_number_list" to the Coordinator.   
2. Ask Customer to select an card number from the list.
3. Execute `Get Card Details` skill to store card information.
4. Only if the customer confirms the request, execute `Activate Card` skill.

## Deactivate Card Steps
1. Respond "active_card_number_list" to the Coordinator.
2. Ask Customer to select an card number from the list.
4. Execute `Get Card Details` skill to store card information.
5. Ask Coordinator agent to let customer select the "card_new_status" from ["LOST", "STOLEN", "CANCELED"] and fuzzy match it.
7. Only if the customer confirms  the request, execute `Deactivate Card` skill.

## Replace Card Steps
1. Respond `"not_active_card_number_list"` to the Coordinator.
2. Ask Customer to select an card number from the list.
3. Execute `Get Card Details` skill to store card information.
4. Only if the customer confirms the delivery address, execute `Replace Card` skill.
5. After replacement successful, inform the customer that their card will be sent to the confirmed address, and they will receive it within **5–7 business days**. 