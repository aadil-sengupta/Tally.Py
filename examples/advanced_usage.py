"""
Advanced examples for Tally Integration Library

This script demonstrates advanced operations like:
- Company creation
- Voucher management
- Stock item creation
- Report generation
"""

from tally_integration import TallyClient, TallyConnectionError, TallyAPIError
from datetime import datetime


def create_sample_company(client):
    """Create a sample company with full details."""
    print("Creating a sample company...")
    
    try:
        response = client.create_company(
            company_name="Sample API Company Ltd",
            mailing_name="Sample API Company",
            address_list=[
                "Plot No. 123, API Street",
                "Technology Park",
                "New Delhi - 110001"
            ],
            state="Delhi",
            country="India",
            email="info@sampleapi.com",
            financial_year_from="20240401",  # April 1, 2024
            books_from="20240401",
            enable_bill_wise=True,
            enable_inventory=True
        )
        print("✓ Company created successfully!")
        return response
    except Exception as e:
        print(f"✗ Error creating company: {e}")
        return None


def create_sample_ledgers(client):
    """Create sample ledgers for different purposes."""
    print("\nCreating sample ledgers...")
    
    ledgers_to_create = [
        {
            "name": "ABC Suppliers Pvt Ltd",
            "parent": "Sundry Creditors",
            "address": "456 Supplier Street, Mumbai",
            "state": "Maharashtra",
            "gstin": "27ABCDE1234F1Z5"
        },
        {
            "name": "XYZ Customers Ltd", 
            "parent": "Sundry Debtors",
            "address": "789 Customer Avenue, Bangalore",
            "state": "Karnataka",
            "mobile": "9876543210"
        },
        {
            "name": "Professional Fees",
            "parent": "Indirect Expenses"
        }
    ]
    
    for ledger in ledgers_to_create:
        try:
            response = client.create_ledger(**ledger)
            print(f"✓ Created ledger: {ledger['name']}")
        except Exception as e:
            print(f"✗ Error creating ledger {ledger['name']}: {e}")


def create_sample_stock_items(client):
    """Create sample stock items."""
    print("\nCreating sample stock items...")
    
    items_to_create = [
        {
            "name": "Laptop Computer",
            "base_unit": "Nos",
            "opening_balance": 10,
            "hsn_code": "8471",
            "gst_rate": 18.0
        },
        {
            "name": "Office Chair",
            "base_unit": "Nos", 
            "opening_balance": 25,
            "hsn_code": "9401",
            "gst_rate": 18.0
        },
        {
            "name": "A4 Paper",
            "base_unit": "Reams",
            "opening_balance": 100,
            "hsn_code": "4802",
            "gst_rate": 12.0
        }
    ]
    
    for item in items_to_create:
        try:
            response = client.create_stock_item(**item)
            print(f"✓ Created stock item: {item['name']}")
        except Exception as e:
            print(f"✗ Error creating stock item {item['name']}: {e}")


def create_sample_vouchers(client):
    """Create sample vouchers."""
    print("\nCreating sample vouchers...")
    
    today = datetime.now().strftime("%Y%m%d")
    
    try:
        # Create a receipt voucher
        response = client.create_receipt_voucher(
            party_ledger_name="XYZ Customers Ltd",
            amount=50000,
            date=today,
            narration="Payment received for invoice #INV001"
        )
        print("✓ Created receipt voucher")
        
    except Exception as e:
        print(f"✗ Error creating receipt voucher: {e}")


def demonstrate_reports(client):
    """Demonstrate report generation capabilities."""
    print("\nDemonstrating report capabilities...")
    
    try:
        # Get license information
        license_info = client.get_license_info()
        print("✓ Retrieved license information")
        
        # Get companies list with details
        companies = client.get_companies_list(include_simple_companies=True)
        print("✓ Retrieved companies list with simple companies")
        
    except Exception as e:
        print(f"✗ Error generating reports: {e}")


def main():
    """Main advanced example function."""
    
    # Initialize client
    client = TallyClient()
    
    try:
        print("Advanced Tally Integration Examples")
        print("=" * 40)
        
        # Test connection first
        if not client.test_connection():
            print("✗ Cannot connect to Tally. Please ensure Tally is running.")
            return
            
        print("✓ Connected to Tally successfully!")
        
        # Run advanced examples
        #create_sample_company(client)
        create_sample_ledgers(client)
        create_sample_stock_items(client)
        create_sample_vouchers(client)
        demonstrate_reports(client)
        
        print("\n" + "=" * 40)
        print("✓ All advanced operations completed!")
        print("\nNote: Check your Tally application to see the created data.")
        
    except TallyConnectionError as e:
        print(f"✗ Connection Error: {e}")
    except TallyAPIError as e:
        print(f"✗ API Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
