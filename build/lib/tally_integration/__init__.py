"""
Tally Integration Library

A comprehensive Python library for integrating with TallyPrime and Tally.ERP 9
through XML API and TDL (Tally Definition Language) files.

This library provides:
- Ready-to-use functions for common Tally operations
- XML request/response handling
- Master data management
- Transaction processing
- Report generation
- Company configuration
"""

from .client import TallyClient
from .exceptions import (
    TallyError, 
    TallyConnectionError, 
    TallyAPIError, 
    TallyValidationError,
    TallyXMLError
)

__version__ = "1.0.0"
__author__ = "Aadil Sengupta"
__email__ = "aadil.sengupta@example.com"  # Update with your actual email
__description__ = "A comprehensive Python library for TallyPrime integration"

__all__ = [
    "TallyClient",
    "TallyError", 
    "TallyConnectionError",
    "TallyAPIError",
    "TallyValidationError",
    "TallyXMLError",
]
