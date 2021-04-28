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

# Get rules with non-compliant resources
noncompliant_rules = []
for rule in rules:
    response1 = client.get_compliance_details_by_config_rule(
        ConfigRuleName = rule
    )
    for key1 in response1['EvaluationResults']:
        if key1['ComplianceType'] == 'NON_COMPLIANT':
            #print(key['EvaluationResultIdentifier']['EvaluationResultQualifier']['ConfigRuleName'])
            if key1['EvaluationResultIdentifier']['EvaluationResultQualifier']['ConfigRuleName'] not in noncompliant_rules:
                noncompliant_rules.append(key1['EvaluationResultIdentifier']['EvaluationResultQualifier']['ConfigRuleName'])

# Write data to CSV file
with open(output_file, 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['ConfigRuleName', 'ResourceId', 'ResourceType'])
    for ncr in noncompliant_rules:
        response2 = client.get_compliance_details_by_config_rule(
            ConfigRuleName = ncr
        )
        # TODO: Validate data - Should be over 60 rows 
        for key2 in response2['EvaluationResults']:
            filewriter.writerow([key2['EvaluationResultIdentifier']['EvaluationResultQualifier']['ConfigRuleName'],
            key2['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceId'],
            key2['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceType']]
            )
