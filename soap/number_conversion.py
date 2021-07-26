from zeep import Client
client = Client(wsdl='http://www.dataaccess.com/webservicesserver/numberconversion.wso?WSDL')

res = client.service.NumberToDollars(20)
print(res)


