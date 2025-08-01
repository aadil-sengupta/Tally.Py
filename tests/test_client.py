"""
Basic tests for Tally Integration Library
"""

import pytest
from unittest.mock import Mock, patch
import requests

from tally_integration import TallyClient, TallyConnectionError, TallyAPIError, TallyValidationError


class TestTallyClient:
    """Test cases for TallyClient class."""
    
    def setup_method(self):
        """Setup test client."""
        self.client = TallyClient()
        
    def test_init_default_values(self):
        """Test client initialization with default values."""
        assert self.client.tally_url == "http://localhost"
        assert self.client.tally_port == 9000
        assert self.client.timeout == 30
        assert self.client.endpoint == "http://localhost:9000"
        
    def test_init_custom_values(self):
        """Test client initialization with custom values."""
        client = TallyClient(
            tally_url="http://192.168.1.100",
            tally_port=8080,
            timeout=60
        )
        assert client.tally_url == "http://192.168.1.100"
        assert client.tally_port == 8080
        assert client.timeout == 60
        assert client.endpoint == "http://192.168.1.100:8080"
        
    @patch('requests.post')
    def test_send_request_success(self, mock_post):
        """Test successful request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<ENVELOPE><HEADER></HEADER><BODY></BODY></ENVELOPE>"
        mock_post.return_value = mock_response
        
        result = self.client._send_request("<TEST>test</TEST>")
        assert result == "<ENVELOPE><HEADER></HEADER><BODY></BODY></ENVELOPE>"
        
    @patch('requests.post')
    def test_send_request_connection_error(self, mock_post):
        """Test connection error handling."""
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        with pytest.raises(TallyConnectionError):
            self.client._send_request("<TEST>test</TEST>")
            
    @patch('requests.post')
    def test_send_request_timeout(self, mock_post):
        """Test timeout error handling."""
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
        
        with pytest.raises(TallyConnectionError):
            self.client._send_request("<TEST>test</TEST>")
            
    @patch('requests.post')
    def test_send_request_api_error(self, mock_post):
        """Test API error handling."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<ENVELOPE><LINEERROR>Some error</LINEERROR></ENVELOPE>"
        mock_post.return_value = mock_response
        
        with pytest.raises(TallyAPIError):
            self.client._send_request("<TEST>test</TEST>")
            
    @patch('requests.post')
    def test_test_connection_success(self, mock_post):
        """Test successful connection test."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        result = self.client.test_connection()
        assert result is True
        
    @patch('requests.post')
    def test_test_connection_failure(self, mock_post):
        """Test failed connection test."""
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        result = self.client.test_connection()
        assert result is False
        
    def test_create_ledger_validation_error(self):
        """Test ledger creation with invalid parameters."""
        with pytest.raises(TallyValidationError):
            self.client.create_ledger("")  # Empty name should raise validation error
            
    def test_create_company_validation_error(self):
        """Test company creation with invalid parameters."""
        with pytest.raises(TallyValidationError):
            self.client.create_company("")  # Empty name should raise validation error


if __name__ == "__main__":
    pytest.main([__file__])
