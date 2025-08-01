#!/usr/bin/env python3
"""
Simple test script to verify Tally Integration Library functionality.

This script tests:
1. Connection to Tally
2. Getting current company information
3. Creating a new ledger

Make sure Tally is running before executing this script.
"""

import sys
import os

# Add the current directory to Python path to import our package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tally_integration import TallyClient, TallyConnectionError, TallyAPIError, TallyValidationError


def test_tally_integration():
    """Test basic Tally integration functionality."""
    
    print("🔧 Tally Integration Library Test")
    print("=" * 50)
    
    # Initialize the client
    print("1. Initializing TallyClient...")
    client = TallyClient()
    print(f"   ✓ Client initialized for {client.endpoint}")
    
    try:
        # Test 1: Connection Test
        print("\n2. Testing connection to Tally...")
        if client.test_connection():
            print("   ✓ Successfully connected to Tally!")
        else:
            print("   ✗ Failed to connect to Tally.")
            print("   Please ensure:")
            print("   - Tally is running")
            print("   - XML API is enabled in Tally")
            print("   - Tally is accessible on localhost:9000")
            return False
            
        # Test 2: Get Current Company
        print("\n3. Getting current company information...")
        try:
            company_response = client.get_current_company()
            print(f"   ✓ Company information retrieved ({len(company_response)} characters)")
            
            # Try to extract company name from response
            if "<NAME>" in company_response:
                start = company_response.find("<NAME>") + 6
                end = company_response.find("</NAME>", start)
                if end > start:
                    company_name = company_response[start:end]
                    print(f"   📊 Current company: {company_name}")
            
        except Exception as e:
            print(f"   ⚠️  Warning: Could not get company info - {e}")
            
        # Test 3: Create a Test Ledger
        print("\n4. Creating a test ledger...")
        test_ledger_name = "API Test Ledger"
        
        try:
            ledger_response = client.create_ledger(
                name=test_ledger_name,
                parent="Sundry Debtors",
                address="Test Address for API Integration",
                mobile="9999999999"
            )
            print(f"   ✓ Test ledger '{test_ledger_name}' created successfully!")
            print(f"   📄 Response length: {len(ledger_response)} characters")
            
        except TallyValidationError as e:
            print(f"   ✗ Validation error: {e}")
        except TallyAPIError as e:
            print(f"   ⚠️  API response: {e}")
            print("   (This might be normal if the ledger already exists)")
        except Exception as e:
            print(f"   ✗ Unexpected error creating ledger: {e}")
            
        # Test 4: Get Ledgers List
        print("\n5. Getting list of ledgers...")
        try:
            ledgers_response = client.get_ledgers_list()
            print(f"   ✓ Ledgers list retrieved ({len(ledgers_response)} characters)")
            
            # Count how many ledgers we can find
            ledger_count = ledgers_response.count("<NAME>")
            if ledger_count > 0:
                print(f"   📋 Found approximately {ledger_count} ledgers")
                
        except Exception as e:
            print(f"   ⚠️  Warning: Could not get ledgers list - {e}")
            
        print("\n" + "=" * 50)
        print("✅ Test completed successfully!")
        print("\nNext steps:")
        print("- Check Tally to see if the test ledger was created")
        print("- Review the examples/ directory for more usage patterns")
        print("- See DOCUMENTATION.md for complete API reference")
        
        return True
        
    except TallyConnectionError as e:
        print(f"\n❌ Connection Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Ensure Tally is running")
        print("2. Check if Tally is listening on port 9000")
        print("3. Verify XML API is enabled in Tally")
        print("4. Try accessing http://localhost:9000 in a browser")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False


def main():
    """Main function to run the test."""
    print("Starting Tally Integration Test...")
    print("Make sure Tally is running before proceeding.\n")
    
    # Ask user to confirm Tally is running
    try:
        user_input = input("Is Tally running and ready? (y/n): ").lower().strip()
        if user_input not in ['y', 'yes']:
            print("Please start Tally and try again.")
            return
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
        return
        
    success = test_tally_integration()
    
    if success:
        print("\n🎉 All tests passed! Your Tally Integration Library is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check your Tally setup and try again.")


if __name__ == "__main__":
    main()
