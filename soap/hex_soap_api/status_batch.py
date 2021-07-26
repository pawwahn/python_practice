import requests
url="http://3.87.12.53:8181/pc/ws/gw/webservice/pc/pc1000/MaintenanceToolsAPI/soap11"
headers = {'Content-Type': 'text/xml'}
body = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://guidewire.com/ws/soapheaders" xmlns:main="http://guidewire.com/pc/ws/gw/webservice/pc/pc1000/MaintenanceToolsAPI">
   <soapenv:Header>
      <soap:traceability_id>?</soap:traceability_id>
      <soap:authentication>
         <soap:username>su</soap:username>
         <soap:password>gw</soap:password>
      </soap:authentication>
   </soapenv:Header>
   <soapenv:Body>noti
      <main:batchProcessStatusByName>
         <!--Optional:-->
         <main:processName>MakeModelUpdate</main:processName>
      </main:batchProcessStatusByName>
   </soapenv:Body>
</soapenv:Envelope>
"""
response = requests.post(url,data=body,headers=headers)
print (response.content)