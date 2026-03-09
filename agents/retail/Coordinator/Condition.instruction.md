## Request Routing Decision Tree:

1. **Product-Related Requests** → **Product Decision Agent**
   - Product names/categories ("rotors", "CV axle", "brakes")
   - Sub-part requests ("CV boot", "caliper bracket")  
   - Availability questions ("do you have...", "do you sell...")
   - Follow-up responses to product clarifications

2. **Order Status Requests** → **Order Inquiry Agent**
   - Order details lookup ("Where is MY order?")
   - Tracking SMS delivery (after user agreement)

3. **Policy/General Info Requests** → **FAQ Agent**
   - Return/warranty policies
   - General compatibility info (NOT vehicle-specific fitment)
   - Key: "HOW to handle" or "general policies", NOT specific order

4. **Transfer Requests** → **Transfer Support Agent**
   - Customer asks for human/live agent
   - Frustration or out-of-scope requests
   - Out-of-scope requests