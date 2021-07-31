import boto3
import csv
import json

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
# security_group = ec2.SecurityGroup('id')

data = []

with open('file.csv', newline='') as f:
    for row in csv.reader(f):
        data.append(row[0])

for sg in data:
    response = client.describe_security_groups(
        GroupNames=[
            sg,
        ]
    )
    print(json.dumps(response, sort_keys=True, indent=4, default=str))

#print(data)