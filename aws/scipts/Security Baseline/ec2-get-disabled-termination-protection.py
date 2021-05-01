import boto3
import json

# This script gets the running instances with termination protection
# disabled.

# Set resource
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

# Get instances using filters for running
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

# Print instance information for EC2s with termination protection disabled
for instance in instances:
    response = client.describe_instance_attribute(
    Attribute='disableApiTermination',
    InstanceId=instance.id,
    )

    for key in response:
        if key == 'DisableApiTermination':
            if (response[key]['Value'] == False):
                print(json.dumps(response, sort_keys=True, indent=4, default=str))

