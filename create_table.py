import boto3

#To be run manually for testing purposes
def dynamo():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('melee_results')
    print(table)
    print(table.creation_date_time)
    res = table.delete_item(
    Key={
        'slug': 'automation-test-tournament'
    }
    )
    print(res['Item'])

# create_table()
# dynamo()
