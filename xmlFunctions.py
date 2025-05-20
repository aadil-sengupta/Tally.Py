import requests
import xml.etree.ElementTree as ET
import logging
import sys

#basic logging configuration

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout 
)


class TallyClient:
    def __init__(self, tally_url="http://localhost", tally_port=9000):
        """
        Initialize TallyClient with server URL and port
        
        Args:
            tally_url (str): Tally server URL
            tally_port (int): Tally server port
        """
        self.tally_url = tally_url
        self.tally_port = tally_port
        self.endpoint = f"{tally_url}:{tally_port}"
        
    def _send_request(self, xml_request):
        """
        Send XML request to Tally server
        
        Args:
            xml_request (str): XML request string
            
        Returns:
            str: XML response from Tally
        """
        try:
            response = requests.post(self.endpoint, data=xml_request)
            if response.status_code == 200:
                return response.text
            else:
                return f"Error: HTTP {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_connection(self):
        """
        Test connection to Tally server
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            response = requests.post(self.endpoint, data="")
            return response.status_code == 200
        except:
            return False


