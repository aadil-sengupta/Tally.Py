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
        <TYPE>Collection</TYPE>
        <ID>CompanyInfo</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES />
            <TDL>
                <TDLMESSAGE>
                    <OBJECT NAME="CurrentCompany">
                        <LOCALFORMULA>CurrentCompany:##SVCURRENTCOMPANY</LOCALFORMULA>
                    </OBJECT>
                    <COLLECTION NAME="CompanyInfo">
                        <OBJECTS>CurrentCompany</OBJECTS>
                    </COLLECTION>
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
                <SVFROMDATE>{from_date}</SVFROMDATE>
                <SVTODATE TYPE="Date">{to_date}</SVTODATE>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <COLLECTION ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="Vouchers">
                        <TYPE> Vouchers : Group</TYPE>
                        <Childof>{group_name}</Childof>
                        <NATIVEMETHOD>*</NATIVEMETHOD>
                    
                    </COLLECTION>
  
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_stock_vouchers_summary(self, stock_item_name, explode_vnum=True, explode_flag=False):
        """
        Get stock vouchers summary
        
        Args:
            stock_item_name (str): Stock item name
            explode_vnum (bool): Include voucher numbers if True
            explode_flag (bool): Include detailed format if True
            
        Returns:
            str: XML response with stock vouchers summary
        """
        explode_vnum_value = "Yes" if explode_vnum else "No"
        explode_flag_value = "Yes" if explode_flag else "No"
        
        xml_request = f"""<ENVELOPE>
<HEADER>
<VERSION>1</VERSION>
<TALLYREQUEST>Export</TALLYREQUEST>
<TYPE>Data</TYPE>
<ID>Stock Vouchers</ID>
</HEADER>
<BODY>
<DESC>
<STATICVARIABLES>
<SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
<ExplodeVNum>{explode_vnum_value}</ExplodeVNum>
<EXPLODEFLAG>{explode_flag_value}</EXPLODEFLAG>
<StockItemName>{stock_item_name}</StockItemName>
</STATICVARIABLES>
</DESC>
</BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_stock_ageing(self, stock_group_name, from_date, to_date):
        """
        Get stock ageing report
        
        Args:
            stock_group_name (str): Stock group name
            from_date (str): From date (format: DD-MMM-YYYY)
            to_date (str): To date (format: DD-MMM-YYYY)
            
        Returns:
            str: XML response with stock ageing report
        """
        xml_request = f"""<ENVELOPE>
<HEADER>
<VERSION>1</VERSION>
<TALLYREQUEST>Export</TALLYREQUEST>
<TYPE>Data</TYPE>
<ID>StockAgeing</ID>
</HEADER>
<BODY>
<DESC>
<STATICVARIABLES>
<SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
<StockGroupName>{stock_group_name}</StockGroupName>
<StockAgeFrom>{from_date}</StockAgeFrom> <StockAgeTo>{to_date}</StockAgeTo> 
</STATICVARIABLES>
</DESC>
</BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_list_of_accounts(self, from_date="", to_date=""):
        """
        Get list of accounts
        
        Args:
            from_date (str): From date (format: YYMMDD)
            to_date (str): To date (format: YYMMDD)
            
        Returns:
            str: XML response with list of accounts
        """
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>List of Accounts</REPORTNAME>
                <STATICVARIABLES>
                    <SVFROMDATE>{from_date}</SVFROMDATE>
                    <SVTODATE>{to_date}</SVTODATE>
                    <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                </STATICVARIABLES>
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    # -------------------- Objects --------------------
    
    def get_ledger_by_name(self, ledger_name, from_date=None, to_date=None):
        """
        Get ledger by name
        
        Args:
            ledger_name (str): Ledger name
            from_date (str, optional): From date (format: YYYYMMDD)
            to_date (str, optional): To date (format: YYYYMMDD)
            
        Returns:
            str: XML response with ledger details
        """
        date_vars = ""
        if from_date and to_date:
            date_vars = f"""<SVFROMDATE TYPE="Date">{from_date}</SVFROMDATE>
                <SVTODATE TYPE="Date">{to_date}</SVTODATE>"""
        
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
                {date_vars}
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <COLLECTION ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="Ledgers">
                        <TYPE>Ledger</TYPE>
                        <NATIVEMETHOD>Address</NATIVEMETHOD>
                        <NATIVEMETHOD>*</NATIVEMETHOD>
                        <FILTERS>Ledgerfilter</FILTERS>
                    </COLLECTION>
                    <SYSTEM TYPE="Formulae" NAME="Ledgerfilter">$Name="{ledger_name}"</SYSTEM>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_voucher_by_master_id(self, master_id, company_name=None):
        """
        Get voucher by master ID
        
        Args:
            master_id (str): Master ID of voucher
            company_name (str, optional): Company name
            
        Returns:
            str: XML response with voucher details
        """
        company_element = f"<SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>" if company_name else ""
        
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>EXPORT</TALLYREQUEST>
        <TYPE>Object</TYPE>
        <SUBTYPE>VOUCHER</SUBTYPE>
        <ID TYPE="Name">ID:'{master_id}'</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
            {company_element}
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                <SVViewName>Accounting Voucher View</SVViewName>
            </STATICVARIABLES>
            <FETCHLIST>
                <FETCH>*</FETCH>
                
            </FETCHLIST>
        </DESC>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_voucher_by_number_and_date(self, voucher_date, voucher_number, company_name=None):
        """
        Get voucher by number and date
        
        Args:
            voucher_date (str): Voucher date (format: DD-MMM-YYYY)
            voucher_number (str): Voucher number
            company_name (str, optional): Company name
            
        Returns:
            str: XML response with voucher details
        """
        company_element = f"<SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>" if company_name else ""
        
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>EXPORT</TALLYREQUEST>
        <TYPE>Object</TYPE>
        <SUBTYPE>VOUCHER</SUBTYPE>
        <ID TYPE="Name">Date:'{voucher_date}':VoucherNumber:'{voucher_number}'</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
            {company_element}
                <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                <SVViewName>Accounting Voucher View</SVViewName>
            </STATICVARIABLES>
            <FETCHLIST>
                <FETCH>*</FETCH>
                
            </FETCHLIST>
        </DESC>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_stock_item_by_master_id(self, master_id):
        """
        Get stock item by master ID
        
        Args:
            master_id (str): Master ID of stock item
            
        Returns:
            str: XML response with stock item details
        """
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Collection</TYPE>
        <ID>CustColl</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <COLLECTION ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No" NAME="CustColl">
                        <TYPE>masters</TYPE>
                        <NATIVEMETHOD>*</NATIVEMETHOD>
                        <FILTERS>filter</FILTERS>
                    </COLLECTION>
                    <SYSTEM TYPE="Formulae" NAME="filter">$Masterid={master_id}</SYSTEM>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)
    
    def get_license_info(self):
        """
        Get Tally license information
        
        Returns:
            str: XML response with license information
        """
        xml_request = """<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Collection</TYPE>
        <ID>LicenseInfo</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES />
            <TDL>
                <TDLMESSAGE>
                    <OBJECT NAME="LicenseInfo">
                        <LOCALFORMULA>IsEducationalMode:  $$LicenseInfo:IsEducationalMode</LOCALFORMULA>
                        <LOCALFORMULA>IsSilver: $$LicenseInfo:IsSilver</LOCALFORMULA>
                        <LOCALFORMULA>IsGold: $$LicenseInfo:IsGold</LOCALFORMULA>
                        <LOCALFORMULA>PlanName: If $$LicenseInfo:IsEducationalMode Then "Educational Version" ELSE  If $$LicenseInfo:IsSilver Then "Silver" ELSE  If $$LicenseInfo:IsGold Then "Gold" else ""</LOCALFORMULA>
                        <LOCALFORMULA>SerialNumber: $$LicenseInfo:SerialNumber</LOCALFORMULA>
                        <LOCALFORMULA>AccountId:$$LicenseInfo:AccountID</LOCALFORMULA>
                        <LOCALFORMULA>IsIndian: $$LicenseInfo:IsIndian</LOCALFORMULA>
                        <LOCALFORMULA>RemoteSerialNumber: $$LicenseInfo:RemoteSerialNumber</LOCALFORMULA>
                        <LOCALFORMULA>IsRemoteAccessMode: $$LicenseInfo:IsRemoteAccessMode</LOCALFORMULA>
                        <LOCALFORMULA>IsLicClientMode: $$LicenseInfo:IsLicClientMode</LOCALFORMULA>
                        <LOCALFORMULA>AdminMailId:$$LicenseInfo:AdminEmailID</LOCALFORMULA>
                        <LOCALFORMULA>IsAdmin:$$LicenseInfo:IsAdmin</LOCALFORMULA>
                        <LOCALFORMULA>ApplicationPath:$$SysInfo:ApplicationPath</LOCALFORMULA>
                        <LOCALFORMULA>DataPath:##SVCurrentPath</LOCALFORMULA>
                        <LOCALFORMULA>UserLevel:$$cmpusername</LOCALFORMULA>
                    </OBJECT>
                    <COLLECTION NAME="LicenseInfo">
                        <OBJECTS>LicenseInfo</OBJECTS>
                    </COLLECTION>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    def create_ledger(self, name, parent=None, address=None, country=None, state=None, mobile=None, gstin=None):
        """
        Create a new ledger in Tally
        
        Args:
            name (str): Name of the ledger
            parent (str, optional): Parent ledger/group name. Default: None
            address (str, optional): Address of the party. Default: None
            country (str, optional): Country of residence. Default: None
            state (str, optional): State name. Default: None
            mobile (str, optional): Mobile number. Default: None
            gstin (str, optional): GST Identification Number. Default: None
            
        Returns:
            str: XML response confirming creation
        """
        # Building the optional elements
        parent_element = f"<PARENT>{parent}</PARENT>" if parent else ""
        address_element = f"<ADDRESS>{address}</ADDRESS>" if address else ""
        country_element = f"<COUNTRYOFRESIDENCE>{country}</COUNTRYOFRESIDENCE>" if country else ""
        state_element = f"<LEDSTATENAME>{state}</LEDSTATENAME>" if state else ""
        mobile_element = f"<LEDGERMOBILE>{mobile}</LEDGERMOBILE>" if mobile else ""
        gstin_element = f"<PARTYGSTIN>{gstin}</PARTYGSTIN>" if gstin else ""
        
        xml_request = f"""<ENVELOPE>
        <HEADER>
            <TALLYREQUEST>Import Data</TALLYREQUEST>
        </HEADER>
        <BODY>
            <IMPORTDATA>
                <REQUESTDESC>
                    <REPORTNAME>All Masters</REPORTNAME>
                </REQUESTDESC>
                <REQUESTDATA>
                    <TALLYMESSAGE xmlns:UDF="TallyUDF">
                        <LEDGER Action="Create">
                            <NAME>{name}</NAME>
                            {parent_element}
                            {address_element}
                            {country_element}
                            {state_element}
                            {mobile_element}
                            {gstin_element}
                        </LEDGER>
                    </TALLYMESSAGE>
                </REQUESTDATA>
            </IMPORTDATA>
        </BODY>
    </ENVELOPE>"""
        
        return self._send_request(xml_request)

    def create_receipt_voucher(self, party_ledger_name, amount, date=None, narration="", voucher_number=None):
        """
        Create a receipt voucher in Tally
        
        Args:
            party_ledger_name (str): Name of the party ledger
            amount (float): Amount to be received
            date (str, optional): Voucher date in format YYYYMMDD. Default: Today
            narration (str, optional): Narration for the voucher. Default: ""
            voucher_number (str, optional): Voucher number. Default: None (auto-generated)
            
        Returns:
            str: XML response confirming creation
        """
        # Default to today's date if not provided
        if not date:
            from datetime import datetime
            date = datetime.now().strftime("%Y%m%d")
        
        # Optional voucher number
        voucher_number_element = f"<VOUCHERNUMBER>{voucher_number}</VOUCHERNUMBER>" if voucher_number else "<VOUCHERNUMBER></VOUCHERNUMBER>"
        
        xml_request = f"""<ENVELOPE>
        <HEADER>
            <TALLYREQUEST>Import Data</TALLYREQUEST>
        </HEADER>
        <BODY>
            <IMPORTDATA>
                <REQUESTDESC>
                    <REPORTNAME>All Masters</REPORTNAME>
                </REQUESTDESC>
                <REQUESTDATA>
                    <TALLYMESSAGE xmlns:UDF="TallyUDF">
                        <VOUCHER ACTION="Create" VCHTYPE=" Receipt ">
                            <VOUCHERTYPENAME>Receipt</VOUCHERTYPENAME>
                            <DATE>{date}</DATE>
                            {voucher_number_element}
                            <PARTYLEDGERNAME>{party_ledger_name}</PARTYLEDGERNAME>
                            <NARRATION>{narration}</NARRATION>
                            <EFFECTIVEDATE>{date}</EFFECTIVEDATE>
                            <ALLLEDGERENTRIES.LIST>
                                <LEDGERNAME>{party_ledger_name}</LEDGERNAME>
                                <REMOVEZEROENTRIES>NO</REMOVEZEROENTRIES>
                                <LEDGERFROMITEM>NO</LEDGERFROMITEM>
                                <ISDEEMEDPOSITIVE>NO</ISDEEMEDPOSITIVE>
                                <AMOUNT>{amount}</AMOUNT>
                            </ALLLEDGERENTRIES.LIST>
                            <ALLLEDGERENTRIES.LIST>
                                <LEDGERNAME>Cash</LEDGERNAME>
                                <REMOVEZEROENTRIES>NO</REMOVEZEROENTRIES>
                                <LEDGERFROMITEM>NO</LEDGERFROMITEM>
                                <ISDEEMEDPOSITIVE>YES</ISDEEMEDPOSITIVE>
                                <AMOUNT>-{amount}</AMOUNT>
                            </ALLLEDGERENTRIES.LIST>
                        </VOUCHER>
                    </TALLYMESSAGE>
                </REQUESTDATA>
            </IMPORTDATA>
        </BODY>
    </ENVELOPE>"""
        
        return self._send_request(xml_request)

    def create_stock_item(self, name, base_unit, opening_balance=0, hsn_code=None, gst_rate=None):
        """
        Create a new stock item in Tally
        
        Args:
            name (str): Name of the stock item
            base_unit (str): Base unit for the stock item (e.g., "Nos", "Kg")
            opening_balance (float, optional): Opening balance quantity. Default: 0
            hsn_code (str, optional): HSN code for the item. Default: None
            gst_rate (float, optional): GST rate percentage. Default: None
            
        Returns:
            str: XML response confirming creation
        """
        # GST details are complex, only include if HSN code and GST rate are provided
        gst_details = ""
        if hsn_code and gst_rate:
            # Calculate CGST and SGST as half of the GST rate
            half_rate = gst_rate / 2
            
            gst_details = f"""
            <GSTAPPLICABLE>&#4; Applicable</GSTAPPLICABLE>
            <GSTDETAILS.LIST>
                <APPLICABLEFROM>20200401</APPLICABLEFROM>
                <CALCULATIONTYPE>On Value</CALCULATIONTYPE>
                <HSNCODE>{hsn_code}</HSNCODE>
                <TAXABILITY>Taxable</TAXABILITY>
                <STATEWISEDETAILS.LIST>
                    <STATENAME>&#4; Any</STATENAME>
                    <RATEDETAILS.LIST>
                        <GSTRATEDUTYHEAD>Central Tax</GSTRATEDUTYHEAD>
                        <GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE>
                        <GSTRATE> {half_rate}</GSTRATE>
                    </RATEDETAILS.LIST>
                    <RATEDETAILS.LIST>
                        <GSTRATEDUTYHEAD>State Tax</GSTRATEDUTYHEAD>
                        <GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE>
                        <GSTRATE> {half_rate}</GSTRATE>
                    </RATEDETAILS.LIST>
                    <RATEDETAILS.LIST>
                        <GSTRATEDUTYHEAD>Integrated Tax</GSTRATEDUTYHEAD>
                        <GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE>
                        <GSTRATE> {gst_rate}</GSTRATE>
                    </RATEDETAILS.LIST>
                    <RATEDETAILS.LIST>
                        <GSTRATEDUTYHEAD>Cess</GSTRATEDUTYHEAD>
                        <GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE>
                    </RATEDETAILS.LIST>
                </STATEWISEDETAILS.LIST>
            </GSTDETAILS.LIST>"""
        
        xml_request = f"""<ENVELOPE>
        <HEADER>
            <TALLYREQUEST>Import Data</TALLYREQUEST>
        </HEADER>
        <BODY>
            <IMPORTDATA>
                <REQUESTDESC>
                    <REPORTNAME>All Masters</REPORTNAME>
                </REQUESTDESC>
                <REQUESTDATA>
                    <TALLYMESSAGE xmlns:UDF="TallyUDF">
                        <STOCKITEM Action="Create">
                            <NAME>{name}</NAME>
                            <BASEUNITS>{base_unit}</BASEUNITS>
                            <OPENINGBALANCE>{opening_balance}</OPENINGBALANCE>
                            {gst_details}
                        </STOCKITEM>
                    </TALLYMESSAGE>
                </REQUESTDATA>
            </IMPORTDATA>
        </BODY>
    </ENVELOPE>"""
        
        return self._send_request(xml_request)

    def create_unit(self, name, is_simple_unit=True):
        """
        Create a new unit in Tally
        
        Args:
            name (str): Name of the unit (e.g., "Nos", "Kg")
            is_simple_unit (bool, optional): Whether it's a simple unit. Default: True
            
        Returns:
            str: XML response confirming creation
        """
        is_simple = "true" if is_simple_unit else "false"
        
        xml_request = f"""<ENVELOPE>
        <HEADER>
            <TALLYREQUEST>Import Data</TALLYREQUEST>
        </HEADER>
        <BODY>
            <IMPORTDATA>
                <REQUESTDESC>
                    <REPORTNAME>All Masters</REPORTNAME>
                </REQUESTDESC>
                <REQUESTDATA>
                    <TALLYMESSAGE xmlns:UDF="TallyUDF">
                        <UNIT Action="Create">
                            <ISSIMPLEUNIT>{is_simple}</ISSIMPLEUNIT>
                            <NAME>{name}</NAME>
                        </UNIT>
                    </TALLYMESSAGE>
                </REQUESTDATA>
            </IMPORTDATA>
        </BODY>
    </ENVELOPE>"""
        
        return self._send_request(xml_request)

    # Example usage of parsing XML response
    def parse_xml_response(self, xml_response):
        """
        Parse XML response from Tally
        
        Args:
            xml_response (str): XML response string
            
        Returns:
            dict: Parsed XML response as dictionary
        """
        try:
            root = ET.fromstring(xml_response)
            # Implement parsing logic based on specific requirements
            # This is a simple example that will need customization based on the actual XML structure
            result = {}
            
            # Very basic parsing - extract all text content
            for elem in root.iter():
                if elem.text and elem.text.strip():
                    result[elem.tag] = elem.text.strip()
                    
            return result
        except Exception as e:
            return {"error": str(e)}

    # -------------------- Company Management --------------------
    
    def create_company(self, company_name, mailing_name=None, address_list=None, state=None,
                       pincode=None, country=None, email=None, financial_year_from="20250401", # Changed default format
                       books_from="20250401", # Changed default format
                       base_currency_symbol="₹", 
                       base_currency_formal_name="Indian Rupees", enable_bill_wise=True, 
                       enable_cost_centers=False, enable_inventory=True):
        """
        Create a new company in Tally
        
        Args:
            company_name (str): Name of the company
            mailing_name (str, optional): Mailing name of the company. Default: Same as company_name
            address_list (list, optional): List of address lines. Default: None
            state (str, optional): State name. Default: None
            pincode (str, optional): Pincode. Default: None
            country (str, optional): Country name. Default: None
            email (str, optional): Email address. Default: None
            financial_year_from (str, optional): Financial year from date (format: YYYYMMDD). Default: 20250401
            books_from (str, optional): Books from date (format: YYYYMMDD). Default: 20250401
            base_currency_symbol (str, optional): Base currency symbol. Default: ₹
            base_currency_formal_name (str, optional): Base currency formal name. Default: Indian Rupees
            enable_bill_wise (bool, optional): Enable bill-wise details. Default: True
            enable_cost_centers (bool, optional): Enable cost centers. Default: False
            enable_inventory (bool, optional): Enable inventory. Default: True
            
        Returns:
            str: XML response confirming creation
        """
        # Set default mailing name if not provided
        if not mailing_name:
            mailing_name = company_name
            
        # Process optional address list
        address_element = ""
        if address_list and isinstance(address_list, list):
            address_lines = ""
            for addr in address_list:
                address_lines += f"<ADDRESS>{addr}</ADDRESS>\n"
            # Note: Tally often expects ADDRESS.LIST within the COMPANY tag directly
            address_element = f"""<ADDRESS.LIST TYPE="String">
                {address_lines}
            </ADDRESS.LIST>"""
            
        # Process other optional elements
        state_element = f"<STATENAME>{state}</STATENAME>" if state else "" # Changed tag to STATENAME
        pincode_element = f"<PINCODE>{pincode}</PINCODE>" if pincode else ""
        country_element = f"<COUNTRYNAME>{country}</COUNTRYNAME>" if country else "" # Changed tag to COUNTRYNAME
        email_element = f"<EMAIL>{email}</EMAIL>" if email else ""
        
        # Convert boolean settings to Yes/No
        bill_wise_value = "Yes" if enable_bill_wise else "No"
        cost_centers_value = "Yes" if enable_cost_centers else "No"
        inventory_value = "Yes" if enable_inventory else "No"
        
        # XML structure based on Postman collection hints and common practices
        # Using STARTINGFROM for Financial Year and BOOKSFROM for Books Beginning
        # Using YYYYMMDD date format
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>All Masters</REPORTNAME>
                 <STATICVARIABLES>
                    
                 </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <COMPANY Action="Create">
                        <NAME>{company_name}</NAME>
                        <MAILINGNAME>{mailing_name}</MAILINGNAME>
                        {address_element}
                        {state_element}
                        {pincode_element}
                        {country_element}
                        {email_element}
                        <STARTINGFROM>{financial_year_from}</STARTINGFROM>
                        <BOOKSFROM>{books_from}</BOOKSFROM>
                        <BASECURRENCYSYMBOL>{base_currency_symbol}</BASECURRENCYSYMBOL>
                        <FORMALNAME>{base_currency_formal_name}</FORMALNAME> 
                        <ISBILLWISEON>{bill_wise_value}</ISBILLWISEON>
                        <ISCOSTCENTRESON>{cost_centers_value}</ISCOSTCENTRESON>
                        <ISINVENTORYON>{inventory_value}</ISINVENTORYON>
                    </COMPANY>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    def configure_company(self, company_name, enable_inventory=None, enable_bill_wise=None, 
                         enable_cost_centers=None, enable_interest_calc=None):
        """
        Configure company features (F11 settings) in Tally
        
        Args:
            company_name (str): Name of the company
            enable_inventory (bool, optional): Enable inventory. Default: None (no change)
            enable_bill_wise (bool, optional): Enable bill-wise details. Default: None (no change)
            enable_cost_centers (bool, optional): Enable cost centers. Default: None (no change)
            enable_interest_calc (bool, optional): Enable interest calculation. Default: None (no change)
            
        Returns:
            str: XML response confirming update
        """
        # Build feature elements based on provided parameters
        features = []
        
        if enable_inventory is not None:
            inventory_value = "Yes" if enable_inventory else "No"
            features.append(f"<ISINVENTORYENABLED>{inventory_value}</ISINVENTORYENABLED>")
            
        if enable_bill_wise is not None:
            bill_wise_value = "Yes" if enable_bill_wise else "No"
            features.append(f"<ISBILLWISEON>{bill_wise_value}</ISBILLWISEON>")
            
        if enable_cost_centers is not None:
            cost_centers_value = "Yes" if enable_cost_centers else "No"
            features.append(f"<ISCOSTCENTRESON>{cost_centers_value}</ISCOSTCENTRESON>")
            
        if enable_interest_calc is not None:
            interest_value = "Yes" if enable_interest_calc else "No"
            features.append(f"<ISINTERESTON>{interest_value}</ISINTERESTON>")
            
        # If no features were specified, return early
        if not features:
            return "Error: No configuration parameters specified"
            
        features_xml = "\n".join(features)
        
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>All Masters</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <COMPANY NAME="{company_name}" ACTION="Alter">
                        {features_xml}
                    </COMPANY>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    def enable_gst(self, company_name, state_name, gst_registration_type="Regular", 
                  gstin=None, applicable_from="20250401"):
        """
        Enable GST for a company in Tally
        
        Args:
            company_name (str): Name of the company
            state_name (str): State name
            gst_registration_type (str, optional): GST registration type. Default: Regular
            gstin (str, optional): GST Identification Number. Default: None
            applicable_from (str, optional): GST applicable from date (format: YYYYMMDD). Default: 20250401
            
        Returns:
            str: XML response confirming update
        """
        # GSTIN is required for Regular registration
        if gst_registration_type == "Regular" and not gstin:
            return "Error: GSTIN is required for Regular GST registration type"
            
        gstin_element = f"<GSTIN>{gstin}</GSTIN>" if gstin else ""
        
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>All Masters</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <COMPANY NAME="{company_name}" ACTION="Alter">
                        <ISGSTENABLED>Yes</ISGSTENABLED>
                        <STATENAME>{state_name}</STATENAME>
                        <GSTREGISTRATIONTYPE>{gst_registration_type}</GSTREGISTRATIONTYPE>
                        {gstin_element}
                        <APPLICABLEFROMGST>{applicable_from}</APPLICABLEFROMGST>
                        <SETALTERGSTDETAILS>Yes</SETALTERGSTDETAILS>
                        <HASSLABRATE>No</HASSLABRATE>
                        <HASLUTBOND>No</HASLUTBOND>
                    </COMPANY>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    # -------------------- Entity Management --------------------

    def delete_ledger(self, company_name, ledger_name):
        """
        Delete a ledger in Tally
        
        Args:
            company_name (str): Name of the company
            ledger_name (str): Name of the ledger to delete
            
        Returns:
            str: XML response confirming deletion
        """
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>All Masters</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <LEDGER NAME="{ledger_name}" ACTION="Delete">
                    </LEDGER>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    def delete_stock_item(self, company_name, stock_item_name):
        """
        Delete a stock item in Tally
        
        Args:
            company_name (str): Name of the company
            stock_item_name (str): Name of the stock item to delete
            
        Returns:
            str: XML response confirming deletion
        """
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>All Masters</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <STOCKITEM NAME="{stock_item_name}" ACTION="Delete">
                    </STOCKITEM>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    def update_unit(self, company_name, unit_name, decimal_places=None, gst_uqc_code=None):
        """
        Update a unit in Tally
        
        Args:
            company_name (str): Name of the company
            unit_name (str): Name of the unit to update
            decimal_places (int, optional): Number of decimal places. Default: None (no change)
            gst_uqc_code (str, optional): GST UQC code. Default: None (no change)
            
        Returns:
            str: XML response confirming update
        """
        # Build elements based on provided parameters
        elements = []
        
        if decimal_places is not None:
            elements.append(f"<DECIMALPLACES>{decimal_places}</DECIMALPLACES>")
            
        if gst_uqc_code is not None:
            elements.append(f"<ISGSTREPUOM>{gst_uqc_code}</ISGSTREPUOM>")
            
        # If no elements were specified, return early
        if not elements:
            return "Error: No update parameters specified"
            
        elements_xml = "\n".join(elements)
        
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>All Masters</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <UNIT NAME="{unit_name}" ACTION="Alter">
                        {elements_xml}
                    </UNIT>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    def delete_unit(self, company_name, unit_name):
        """
        Delete a unit in Tally
        
        Args:
            company_name (str): Name of the company
            unit_name (str): Name of the unit to delete
            
        Returns:
            str: XML response confirming deletion
        """
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>All Masters</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <UNIT NAME="{unit_name}" ACTION="Delete">
                    </UNIT>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    # -------------------- Voucher Management --------------------

    def create_journal_voucher(self, company_name, entries, date=None, voucher_number=None, 
                              narration=""):
        """
        Create a journal voucher in Tally
        
        Args:
            company_name (str): Name of the company
            entries (list): List of dictionaries with keys:
                            - ledger_name (str): Name of the ledger
                            - is_debit (bool): True for debit, False for credit
                            - amount (float): Amount (positive value)
            date (str, optional): Voucher date in format YYYYMMDD. Default: Today
            voucher_number (str, optional): Voucher number. Default: None (auto-generated)
            narration (str, optional): Narration for the voucher. Default: ""
            
        Returns:
            str: XML response confirming creation
        """
        # Default to today's date if not provided
        if not date:
            from datetime import datetime
            date = datetime.now().strftime("%Y%m%d")
        
        # Optional voucher number
        voucher_number_element = f"<VOUCHERNUMBER>{voucher_number}</VOUCHERNUMBER>" if voucher_number else ""
        
        # Create ledger entries
        ledger_entries = []
        for entry in entries:
            # For journal entries, the sign of amount and is_deemed_positive need to be set correctly
            # For debit entries: is_deemed_positive=Yes, amount=-value
            # For credit entries: is_deemed_positive=No, amount=value
            is_deemed_positive = "Yes" if entry.get('is_debit', True) else "No"
            amount = float(entry.get('amount', 0))
            
            # Adjust sign based on is_debit
            amount_value = -amount if entry.get('is_debit', True) else amount
            
            ledger_entry = f"""<ALLLEDGERENTRIES.LIST>
                <LEDGERNAME>{entry.get('ledger_name', '')}</LEDGERNAME>
                <ISDEEMEDPOSITIVE>{is_deemed_positive}</ISDEEMEDPOSITIVE>
                <AMOUNT>{amount_value}</AMOUNT>
            </ALLLEDGERENTRIES.LIST>"""
            
            ledger_entries.append(ledger_entry)
        
        ledger_entries_xml = "\n".join(ledger_entries)
        
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>Vouchers</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <VOUCHER VCHTYPE="Journal" ACTION="Create">
                        <DATE>{date}</DATE>
                        <VOUCHERTYPENAME>Journal</VOUCHERTYPENAME>
                        {voucher_number_element}
                        <NARRATION>{narration}</NARRATION>
                        <PERSISTEDVIEW>Accounting Voucher View</PERSISTEDVIEW>
                        {ledger_entries_xml}
                    </VOUCHER>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    def update_voucher(self, company_name, master_id, narration=None, voucher_type=None):
        """
        Update a voucher in Tally using its master ID
        
        Args:
            company_name (str): Name of the company
            master_id (str): Master ID of the voucher
            narration (str, optional): New narration for the voucher. Default: None (no change)
            voucher_type (str, optional): Voucher type name. Default: None (no change)
            
        Returns:
            str: XML response confirming update
        """
        # Build elements based on provided parameters
        elements = []
        
        if narration is not None:
            elements.append(f"<NARRATION>{narration}</NARRATION>")
            
        if voucher_type is not None:
            elements.append(f"<VOUCHERTYPENAME>{voucher_type}</VOUCHERTYPENAME>")
            
        # If no elements were specified, return early
        if not elements:
            return "Error: No update parameters specified"
            
        elements_xml = "\n".join(elements)
        
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>Vouchers</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <VOUCHER ACTION="Alter">
                        <MASTERID>{master_id}</MASTERID>
                        {elements_xml}
                    </VOUCHER>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    def cancel_voucher(self, company_name, master_id):
        """
        Cancel a voucher in Tally using its master ID
        
        Args:
            company_name (str): Name of the company
            master_id (str): Master ID of the voucher
            
        Returns:
            str: XML response confirming cancellation
        """
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>Vouchers</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <VOUCHER ACTION="Cancel">
                        <MASTERID>{master_id}</MASTERID>
                    </VOUCHER>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    # -------------------- Group Management --------------------

    def create_group(self, company_name, group_name, parent_group, 
                    enable_bill_wise=None, is_addable=True):
        """
        Create a new group in Tally
        
        Args:
            company_name (str): Name of the company
            group_name (str): Name of the group
            parent_group (str): Parent group name
            enable_bill_wise (bool, optional): Enable bill-wise details. Default: None (inherit from parent)
            is_addable (bool, optional): Allow direct entries to this group. Default: True
            
        Returns:
            str: XML response confirming creation
        """
        # Build optional elements
        bill_wise_element = ""
        if enable_bill_wise is not None:
            bill_wise_value = "Yes" if enable_bill_wise else "No"
            bill_wise_element = f"<ISBILLWISEON>{bill_wise_value}</ISBILLWISEON>"
            
        is_addable_value = "Yes" if is_addable else "No"
        
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>All Masters</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <GROUP NAME="{group_name}" ACTION="Create">
                        <PARENT>{parent_group}</PARENT>
                        {bill_wise_element}
                        <ISADDABLE>{is_addable_value}</ISADDABLE>
                    </GROUP>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    def update_group(self, company_name, group_name, parent_group=None, 
                    enable_bill_wise=None, is_addable=None):
        """
        Update a group in Tally
        
        Args:
            company_name (str): Name of the company
            group_name (str): Name of the group to update
            parent_group (str, optional): New parent group name. Default: None (no change)
            enable_bill_wise (bool, optional): Enable bill-wise details. Default: None (no change)
            is_addable (bool, optional): Allow direct entries to this group. Default: None (no change)
            
        Returns:
            str: XML response confirming update
        """
        # Build elements based on provided parameters
        elements = []
        
        if parent_group is not None:
            elements.append(f"<PARENT>{parent_group}</PARENT>")
            
        if enable_bill_wise is not None:
            bill_wise_value = "Yes" if enable_bill_wise else "No"
            elements.append(f"<ISBILLWISEON>{bill_wise_value}</ISBILLWISEON>")
            
        if is_addable is not None:
            is_addable_value = "Yes" if is_addable else "No"
            elements.append(f"<ISADDABLE>{is_addable_value}</ISADDABLE>")
            
        # If no elements were specified, return early
        if not elements:
            return "Error: No update parameters specified"
            
        elements_xml = "\n".join(elements)
        
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>All Masters</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <GROUP NAME="{group_name}" ACTION="Alter">
                        {elements_xml}
                    </GROUP>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    def delete_group(self, company_name, group_name):
        """
        Delete a group in Tally
        
        Args:
            company_name (str): Name of the company
            group_name (str): Name of the group to delete
            
        Returns:
            str: XML response confirming deletion
        """
        xml_request = f"""<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <IMPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>All Masters</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
                <TALLYMESSAGE xmlns:UDF="TallyUDF">
                    <GROUP NAME="{group_name}" ACTION="Delete">
                    </GROUP>
                </TALLYMESSAGE>
            </REQUESTDATA>
        </IMPORTDATA>
    </BODY>
</ENVELOPE>"""
        
        return self._send_request(xml_request)

    def list_tally_companies(self):
        """
        Retrieves a list of all companies loaded in Tally using the requests library.
        Exports the predefined collection 'List of Companies'. Requires a company to be selected first.

        Args:
            tally_url (str): The URL of the Tally XML RPC server.

        Returns:
            list: A list of company names, or an empty list if unable to connect/find.
            None: Returns None if a significant error occurs.
        """
        tally_url = self.endpoint
        logging.info("Attempting to list all companies via Collection export...")
        headers = {'Content-Type': 'application/xml'}
        request_xml = """
        <ENVELOPE>
            <HEADER>
                <VERSION>1</VERSION>
                <TALLYREQUEST>Export</TALLYREQUEST>
                <TYPE>Collection</TYPE>
                <ID>List of Companies</ID>
            </HEADER>
            <BODY>
                <DESC>
                    <STATICVARIABLES>
                        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                    </STATICVARIABLES>
                    <FETCHLIST>
                    <FETCH>Name</FETCH>
                    </FETCHLIST>
                </DESC>
            </BODY>
        </ENVELOPE>
        """

        try:
            response = requests.post(tally_url, data=request_xml.encode('utf-8'), headers=headers, timeout=20)
            response_xml = response.text
            logging.debug(f"List Companies Raw Response:\n{response_xml}") # Log raw response at debug level

            if not response_xml or not response_xml.strip().startswith('<ENVELOPE>'):
                logging.warning(f"Received unexpected response format listing companies: {response_xml[:100]}...")
                return None

            companies = []
            try:
                root = ET.fromstring(response_xml)

                status = root.findtext('.//HEADER/STATUS')
                if status and status.strip() != '1':
                    error_nodes = root.findall('.//BODY/DATA/LINEERROR')
                    if error_nodes:
                        errors = ", ".join([err.text.strip() for err in error_nodes if err.text])
                        logging.error(f"Tally reported errors listing companies: {errors}")
                    else:
                        logging.error(f"Tally returned status {status} listing companies. Response: {response_xml[:200]}...")
                    return None

                # Expecting <COLLECTION><COMPANY><NAME>...</NAME></COMPANY>...</COLLECTION>
                name_elements = root.findall('.//COLLECTION/COMPANY/NAME')
                if not name_elements:
                    # Fallback check for simpler structure just in case
                    name_elements = root.findall('.//NAME')

                for name_element in name_elements:
                    if name_element.text:
                        companies.append(name_element.text.strip())

                companies = sorted(list(set(companies)))
                logging.info(f"Successfully listed companies: {companies}")
                return companies

            except ET.ParseError as e:
                logging.error(f"Error parsing Tally XML response for list companies: {e}")
                logging.error(f"Received Content Snippet:\n{response_xml[:500]}...")
                return None
            except Exception as e:
                logging.exception("Unexpected error during XML processing for list companies.") # Log full traceback
                return None

        except requests.exceptions.ConnectionError:
            logging.error(f"Connection refused. Is Tally running/configured on {tally_url}?")
            return None
        except requests.exceptions.Timeout:
            logging.error(f"Request timed out connecting to Tally on {tally_url}.")
            return None
        except requests.exceptions.RequestException as e:
            error_detail = ""
            if e.response is not None:
                error_detail = f" HTTP Status: {e.response.status_code}. Response: {e.response.text[:200]}..."
            logging.error(f"Request exception listing companies: {e}{error_detail}")
            return None
        except Exception as e:
            logging.exception("Unexpected error occurred while listing companies.") # Log full traceback
            return None
    def select_tally_company(self, company_name):
        """
        Selects a specific company in Tally using the requests library.
        Uses the Export/Data method with SVCURRENTCOMPANY, expecting an empty ENVELOPE on success.

        Args:
            company_name (str): The exact name of the company to select.
            tally_url (str): The URL of the Tally XML RPC server.

        Returns:
            bool: True if the company was selected successfully (or assumed based on response), False otherwise.
        """
        tally_url = self.endpoint
        logging.info(f"Attempting to select company: '{company_name}'")
        headers = {'Content-Type': 'application/xml'}
        request_xml = f"""
        <ENVELOPE>
            <HEADER>
                <VERSION>1</VERSION>
                <TALLYREQUEST>Export</TALLYREQUEST>
                <TYPE>Data</TYPE>
                <ID>Trial Balance</ID>
            </HEADER>
            <BODY>
                <DESC>
                    <STATICVARIABLES>
                        <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
                        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                    </STATICVARIABLES>
                </DESC>
            </BODY>
        </ENVELOPE>
        """

        try:
            response = requests.post(tally_url, data=request_xml.encode('utf-8'), headers=headers, timeout=25)
            response_xml = response.text
            logging.debug(f"Select Company '{company_name}' Raw Response:\n{response_xml}") # Log raw response

            # Check 1: Empty Envelope means success for this specific method
            if response_xml.strip() == "<ENVELOPE></ENVELOPE>":
                logging.info(f"Received empty ENVELOPE selecting '{company_name}'. Assuming success.")
                return True

            # Check 2: Any other response format suggests failure
            logging.warning(f"Did not receive expected empty ENVELOPE for select company '{company_name}'. Response: {response_xml[:200]}...")

            # Optional: Try parsing to log specific errors if present
            try:
                root = ET.fromstring(response_xml)
                status = root.findtext('.//HEADER/STATUS')
                errors = root.findall('.//BODY/DATA/LINEERROR')
                error_text = ", ".join([e.text.strip() for e in errors if e.text])
                logging.warning(f"Select company '{company_name}' failed. Status: {status}. Errors: {error_text}")
            except ET.ParseError:
                logging.warning(f"Select company '{company_name}' failed. Response was not valid XML.")
            except Exception as parse_e:
                logging.warning(f"Select company '{company_name}' failed. Error processing unexpected response: {parse_e}")

            return False # Explicitly return False if empty envelope wasn't received

        except requests.exceptions.ConnectionError:
            logging.error(f"Connection refused selecting '{company_name}'. Is Tally running/configured on {tally_url}?")
            return False
        except requests.exceptions.Timeout:
            logging.error(f"Request timed out selecting '{company_name}' on {tally_url}.")
            return False
        except requests.exceptions.RequestException as e:
            error_detail = ""
            if e.response is not None:
                error_detail = f" HTTP Status: {e.response.status_code}. Response: {e.response.text[:200]}..."
            logging.error(f"Request exception selecting company '{company_name}': {e}{error_detail}")
            return False
        except Exception as e:
            logging.exception(f"Unexpected error occurred while selecting company '{company_name}'.") # Log full traceback
            return False

# Example usage:
if __name__ == "__main__":
    # Create Tally client
    tally = TallyClient()
    
    # Check if Tally is running
    if tally.test_connection():
        print("Connected to Tally")
        
        # Get current company
        current_company = tally.get_current_company()
        print(f"Current company: {current_company}")
        
        # Get list of companies
        companies = tally.get_companies_list()
        print(f"Companies: {companies}")
        
        # Get list of ledgers
        ledgers = tally.get_ledgers_list("ABC Company")
        print(f"Ledgers: {ledgers}")
    else:
        print("Failed to connect to Tally")