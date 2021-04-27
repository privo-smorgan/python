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
#for ncrule in noncompliant_rules:
    #print(ncrule)
#print(len(noncompliant_rules))
print('ConfigRuleName, ResourceId, ResourceType')
for ncr in noncompliant_rules:
    response2 = client.get_compliance_details_by_config_rule(
        ConfigRuleName = ncr
    )
    # TODO: Get ConfigRuleName, ResourceId, and ResourceType for each non-compliant rule
    # TODO: Validate data
    for key2 in response2['EvaluationResults']:
        print(key2['EvaluationResultIdentifier']['EvaluationResultQualifier']['ConfigRuleName']+','+
        key2['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceId']+','+
        key2['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceType']
        )
# TODO: Generate a CSV from above
# Create CSV output each