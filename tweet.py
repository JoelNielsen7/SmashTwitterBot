import os
import json
import requests
import twitter

def tweet_library(message, reply = None, tweeter = None):
    api = twitter.Api(consumer_key='oOkLIKSCZMNjiZeF7gVTQQNNE',
                      consumer_secret='Su7dfAiQyIbgOKFGilanaxkzha5aMwERsAtSPaoz9Lrchp2uJj',
                      access_token_key='1149863023349288960-ISG9TdC9LoBtmvww0ibU3lFu3dvQ2G',
                      access_token_secret='zyM2NUOu8PDwDOt6Izi01N2tZ7h2JGmf9y4SxIMpd98Xc')
    if reply == None:
        res = api.PostUpdate(message)
    else:
        message = "@{}".format(tweeter) + ' ' +  message
        print("Replying")
        res = api.PostUpdate(message, in_reply_to_status_id=reply)
    print(res)


def tweet(message):
    shell_string = "twurl -d 'status={}' /1.1/statuses/update.json".format(message)
    # shell_string = "twurl -d '{}' /1.1/statuses/update.json".format(payload)
    os.system(shell_string)

def reply(message, id):
    shell_string = "twurl -d 'status={}' -d 'in_reply_to_status_id={}' /1.1/statuses/update.json".format(message, id)
    os.system(shell_string)

def get_mentions():
    shell_string = "twurl /1.1/statuses/mentions_timeline.json > tmp"
    os.system(shell_string)
    res = open('tmp', 'r').read()
    # print(json.loads(res))
    res = json.loads(res)
    for tweet in res:
        print(tweet['text'])
    return res

def get_my_tweets():
    shell_string = "twurl /1.1/statuses/home_timeline.json > tmp"
    os.system(shell_string)
    res = open('tmp', 'r').read()
    # print(json.loads(res))
    res = json.loads(res)
    for tweet in res:
        print(tweet['text'])
    return res

def auto_reply():
    mentions = get_mentions()
    for tweet in mentions[0:1]:
        id = tweet['id']
        reply('@melee_results auto-reply', id)

def slug_fail(id, text):
    tweet_library('Could not find a tournament with the slug/name: {}. Please make sure your tournament slug is correct and try again'.format(text), id)

def register_success(id, text):
    tweet_library('Success! The tournament: {} has been registered. Live updates of top 8 will be tweeted.'.format(text), id)
# tweet('json')
# get_mentions()
# get_my_tweets()
# auto_reply()
if __name__ == '__main__':
    # tweet_library("Test reply", '1158165932520419334', 'testuse84017952')
    string = 'Test'
    tweet_library(string)
    # reply("Test reply", 1158160704177942529)
