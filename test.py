from tally_integration import TallyClient, TallyConnectionError, TallyAPIError


client = TallyClient()

try:
    # Test 1: Connection test
    print("=== Testing Connection ===")
    connection_result = client.test_connection()
    print(f"Connection successful: {connection_result}")
    
    if not connection_result:
        print("Cannot proceed - Tally is not accessible")
        exit(1)
    
    # Test 2: Get current company
    print("\n=== Getting Current Company ===")
    company_response = client.get_current_company()
    print("Company Response:")
    print(company_response)
    
    # Test 3: Create a test ledger
    print("\n=== Creating Test Ledger ===")
    ledger_response = client.create_ledger(
        name="Simple Test Ledger",
        parent="Sundry Debtors",
        address="123 Test Address"
    )
    print("Ledger Creation Response:")
    print(ledger_response)
    
except TallyConnectionError as e:
    print(f"Connection Error: {e}")
except TallyAPIError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")