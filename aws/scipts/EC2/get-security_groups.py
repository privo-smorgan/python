import boto3
import json
import os
from datetime import date
import csv

ec2 = boto3.resource('ec2')

for security_group in ec2.SecurityGroup.all():
    print(security_group)