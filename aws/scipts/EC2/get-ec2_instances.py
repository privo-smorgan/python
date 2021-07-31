import boto3
import json
import os
from datetime import date
import csv

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
security_group = ec2.SecurityGroup('id')
today = date.today()
date_var = today.strftime("%b-%d-%Y")
output_file = 'output-ec2_security_groups-'+ date_var +'.csv'
if os.path.isfile(output_file):
    print('Output file exists!')
else:
    f = open(output_file, "w")
    f.close()


#instances = ec2.instances()
with open(output_file, 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['InstanceId', 'InstanceName', 'InstanceState', 'SecurityGroup', 'SecurityGroupId', 'SecurityGroupIPPermissions'])

    for instance in ec2.instances.all():
        response = client.describe_instances(
            InstanceIds = [instance.id]
        )
        inst_state = instance.state
        inst_sg = instance.security_groups
        inst_tags = instance.tags
        for tag in inst_tags:
            if tag['Key'] == 'Name':
                inst_name = tag['Value']
        security_group = ec2.SecurityGroup(
            inst_sg[0]['GroupId']
            )    
        
        #print(security_group.group_name, security_group.ip_permissions, security_group.owner_id)    
        filewriter.writerow(
            [instance.id,
            inst_name,
            inst_state['Name'],
            security_group.group_name,
            inst_sg[0]['GroupId'],
            security_group.ip_permissions]
            )
        
    #print(instance.id, instance.state, instance.security_groups)
