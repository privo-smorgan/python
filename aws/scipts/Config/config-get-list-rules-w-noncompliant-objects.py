import boto3

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