
import requests

url = "http://3.87.12.53:8181/pc/ws/gw/webservice/pc/pc1000/MaintenanceToolsAPI/soap11"
headers = {'Content-Type': 'text/xml'}
run_body = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://guidewire.com/ws/soapheaders" xmlns:main="http://guidewire.com/pc/ws/gw/webservice/pc/pc1000/MaintenanceToolsAPI">
   <soapenv:Header>
      <soap:traceability_id>?</soap:traceability_id>
      <soap:authentication>
         <soap:username>su</soap:username>
         <soap:password>gw</soap:password>
      </soap:authentication>
   </soapenv:Header>
   <soapenv:Body>
      <main:startBatchProcess>
         <!--Optional:-->
         <main:processName>MakeModelUpdate</main:processName>
      </main:startBatchProcess>
   </soapenv:Body>
</soapenv:Envelope>
"""
status_body = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://guidewire.com/ws/soapheaders" xmlns:main="http://guidewire.com/pc/ws/gw/webservice/pc/pc1000/MaintenanceToolsAPI">
   <soapenv:Header>
      <soap:traceability_id>?</soap:traceability_id>
      <soap:authentication>
         <soap:username>su</soap:username>
         <soap:password>gw</soap:password>
      </soap:authentication>
   </soapenv:Header>
   <soapenv:Body>
      <main:batchProcessStatusByName>
         <!--Optional:-->
         <main:processName>MakeModelUpdate</main:processName>
      </main:batchProcessStatusByName>
   </soapenv:Body>
</soapenv:Envelope>"""
response = requests.post(url, data=run_body, headers=headers)
print(response.content)
import xmltodict,json

resp = xmltodict.parse(response.content)
pid = resp['tns:Envelope']['tns:Body']['startBatchProcessResponse']['return']['pogo:Pid']
print (pid)
response = requests.post(url, data=status_body, headers=headers)
resp = xmltodict.parse(response.content)
print(resp)
completed = resp['tns:Envelope']['tns:Body']['batchProcessStatusByNameResponse']['return']['pogo:Complete']
executing = resp['tns:Envelope']['tns:Body']['batchProcessStatusByNameResponse']['return']['pogo:Executing']
success = resp['tns:Envelope']['tns:Body']['batchProcessStatusByNameResponse']['return']['pogo:Success']
failedOps = resp['tns:Envelope']['tns:Body']['batchProcessStatusByNameResponse']['return']['pogo:FailedOps']
starting = resp['tns:Envelope']['tns:Body']['batchProcessStatusByNameResponse']['return']['pogo:Starting']
opsCompleted = resp['tns:Envelope']['tns:Body']['batchProcessStatusByNameResponse']['return']['pogo:OpsCompleted']
startingOrExecuting = resp['tns:Envelope']['tns:Body']['batchProcessStatusByNameResponse']['return'][
    'pogo:StartingOrExecuting']
pogo = resp['tns:Envelope']['tns:Body']['batchProcessStatusByNameResponse']['return']['@xmlns:pogo']
pogoType = resp['tns:Envelope']['tns:Body']['batchProcessStatusByNameResponse']['return']['pogo:Type']
if startingOrExecuting == 'true':
    # check after some time
    print
    'check for the status after some time'
elif completed == 'true' and (success == 'true' or failedOps == '0'):
    # stop check ing the status for the pid
    print('stop checking the status for the pid')
elif completed == 'true' and (success == 'false' or failedOps == '1'):
    # screate service now ticket
    print('create service now ticket', pogo, pogoType)

