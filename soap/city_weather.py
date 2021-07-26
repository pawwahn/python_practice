from zeep import Client
from requests import Session
from zeep.transports import Transport

session = Session()
session.verify = False
client = Client(wsdl='http://wsf.cdyne.com/weatherws/weather.asmx?wsdl')



# In terminal use, $> python -mzeep wsdl-url