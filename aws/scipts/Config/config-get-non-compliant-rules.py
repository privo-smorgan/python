'''
# List Rules
aws configservice describe-config-rules --query 'ConfigRules[].ConfigRuleName' > t
# From the rules file above, make a short CSV with the number of non-compliant resources.  We only care about > 0
for rule in $(cat t); do
    echo -n "$rule,"
    aws configservice get-compliance-details-by-config-rule \
        --config-rule-name "$rule" \
        --query 'EvaluationResults[?ComplianceType==`NON_COMPLIANT`]' | jq length
done
# Split the CSV, or grep off the ,0 entries
# Loop the the file with rules
for rule in $(cat t); do
    echo "Rule: $rule"
    aws configservice get-compliance-details-by-config-rule \
        --config-rule-name "$rule" \
        --query 'EvaluationResults[?ComplianceType==`NON_COMPLIANT`].EvaluationResultIdentifier.EvaluationResultQualifier' \
        --output text
done
'''
import boto3
import json
import os
from datetime import date
import csv

# Create output file
today = date.today()
date_var = today.strftime("%b-%d-%Y")
output_file = 'output-non_compliant_rules-'+ date_var +'.csv'
if os.path.isfile(output_file):
    print('Output file exists!')
else:
    f = open(output_file, "w")
    f.close()

client = boto3.client('config')

# Get AWS Config rule details
rules = []
response = client.describe_config_rules()
paginator = client.get_paginator('describe_config_rules')
response_iterator = paginator.paginate(
    PaginationConfig={
        'MaxItems' : 200
    }
)
for page in response_iterator:
    for key in page['ConfigRules']:
        rules.append(key['ConfigRuleName'])

# Get rules with non-compliant resources andwrite data to CSV file
with open(output_file, 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['ConfigRuleName', 'ResourceId', 'ResourceType'])
    paginator1 = client.get_paginator('get_compliance_details_by_config_rule')
    for rule in rules:
        response1 = paginator1.paginate(
            ConfigRuleName = rule,
            ComplianceTypes = ['NON_COMPLIANT'],
            PaginationConfig={
                'MaxItems' : 200
            }
        )
        for page1 in response1:
            for key1 in page1['EvaluationResults']:
                filewriter.writerow([key1['EvaluationResultIdentifier']['EvaluationResultQualifier']['ConfigRuleName'],
                key1['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceId'],
                key1['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceType']]
                )
