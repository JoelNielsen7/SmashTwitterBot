import json
import graphql_queries
import pprint
import boto3
import tweet

pp = pprint.PrettyPrinter(indent=2)

def lambda_handler(event, context):
    body = json.loads(event['body'])
    print(body)

    try:
        create_event = body['tweet_create_events'][0]
    except Exception as e:
        print(e)
        print("Not a create tweet event")
        return


    flag = False
    for user in create_event['entities']['user_mentions']:
        if user['screen_name'].lower() == 'melee_results':
            flag = True
    if flag == False:
        print("Didn't mention me")
        return
    if 'RT' in create_event['text']:
        print("RT event, skipping")
        return
    text = create_event['text']
    text = text.replace('@melee_results', '').strip()
    print(text)
    tweeter = create_event['user']['screen_name']

    ultimate = False
    ult = 'N'
    if 'ultimate' in text:
        ultimate = True
        ult = 'Y'
        text = text.replace('ultimate', '').strip()

    event_id, top_8_id, state = graphql_queries.get_tournament(text, ultimate)
    if event_id == None:
        tweet.tweet_library('Could not find a tournament with that slug/name. Please make sure your tournament slug is correct and try again', create_event['id_str'], tweeter)
        # tweet.slug_fail(create_event['id_str'], text)
        return
    if top_8_id == 0:
        tweet.tweet_library("I found the event for that tournament, but it looks like the brackets haven't been published yet. Try again a little closer to the event", create_event['id_str'], tweeter)
        return
    res = graphql_queries.get_top_8(event_id, top_8_id)
    # pp.pprint(res)
    # print(len(json.dumps(res)))

    #Insert into into db
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('melee_results')

    #try to get item to see if duplicate
    get_res = table.get_item(
    Key={
        'slug': text
    }
    )
    try:
        dup = get_res['Item']
        print(dup)
    except:
        item = res['data']['phase']
        item['slug'] = text
        item['ultimate'] = ult
        if state == 3:
            item['active'] = 'N'
        else:
            item['active'] = 'Y'
        item['event_id'] = event_id
        item['top_8_id'] = top_8_id
        table.put_item(
            Item=item
        )
    else:
        #tweet duplicate
        print("Entry already exists")
        tweet.tweet_library("I'm already watching that tournament.", create_event['id_str'], tweeter)
        return
    #Tweet success

    tweet.tweet_library('Success! The tournament: {} has been registered. Live updates of top 8 will be tweeted.'.format(text), create_event['id_str'], tweeter)
    print(body)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }



# raw = "{'body': {'for_user_id': '1149863023349288960', 'tweet_create_events': [{'created_at': 'Sun Aug 04 23:40:04 +0000 2019', 'id': 1158160704177942529, 'id_str': '1158160704177942529', 'text': '@melee_results super-smash-con-2019', 'source': '<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>', 'truncated': False, 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': 1149863023349288960, 'in_reply_to_user_id_str': '1149863023349288960', 'in_reply_to_screen_name': 'melee_results', 'user': {'id': 1158151931782729730, 'id_str': '1158151931782729730', 'name': 'test user', 'screen_name': 'testuse84017952', 'location': None, 'url': None, 'description': None, 'translator_type': 'none', 'protected': False, 'verified': False, 'followers_count': 0, 'friends_count': 0, 'listed_count': 0, 'favourites_count': 0, 'statuses_count': 1, 'created_at': 'Sun Aug 04 23:05:12 +0000 2019', 'utc_offset': None, 'time_zone': None, 'geo_enabled': False, 'lang': None, 'contributors_enabled': False, 'is_translator': False, 'profile_background_color': 'F5F8FA', 'profile_background_image_url': '', 'profile_background_image_url_https': '', 'profile_background_tile': False, 'profile_link_color': '1DA1F2', 'profile_sidebar_border_color': 'C0DEED', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 'profile_image_url': 'http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', 'profile_image_url_https': 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png', 'default_profile': True, 'default_profile_image': False, 'following': None, 'follow_request_sent': None, 'notifications': None}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'quote_count': 0, 'reply_count': 0, 'retweet_count': 0, 'favorite_count': 0, 'entities': {'hashtags': [], 'urls': [], 'user_mentions': [{'screen_name': 'melee_results', 'name': 'Smash Results Bot', 'id': 1149863023349288960, 'id_str': '1149863023349288960', 'indices': [0, 14]}], 'symbols': []}, 'favorited': False, 'retweeted': False, 'filter_level': 'low', 'lang': 'en', 'timestamp_ms': '1564962004118'}]}""
#
# if __name__ == '__main__':
#     lambda_handler(raw, None)
