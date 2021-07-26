from zeep import Client

client = Client(wsdl='http://www.webservicex.com/CurrencyConvertor.asmx?wsdl')

res = client.service.NumberToDollars(40)
print(res)