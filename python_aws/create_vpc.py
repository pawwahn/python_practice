import boto3
ec2 = boto3.resource('ec2')

#create vpc
vpc = ec2.create_vpc(
        CidrBlock='172.16.0.0/16')

#Assign name to your VPC
vpc.create_tags(Tags=[{"Key": "Name", "Value":"my_vpcs"}])
vpc.wait_until_available()

# enable public dns hostname so that we can SSH into it later
ec2Client = boto3.client('ec2')
ec2Client.modify_vpc_attribute(VpcId = vpc.id, EnableDnsSupport = {'Value': True})
ec2Client.modify_vpc_attribute(VpcId = vpc.id, EnableDnsHostnames = {'Value': True})

# create an internet gateway # attach it to VPC
internetgateway = ec2.create_internet_gateway()
internetgateway.create_tags(Tags=[{"Key": "Name", "Value":"myIG1"}])

# attach internet gateway to VPC
vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)

# create a route table and a public route
routetable = vpc.create_route_table()
routetable.create_tags(Tags=[{"Key": "Name", "Value":"public_route_table1"}])
route = routetable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetgateway.id)

# create subnet
subnet1 = ec2.create_subnet(CidrBlock='172.16.1.0/24', VpcId=vpc.id, AvailabilityZone= 'ap-south-1a',)
subnet1.create_tags(Tags=[{"Key": "Name", "Value":"public_subnet"}])

# associate it with route table
routetable.associate_with_subnet(SubnetId=subnet1.id)

subnet2 = ec2.create_subnet(CidrBlock='172.16.2.0/24', VpcId=vpc.id, AvailabilityZone= 'ap-south-1b',)
subnet2.create_tags(Tags=[{"Key": "Name", "Value":"private_subnet"}])


# Create a security group and allow SSH inbound rule through the VPC
securitygroup = ec2.create_security_group(GroupName='SSH-ONLY', Description='only allow SSH traffic', VpcId=vpc.id)
securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)




