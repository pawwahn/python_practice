import boto3
ec2 = boto3.resource('ec2')

# create a new EC2 instance
instances = ec2.create_instances(
     ImageId='ami-0d2692b6acea72ee6',
     MinCount=1,
     MaxCount=1,
     InstanceType='t2.micro',
     KeyName='ec2-keypair.pem',
     Monitoring={'Enabled': False},
     #SubnetId='subnet-03bbc30da231194d4'

 )
#instances["VpcId"]='vpc-070739f5ac93079ed'