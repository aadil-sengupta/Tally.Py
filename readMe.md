# Tally Integration Library

## Overview

This library provides a comprehensive collection of Python functions and XML structures for integrating with TallyPrime, the leading accounting and business management software. It serves as a developer toolkit for building applications, automations, and integrations that interact with Tally's XML API.

The library includes ready-to-use functions for common Tally operations, well-structured XML request templates, and extensive documentation to help developers create robust Tally-based solutions without having to learn the intricacies of Tally's XML API from scratch.

## What's Included

### Core Components

**Python TallyClient Class (`xmlFunctions.py`)**: A comprehensive client library with methods for:
- **Data Retrieval**: Get companies, ledgers, stock items, vouchers, groups, and reports
- **Master Data Management**: Create and manage ledgers, stock items, companies, and units  
- **Transaction Processing**: Create vouchers (receipts, journals), update and cancel transactions
- **Reports & Analytics**: Generate sales reports, payslips, bill receivables, stock aging, and more
- **Company Configuration**: Set up GST, configure features, and manage company settings

**Experimental TDL Files**: A collection of cutting-edge Tally Definition Language (TDL) files that push the boundaries of Tally integration:
- **Advanced API Integrations**: TDLs that can be loaded directly into Tally for enhanced control
- **Custom Function Libraries**: Extended functionality beyond default Tally capabilities  
- **Voucher Processing**: Advanced voucher manipulation and filtering
- **Company Management**: Automated company import and configuration
- **Report Customization**: Custom report definitions and data extraction
- **AI Integration Experiments**: TDLs designed to work with AI services (Claude, AI Studio)

These experimental TDLs represent a new approach to Tally integration - by placing them in specific directories and executing through APIs, developers can gain significantly more control over Tally than what's typically allowed by default.

**Documentation & References**: Comprehensive developer materials including:
- **Tally Developer Reference Guide**: Complete technical documentation for TDL and XML API
- **TDL Reference Manual**: Official reference from a previous Tally version (PDF format)
- **Tally Functions Guide**: Comprehensive PDF documenting all available Tally functions
- **Troubleshooting Guides**: Common issues and solutions for Tally integration
- **XML API Documentation**: Detailed specifications for Tally's XML interface

## Experimental TDL Integration

### Advanced Tally Control

This library includes experimental TDL files that represent a breakthrough approach to Tally integration. Unlike traditional XML API calls, these TDLs can be:

- **Dynamically Loaded**: Placed in specific Tally directories and loaded at runtime
- **API Executed**: Triggered through API calls for enhanced automation
- **Deeply Integrated**: Access internal Tally functions not exposed through standard XML API
- **Highly Customizable**: Create entirely new workflows and business logic within Tally

### Current Experimental Features

The experimental TDL collection includes:
- **AI Service Integration**: Direct connections to Claude and AI Studio for intelligent processing
- **Advanced Voucher Operations**: Complex filtering, searching, and manipulation capabilities
- **Custom Report Generation**: Reports that go beyond standard Tally reporting limitations  
- **Company Automation**: Automated company setup and configuration processes
- **Extended API Functions**: Access to Tally functions not available through traditional methods

**Note**: These experimental TDLs are still under active development and may require specific Tally configurations or versions to function properly.

## Installation

### From Wheel File

Install directly from the pre-built wheel file:

```bash
pip install dist/tally_integration-1.0.0-py3-none-any.whl
```

### From Source

Clone and install from the repository:

```bash
# Clone the repository
git clone https://github.com/aadil-sengupta/Tally.Py.git
cd Tally.Py

# Install the package
pip install -e .
```

### Requirements
- Python 3.7 or higher
- Tally.ERP 9 or TallyPrime with XML API enabled
- Network access to Tally server (default: localhost:9000)
- `requests` library (automatically installed as dependency)

## Quick Start

```python
from tally_integration import TallyClient, TallyConnectionError

# Initialize client (default: http://localhost:9000)
client = TallyClient()

# For remote Tally server:
# client = TallyClient(tally_url="http://192.168.1.100", tally_port=9000)

try:
    # Test connection
    if client.test_connection():
        print("✓ Connected to Tally!")
        
        # Get company information
        company_info = client.get_current_company()
        print("Current company info retrieved")
        
        # Create a new ledger
        response = client.create_ledger(
            name="Test API Customer",
            parent="Sundry Debtors",
            address="123 Test Street, Test City",
            mobile="9999999999"
        )
        print("✓ New ledger created!")
        
    else:
        print("✗ Cannot connect to Tally. Please ensure Tally is running.")
        
except TallyConnectionError as e:
    print(f"Connection error: {e}")
```

For more examples, see the `examples/` directory and check `DOCUMENTATION.md` for comprehensive API reference.

## Key Features

*   **Complete XML API Coverage**: Functions for most common Tally operations including data export, import, and manipulation
*   **Ready-to-Use**: Pre-built functions that handle XML construction and parsing
*   **Extensible**: Well-structured code that can be easily extended for custom requirements
*   **Battle-Tested**: Most functions have been tested with real Tally instances
*   **Developer-Friendly**: Clear function signatures, comprehensive docstrings, and logical organization

## Function Categories

### Data Collections & Reports
- Company and ledger listings
- Stock item and voucher collections  
- Sales reports and financial statements
- Stock aging and inventory reports
- Custom filtered data retrieval

### Master Data Operations
- Create/update/delete ledgers and groups
- Stock item and unit management
- Company creation and configuration
- GST setup and compliance features

### Transaction Management  
- Voucher creation (sales, purchase, receipt, payment, journal)
- Transaction updates and cancellations
- Bulk data imports and exports
- Real-time data synchronization

### Administrative Functions
- Company configuration and feature toggles
- User management and access control
- License information and system status
- Data validation and error handling

## Target Developers

This library is designed for:

*   **Software Developers**: Building ERP integrations, accounting software, or business applications
*   **System Integrators**: Connecting Tally with e-commerce platforms, CRMs, or other business systems  
*   **Automation Engineers**: Creating scripts for data migration, report generation, or routine operations
*   **Business Application Developers**: Building custom Tally-based solutions for specific industries
*   **API Integration Specialists**: Working on real-time data exchange between Tally and external systems

## Important Notes

**Testing Status**: Most functions have been tested and work reliably, but some may contain bugs or edge cases that need handling in production environments. Thorough testing is recommended before deploying in critical business scenarios.

**Version Compatibility**: Functions are designed primarily for TallyPrime, with many also compatible with Tally.ERP 9. Always verify compatibility with your specific Tally version.

**API Dependencies**: Requires Tally to be running with XML API enabled (typically on port 9000). Network connectivity and proper Tally configuration are prerequisites.
