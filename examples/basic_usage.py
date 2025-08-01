"""
Basic usage examples for Tally Integration Library

This script demonstrates basic operations like:
- Testing connection to Tally
- Getting company information
- Retrieving ledgers list
- Creating a new ledger
"""

from tally_integration import TallyClient, TallyConnectionError, TallyAPIError


def main():
    """Main example function."""
    
    # Initialize the Tally client
    # Default connection: http://localhost:9000
    client = TallyClient()
    
    # For custom Tally server, use:
    # client = TallyClient(tally_url="http://192.168.1.100", tally_port=9000)
    
    try:
        print("1. Testing connection to Tally...")
        if client.test_connection():
            print("✓ Successfully connected to Tally!")
        else:
            print("✗ Failed to connect to Tally. Please ensure Tally is running.")
            return
            
        print("\n2. Getting current company information...")
        company_info = client.get_current_company()
        print("Company info received:", len(company_info), "characters")
        
        print("\n3. Getting list of companies...")
        companies = client.get_companies_list()
        print("Companies list received:", len(companies), "characters")
        
        print("\n4. Getting list of ledgers...")
        ledgers = client.get_ledgers_list()
        print("Ledgers list received:", len(ledgers), "characters")
        
        print("\n5. Creating a new test ledger...")
        response = client.create_ledger(
            name="Test Customer API",
            parent="Sundry Debtors",
            address="123 Test Street, Test City",
            mobile="9999999999"
        )
        print("Ledger creation response:", len(response), "characters")
        
        print("\n6. Parsing XML response example...")
        parsed = client.parse_xml_response(company_info)
        print("Parsed response keys:", list(parsed.keys())[:5], "...")
        
        print("\n✓ All basic operations completed successfully!")
        
    except TallyConnectionError as e:
        print(f"✗ Connection Error: {e}")
        print("Make sure Tally is running and accessible.")
        
    except TallyAPIError as e:
        print(f"✗ API Error: {e}")
        print("Check the Tally server response for more details.")
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
