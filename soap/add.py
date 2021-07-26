from zeep import Client
client = Client(wsdl='http://www.dneonline.com/calculator.asmx?wsdl')
res = client.service.Add(3,4)

# client = Client(wsdl='https://www.w3schools.com/XML/tempconvert.asmx?WSDL')
# #client.service.ping()
# res = client.service.CelsiusToFahrenheit('98.6')


# client = Client(wsdl='http://wl-osbdev-middle:8011/IdentityVericationService/proxy/GenericToValidationProxy?wsdl')

print(res)
