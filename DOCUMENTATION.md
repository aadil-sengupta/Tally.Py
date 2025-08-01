# Tally Integration Library Documentation

## Overview

The Tally Integration Library is a comprehensive Python package that provides a simple and powerful interface for integrating with Tally accounting software (TallyPrime and Tally.ERP 9) through XML API.

## Features

- **Easy Connection Management**: Simple client setup with automatic error handling
- **Comprehensive API Coverage**: Support for companies, ledgers, vouchers, stock items, and more
- **Robust Error Handling**: Custom exception hierarchy for better error management
- **Type Safety**: Full type hints for better development experience
- **Documentation**: Comprehensive documentation and examples
- **TDL Support**: Includes experimental TDL files for advanced integrations

## Installation

```bash
pip install tally-integration
```

## Quick Start

```python
from tally_integration import TallyClient

# Initialize client (default: http://localhost:9000)
client = TallyClient()

# Test connection
if client.test_connection():
    print("Connected to Tally successfully!")
    
    # Get current company
    company_info = client.get_current_company()
    
    # Get list of ledgers
    ledgers = client.get_ledgers_list()
    
    # Create a new ledger
    response = client.create_ledger(
        name="Test Customer",
        parent="Sundry Debtors",
        address="123 Test Street"
    )
```

## API Reference

### TallyClient Class

The main client class for interacting with Tally.

#### Initialization

```python
TallyClient(tally_url="http://localhost", tally_port=9000, timeout=30)
```

**Parameters:**
- `tally_url` (str): Tally server URL
- `tally_port` (int): Tally server port
- `timeout` (int): Request timeout in seconds

#### Connection Methods

##### test_connection()
Test connection to Tally server.

**Returns:** `bool` - True if connection successful

```python
if client.test_connection():
    print("Tally is accessible")
```

##### get_current_company()
Get current company information from Tally.

**Returns:** `str` - XML response with company information

### Company Management

##### create_company(company_name, **kwargs)
Create a new company in Tally.

**Parameters:**
- `company_name` (str): Name of the company (required)
- `mailing_name` (str, optional): Mailing name
- `address_list` (List[str], optional): List of address lines
- `state` (str, optional): State name
- `pincode` (str, optional): Pincode
- `country` (str, optional): Country name
- `email` (str, optional): Email address
- `financial_year_from` (str, optional): Financial year start date (YYYYMMDD)
- `books_from` (str, optional): Books start date (YYYYMMDD)
- `base_currency_symbol` (str, optional): Currency symbol (default: ₹)
- `base_currency_formal_name` (str, optional): Currency name (default: Indian Rupees)
- `enable_bill_wise` (bool, optional): Enable bill-wise details (default: True)
- `enable_cost_centers` (bool, optional): Enable cost centers (default: False)
- `enable_inventory` (bool, optional): Enable inventory (default: True)

**Returns:** `str` - XML response confirming creation

```python
response = client.create_company(
    company_name="My Company Ltd",
    mailing_name="My Company",
    address_list=["123 Business St", "Business City"],
    state="State Name",
    email="info@mycompany.com"
)
```

##### get_companies_list(include_simple_companies=False)
Get list of companies from Tally.

**Parameters:**
- `include_simple_companies` (bool): Include simple companies

**Returns:** `str` - XML response with company list

### Ledger Management

##### create_ledger(name, **kwargs)
Create a new ledger in Tally.

**Parameters:**
- `name` (str): Name of the ledger (required)
- `parent` (str, optional): Parent ledger/group name
- `address` (str, optional): Address of the party
- `country` (str, optional): Country of residence
- `state` (str, optional): State name
- `mobile` (str, optional): Mobile number
- `gstin` (str, optional): GST Identification Number

**Returns:** `str` - XML response confirming creation

```python
response = client.create_ledger(
    name="ABC Suppliers",
    parent="Sundry Creditors",
    address="456 Supplier Street",
    state="Maharashtra",
    gstin="27ABCDE1234F1Z5"
)
```

##### get_ledgers_list(company_name=None)
Get list of ledgers from Tally.

**Parameters:**
- `company_name` (str, optional): Company name

**Returns:** `str` - XML response with ledgers list

### Stock Management

##### create_stock_item(name, base_unit, **kwargs)
Create a new stock item in Tally.

**Parameters:**
- `name` (str): Name of the stock item (required)
- `base_unit` (str): Base unit for the stock item (required)
- `opening_balance` (float, optional): Opening balance quantity (default: 0)
- `hsn_code` (str, optional): HSN code for the item
- `gst_rate` (float, optional): GST rate percentage

**Returns:** `str` - XML response confirming creation

```python
response = client.create_stock_item(
    name="Laptop Computer",
    base_unit="Nos",
    opening_balance=10,
    hsn_code="8471",
    gst_rate=18.0
)
```

##### create_unit(name, is_simple_unit=True)
Create a new unit in Tally.

**Parameters:**
- `name` (str): Name of the unit (required)
- `is_simple_unit` (bool, optional): Whether it's a simple unit (default: True)

**Returns:** `str` - XML response confirming creation

### Voucher Management

##### create_receipt_voucher(party_ledger_name, amount, **kwargs)
Create a receipt voucher in Tally.

**Parameters:**
- `party_ledger_name` (str): Name of the party ledger (required)
- `amount` (float): Amount to be received (required)
- `date` (str, optional): Voucher date in format YYYYMMDD (default: today)
- `narration` (str, optional): Narration for the voucher (default: "")
- `voucher_number` (str, optional): Voucher number (default: auto-generated)

**Returns:** `str` - XML response confirming creation

```python
response = client.create_receipt_voucher(
    party_ledger_name="XYZ Customer",
    amount=50000,
    narration="Payment received for invoice #INV001"
)
```

### Information and Reports

##### get_license_info()
Get Tally license information.

**Returns:** `str` - XML response with license information

##### parse_xml_response(xml_response)
Parse XML response from Tally into a Python dictionary.

**Parameters:**
- `xml_response` (str): XML response string

**Returns:** `Dict[str, Any]` - Parsed XML response as dictionary

```python
company_info = client.get_current_company()
parsed_data = client.parse_xml_response(company_info)
print(parsed_data)
```

## Exception Handling

The library provides a comprehensive exception hierarchy:

### TallyError
Base exception class for all Tally-related errors.

### TallyConnectionError
Raised when connection to Tally server fails.

```python
from tally_integration import TallyConnectionError

try:
    client.get_current_company()
except TallyConnectionError as e:
    print(f"Connection failed: {e}")
```

### TallyAPIError
Raised when Tally API returns an error response.

```python
from tally_integration import TallyAPIError

try:
    client.create_ledger("Invalid Ledger")
except TallyAPIError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
```

### TallyValidationError
Raised when input validation fails.

```python
from tally_integration import TallyValidationError

try:
    client.create_ledger("")  # Empty name
except TallyValidationError as e:
    print(f"Validation error: {e}")
```

### TallyXMLError
Raised when XML parsing fails.

```python
from tally_integration import TallyXMLError

try:
    client.parse_xml_response("invalid xml")
except TallyXMLError as e:
    print(f"XML parsing error: {e}")
```

## Configuration

### Custom Server Configuration

```python
# Connect to remote Tally server
client = TallyClient(
    tally_url="http://192.168.1.100",
    tally_port=9000,
    timeout=60
)
```

### Error Handling Best Practices

```python
from tally_integration import (
    TallyClient, 
    TallyConnectionError, 
    TallyAPIError, 
    TallyValidationError
)

client = TallyClient()

try:
    # Test connection first
    if not client.test_connection():
        print("Tally is not accessible")
        return
        
    # Perform operations
    response = client.create_ledger(
        name="Test Ledger",
        parent="Sundry Debtors"
    )
    
except TallyConnectionError as e:
    print(f"Connection issue: {e}")
except TallyAPIError as e:
    print(f"Tally API error: {e}")
except TallyValidationError as e:
    print(f"Input validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Advanced Usage

### Batch Operations

```python
# Create multiple ledgers
ledgers = [
    {"name": "Customer 1", "parent": "Sundry Debtors"},
    {"name": "Customer 2", "parent": "Sundry Debtors"},
    {"name": "Supplier 1", "parent": "Sundry Creditors"}
]

for ledger in ledgers:
    try:
        response = client.create_ledger(**ledger)
        print(f"Created: {ledger['name']}")
    except Exception as e:
        print(f"Failed to create {ledger['name']}: {e}")
```

### XML Response Processing

```python
import xml.etree.ElementTree as ET

# Get and process company information
company_xml = client.get_current_company()

# Parse using built-in method
parsed_data = client.parse_xml_response(company_xml)

# Or parse manually for complex structures
root = ET.fromstring(company_xml)
for element in root.iter():
    print(f"{element.tag}: {element.text}")
```

## TDL Files

The package includes experimental TDL (Tally Definition Language) files for advanced integrations. These files are located in the `experimental_tdls` directory and provide additional functionality for custom Tally operations.

## Examples

See the `examples/` directory for complete working examples:

- `basic_usage.py`: Basic operations and connection testing
- `advanced_usage.py`: Advanced operations including company creation and voucher management

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the documentation and examples
- Review the TDL reference files included in the package
- Submit issues on the project repository

## Version History

### 1.0.0
- Initial release
- Core API functionality
- Exception handling
- Documentation and examples
- TDL files integration
