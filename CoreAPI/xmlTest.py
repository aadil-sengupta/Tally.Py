import requests

xml = """
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Execute</TALLYREQUEST>
        <TYPE>TDLFunction</TYPE>
        <ID>SimpleAdd</ID>
    </HEADER>
    <BODY>
        <DESC>
            <PARAM>10</PARAM>
            <PARAM>20</PARAM>
        </DESC>
    </BODY>
</ENVELOPE>
"""
url = "http://localhost:9000"

print(requests.post(url, data=xml).text)

