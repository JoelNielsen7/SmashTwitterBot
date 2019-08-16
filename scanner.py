import json
import graphql_queries
import boto3
from boto3.dynamodb.conditions import Key, Attr
import tweet
import parser
import pprint
pp = pprint.PrettyPrinter(indent=2)

def format_tweet(tuple, tourney):
    tweet = '''{} has defeated {} {} in {} of {}'''.format(tuple[0], tuple[1], tuple[2], tuple[3], tourney)
    return tweet

def lambda_handler(event, context):
    # pull all active rows from db
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('melee_results')

    res = table.scan(
    FilterExpression=Attr('active').eq('Y')
    )

    pp.pprint(res)

    for tourney in res['Items']:
        event_id = str(tourney['event_id'])
        top_8_id = str(tourney['top_8_id'])
        active, name = graphql_queries.get_active(tourney['slug'])
        print("Active:", active)
        active_letter = 'Y'
        if active == 2:
            active_letter = 'N'
        res = graphql_queries.get_top_8(event_id, top_8_id)
        #retrieve curernt top 8 and check for differences
        item = res['data']['phase']

        differences = parser.find_differences(tourney, item)
        #if different send tweet and update db
        for diff in differences:
            string = format_tweet(diff, name)
            print(string)
            tweet.tweet_library(string)

        if (len(differences) != 0) or (active_letter != tourney['active']):
            #delete and re-put item because I don't want to go through each field and find the differences
            dele = table.delete_item(
            Key={
                'slug': str(tourney['slug'])
            }
            )
            item['slug'] = tourney['slug']
            item['ultimate'] = tourney['ultimate']
            if active == 3:
                item['active'] = 'N'
            else:
                item['active'] = 'Y'
            item['event_id'] = event_id
            item['top_8_id'] = top_8_id
            res = table.put_item(
                Item=item
            )
            print(res)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


if __name__ == '__main__':
    lambda_handler(None, None)
