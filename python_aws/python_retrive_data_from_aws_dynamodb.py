#client = boto3.client('dynamodb',aws_access_key_id='yyyy', aws_secret_access_key='xxxx', region_name='***')


from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
#Asia Pacific (Sydney)	ap-southeast-2	rds.ap-southeast-2.amazonaws.com	HTTPS
dynamodb = boto3.resource('dynamodb',aws_access_key_id='************', aws_secret_access_key='****/*****/*G****c**Q#', region_name='ap-southeast-2')
print(dynamodb)

table = dynamodb.Table('Orders')

print("Orders List")

OrderId = 'OrderId'
Address = 'Address'

try:
    response = table.get_item(
        Key={
            'OrderId': OrderId,
            'Address': Address
        }
    )
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("===")

    item = response['Item']
    print("GetItem succeeded:")
    print(json.dumps(item, indent=4, cls=DecimalEncoder))

print(response)
for i in response['Items']:
    print(i['year'], ":", i['title'])