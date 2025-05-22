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
            
    def get_current_company(self):
        """
        Get current company name from Tally
        
        Returns:
            str: Current company name
        """
        xml_request = """<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE>
        <ID>GetCurrentCompanyNameReport</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <REPORT NAME="GetCurrentCompanyNameReport" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
                        <FORMS>CompanyNameForm</FORMS>
                    </REPORT>
                    <FORM NAME="CompanyNameForm" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
                        <TOPPARTS>CompanyNamePart</TOPPARTS>
                        <XMLTAG>COMPANY</XMLTAG>
                    </FORM>
                    <PART NAME="CompanyNamePart" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
                        <TOPLINES>CompanyNameLine</TOPLINES>
                        <SCROLLED>Vertical</SCROLLED>
                    </PART>
                    <LINE NAME="CompanyNameLine" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
                        <LEFTFIELDS>CompanyNameField</LEFTFIELDS>
                    </LINE>
                    <FIELD NAME="CompanyNameField" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
                        <SET>##SVCURRENTCOMPANY</SET>
                        <XMLTAG>NAME</XMLTAG>
                    </FIELD>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    # -------------------- Collections --------------------
    
    def get_sales_report(self):
        """
        Fetches all Sales Vouchers for Current Period
        
        Returns:
            str: XML response with sales vouchers
        """
        xml_request = """<ENVELOPE>
<HEADER>
<VERSION>1</VERSION>
<TALLYREQUEST>EXPORT</TALLYREQUEST>
<TYPE>COLLECTION</TYPE>
<ID>Sales Vouchers</ID>
</HEADER>
<BODY>
<DESC>
<STATICVARIABLES>
<SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
</STATICVARIABLES>
<TDL>
<TDLMESSAGE>

</TDLMESSAGE>
</TDL>
</DESC>
</BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_companies_list(self, include_simple_companies=False):
        """
        Get list of companies from Tally
        
        Args:
            include_simple_companies (bool): Include simple companies in the list
            
        Returns:
            str: XML response with company list
        """
        simple_companies_value = "No" if not include_simple_companies else "Yes"
        
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Collection</TYPE>
        <ID>List of Companies</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
            <SVIsSimpleCompany>{simple_companies_value}</SVIsSimpleCompany>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <COLLECTION ISMODIFY="No" ISFIXED="No" ISINITIALIZE="Yes" ISOPTION="No" ISINTERNAL="No" NAME="List of Companies">
                    
                        <TYPE>Company</TYPE>
                        <NATIVEMETHOD>Name</NATIVEMETHOD>
                    </COLLECTION>
                    <ExportHeader>EmpId:5989</ExportHeader>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_ledgers_list(self, company_name=None):
        """
        Get list of ledgers from Tally
        
        Args:
            company_name (str): Company name
            
        Returns:
            str: XML response with ledgers list
        """
        company_element = f"<SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>" if company_name else ""
        
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Collection</TYPE>
        <ID>Ledgers</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                {company_element}
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <COLLECTION ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="Ledgers">
                        <TYPE>Ledger</TYPE>
                        <NATIVEMETHOD>Address</NATIVEMETHOD>
                        <NATIVEMETHOD>Masterid</NATIVEMETHOD>
                        <NATIVEMETHOD>*</NATIVEMETHOD>
                    </COLLECTION>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_stock_items_list(self):
        """
        Get list of stock items from Tally
        
        Returns:
            str: XML response with stock items list
        """
        xml_request = """<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Collection</TYPE>
        <ID>Custom List of StockItems</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES />
            <TDL>
                <TDLMESSAGE>
                    <COLLECTION ISMODIFY="No" ISFIXED="No" ISINITIALIZE="Yes" ISOPTION="No" ISINTERNAL="No" NAME="Custom List of StockItems">
                        <TYPE>StockItem</TYPE>
                        <NATIVEMETHOD>MasterID</NATIVEMETHOD>
                        <NATIVEMETHOD>GUID</NATIVEMETHOD>
                    </COLLECTION>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""