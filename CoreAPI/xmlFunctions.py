import requests
import xml.etree.ElementTree as ET
import logging
import sys # For basic logging config

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout # Log to standard output
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
        
        return self._send_request(xml_request)
    
    def get_vouchers_by_type(self, company_name, from_date, to_date, voucher_type="Attendance"):
        """
        Get vouchers by type
        
        Args:
            company_name (str): Company name
            from_date (str): From date (format: 01-Apr-2010)
            to_date (str): To date (format: 04-Jun-2021)
            voucher_type (str): Voucher type (default: Attendance)
            
        Returns:
            str: XML response with vouchers
        """
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE>
        <ID>List Of Vouchers</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                <SVFROMDATE TYPE="Date">{from_date}</SVFROMDATE>
                <SVTODATE TYPE="Date">{to_date}</SVTODATE>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <REPORT ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="List Of Vouchers">
                        <FORMS>List Of Vouchers</FORMS>
                    </REPORT>
                    <FORM ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="List Of Vouchers">
                        <TOPPARTS>List Of Vouchers</TOPPARTS>
                        <XMLTAG>ListOfVouchers</XMLTAG>
                    </FORM>
                    <PART ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="List Of Vouchers">
                        <TOPLINES>List Of Vouchers</TOPLINES>
                        <REPEAT>List Of Vouchers : FormList Of Vouchers</REPEAT>
                        <SCROLLED>Vertical</SCROLLED>
                    </PART>
                    <LINE ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="List Of Vouchers">
                        <LEFTFIELDS>MASTERID</LEFTFIELDS>
                        <LEFTFIELDS>VoucherNumber</LEFTFIELDS>
                        <LEFTFIELDS>Date</LEFTFIELDS>
                    </LINE>
                    <FIELD ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="MASTERID">
                        <SET>$MASTERID</SET>
                        <XMLTAG>MASTERID</XMLTAG>
                    </FIELD>
                    <FIELD ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="VoucherNumber">
                        <SET>$VoucherNumber</SET>
                        <XMLTAG>VoucherNumber</XMLTAG>
                    </FIELD>
                    <FIELD ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="Date">
                        <SET>$Date</SET>
                        <XMLTAG>Date</XMLTAG>
                    </FIELD>
                    <COLLECTION ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="FormList Of Vouchers">
                        <TYPE>Voucher</TYPE>
                        <FILTERS>VoucherType</FILTERS>
                    </COLLECTION>
                    <SYSTEM TYPE="Formulae" NAME="VoucherType">$VoucherTypeName = "{voucher_type}"</SYSTEM>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_groups_list(self):
        """
        Get list of groups from Tally
        
        Returns:
            str: XML response with groups list
        """
        xml_request = """<ENVELOPE>
     <HEADER>
            <VERSION>1</VERSION>
            <TALLYREQUEST>Export</TALLYREQUEST>
            <TYPE>Collection</TYPE>
            <ID>Collection of Ledgers</ID>
     </HEADER>
<BODY>
<DESC>
<TDL>
<TDLMESSAGE>
<OBJECT NAME="LicenseInfo" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
  <LOCALFORMULA>IsEducationalMode: $SV_LICENSE_TRIAL</LOCALFORMULA>
  <LOCALFORMULA>IsSilver: $SV_LICENSE_SILVER</LOCALFORMULA>
   <LOCALFORMULA>Folderpath:$SVCURRENTCOMPANY</LOCALFORMULA>
   <LOCALFORMULA>LicenseName:
   If $SV_LICENSE_TRIAL Then $$LocaleString:"Educational Version"  
   ELSE
   If $SV_LICENSE_SILVER Then $$LocaleString:"Silver" 
   ELSE
    If $SV_LICENSE_GOLD Then $$LocaleString:"Gold" 
   else ""</LOCALFORMULA>
  </OBJECT>
<COLLECTION NAME="Collection of Ledgers" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
  <OBJECTS> LicenseInfo</OBJECTS>  
  <NATIVEMETHOD>IsEducationalMode</NATIVEMETHOD>
  </COLLECTION>

  </TDLMESSAGE>
  </TDL>

</DESC>
</BODY>
</ENVELOPE>
"""
        
        return self._send_request(xml_request)
    
    def get_groups_list(self, company_name=None):
        """
        Get list of groups from Tally

        Args:
            company_name (str, optional): Company name. If None, uses the currently selected company.

        Returns:
            str: XML response with groups list
        """
        company_element = f"<SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>" if company_name else ""

        xml_request = f"""<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Collection</TYPE>
        <ID>List of Groups</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                {company_element}
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <COLLECTION NAME="List of Groups" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
                        <TYPE>Group</TYPE>
                        <FETCH>Name, Parent, MasterID</FETCH>
                    </COLLECTION>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""

        return self._send_request(xml_request)

    # -------------------- Reports --------------------
    
    def get_payslip(self, from_date, to_date, employee_name):
        """
        Get employee payslip
        
        Args:
            from_date (str): From date (format: YYYYMMDD)
            to_date (str): To date (format: YYYYMMDD)
            employee_name (str): Employee name
            
        Returns:
            str: PDF data of payslip
        """
        xml_request = f"""<ENVELOPE>
<HEADER>
<TALLYREQUEST>Export Data</TALLYREQUEST>
</HEADER>
<BODY>
<EXPORTDATA>
<REQUESTDESC>
<REPORTNAME>SelectiveEmployeePaySlip</REPORTNAME>
<STATICVARIABLES>
<SVEXPORTFORMAT>$$SysName:pdf</SVEXPORTFORMAT>
<SVFROMDATE>{from_date}</SVFROMDATE>
<SVTODATE>{to_date}</SVTODATE>
<CostCentreName>{employee_name}</CostCentreName>
</STATICVARIABLES>
</REQUESTDESC>
</EXPORTDATA>
</BODY>
</ENVELOPE>"""
        
        try:
            # Send request specifically for this function to handle binary content
            response = requests.post(self.endpoint, data=xml_request)
            if response.status_code == 200:
                # Return raw byte content for PDF
                return response.content
            else:
                logging.error(f"Error fetching payslip: HTTP {response.status_code} - {response.text[:200]}...")
                return f"Error: HTTP {response.status_code}"
        except Exception as e:
            logging.exception("Error occurred during get_payslip request.")
            return f"Error: {str(e)}"
    
    def get_sales_report_voucher_register(self, from_date, to_date, company_name, voucher_type="Sales"):
        """
        Get sales report using the Voucher Register
        
        Args:
            from_date (str): From date (format: YYYYMMDD)
            to_date (str): To date (format: YYYYMMDD)
            company_name (str): Company name
            voucher_type (str): Voucher type (default: Sales)
            
        Returns:
            str: XML response with sales report
        """
        xml_request = f"""<ENVELOPE>
  <HEADER>
    <VERSION>1</VERSION>
    <TALLYREQUEST>EXPORT</TALLYREQUEST>
    <TYPE>DATA</TYPE>
    <ID>Voucher Register</ID>
  </HEADER>
  <BODY>
    <DESC>
      <STATICVARIABLES>
        <SVEXPORTFORMAT>$$SysName:xml</SVEXPORTFORMAT>
        <SVFROMDATE TYPE="DATE">{from_date}</SVFROMDATE>
        <SVTODATE TYPE="DATE">{to_date}</SVTODATE>
        <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
        <VOUCHERTYPENAME TYPE="STRING">{voucher_type}</VOUCHERTYPENAME>
      </STATICVARIABLES>
    </DESC>
  </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_bill_receivables(self, from_date, to_date, company_name):
        """
        Get bill receivables report
        
        Args:
            from_date (str): From date (format: DD-MMM-YYYY)
            to_date (str): To date (format: DD-MMM-YYYY)
            company_name (str): Company name
            
        Returns:
            str: XML response with bill receivables
        """
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <STATICVARIABLES>
                    <SVViewName>Accounting Voucher View</SVViewName>
                    <SVFROMDATE>{from_date}</SVFROMDATE>
                    <SVTODATE>{to_date}</SVTODATE>
                    <SVEXPORTFORMAT>$$SysName:xml</SVEXPORTFORMAT>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
                <REPORTNAME>Bills Receivable</REPORTNAME>
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_ledger_vouchers(self, from_date, to_date, ledger_name="Sales"):
        """
        Get vouchers for a specific ledger
        
        Args:
            from_date (str): From date
            to_date (str): To date
            ledger_name (str): Ledger name (default: Sales)
            
        Returns:
            str: XML response with ledger vouchers
        """
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Collection</TYPE>
        <ID>Vouchers</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                <SVViewName>Accounting Voucher View</SVViewName>
                <SVFROMDATE>{from_date}</SVFROMDATE>
                <SVTODATE TYPE="Date">{to_date}</SVTODATE>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <COLLECTION ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="Vouchers">
                        <TYPE> Vouchers</TYPE>
                        <Childof>{ledger_name}</Childof>
                        <NATIVEMETHOD>*</NATIVEMETHOD>
                    
                    </COLLECTION>
  
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_group_vouchers(self, from_date, to_date, group_name="Sales Accounts"):
        """
        Get vouchers for a specific group
        
        Args:
            from_date (str): From date
            to_date (str): To date
            group_name (str): Group name (default: Sales Accounts)
            
        Returns:
            str: XML response with group vouchers
        """
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Collection</TYPE>
        <ID>Vouchers</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                <SVViewName>Accounting Voucher View</SVViewName>
                <SVFROMDATE TYPE="Date">{from_date}</SVFROMDATE>
                <SVTODATE TYPE="Date">{to_date}</SVTODATE>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <COLLECTION ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="Vouchers">
                        <TYPE>Voucher</TYPE>
                        <CHILDOF>{group_name}</CHILDOF>
                        <NATIVEMETHOD>*</NATIVEMETHOD>
                    
                    </COLLECTION>
  
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)