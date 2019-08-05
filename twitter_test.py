import requests
import graphene
import json
import pprint
import time
import graphql_queries
from top8 import Top8
api_token = 'eb81ad79e7fd95db2ede0470cac03757'

twitter_url = 'https://api.twitter.com/1.1/statuses/update.json'
smash_url = 'https://api.smash.gg/gql/alpha'

pp = pprint.PrettyPrinter(indent=2)

def query(query_string, variables=None):
    headers = {
    'Authorization': 'Bearer' + api_token,
    'Content-type': 'application/json'
    }

    post_data = {
    'query': query_string,
    'variables': variables
    }

    try:
        r = requests.post(smash_url, headers=headers, data=json.dumps(post_data))
    except:
        print(r.status_code, r.content)
    return r.json()

def get_idssss_bad(slug):
    query_string = '''
    query TournamentQuery($slug: String, $page: Int!, $perPage: Int!)
    {tournament(slug: $slug){
            events {
              name
              standings(query: {
                page: $page
                perPage: $perPage
              }){
                nodes{
                  standing
                  entrant{
                    name
                  }
                }
              }
            }
        }
    }'''

    vars = {
    "slug": slug,
    "page": 1,
    "perPage": 3,
    }


    res = query(query_string, vars)
    pp.pprint(res)

def get_ids(slug):
    query_string = '''
    query TournamentQuery($slug: String)
    {tournament(slug: $slug){
    events{
        name
        id
        phases{
        id
        name
        }
        }
    }
    }'''

    vars = {
    "slug": slug,
    # "slug": "evo-2017"
    }

    res = query(query_string, vars)
    melee_id = ''
    melee_name = ''
    top_8_id = 0
    for x in res['data']['tournament']['events']:
        if 'melee' in x['name'].lower():
            if melee_id == '':
                melee_id = x['id']
                melee_name = x['name']
                for phase in x['phases']:
                    if ('8' in phase['name'].lower() or 'eight' in phase['name'].lower() or 'finals' in phase['name'].lower() or 'final' in phase['name'].lower()):
                        top_8_id = phase['id']
            else:
                if ('1' in x['name'].lower() or 'one' in x['name'].lower() or 'singles' in x['name'].lower()):
                    melee_id = x['id']
                    melee_name = x['name']
                    for phase in x['phases']:
                        if ('8' in phase['name'].lower() or 'eight' in phase['name'].lower() or 'finals' in phase['name'].lower() or 'final' in phase['name'].lower()):
                            top_8_id = phase['id']

    pp.pprint(res)
    print(melee_id)
    print(top_8_id)
    return melee_id, top_8_id


# def get_top_8(melee_id, top_8_id):
#     event_query = '''
#     query PhaseSets($phaseId: ID!, $page:Int!, $perPage:Int!){
#     phase(id:$phaseId){
#         id
#         name
#         sets(
#           page: $page
#           perPage: $perPage
#           sortType: STANDARD
#         ){
#           pageInfo{
#             total
#           }
#           nodes{
#             winnerId
#             round
#             fullRoundText
#             completedAt
#             id
#             games{
#                 winnerId
#             }
#             slots{
#               id
#               standing{
#                 placement
#               }
#               entrant{
#                 id
#                 name
#               }
#             }
#           }
#         }
#       }
#     }'''
#
#     event_vars = {
#     'phaseId': top_8_id,
#     'page': '1',
#     'perPage':'100'
#     }
#
#     res = query(event_query, event_vars)
#     # pp.pprint(res)
#     return res

def find_changes(new_top8, old_top8):
    x=0

def main(slug):
    melee_id, top_8_id = get_ids(slug)
    past_top = {}
    top = {}
    top8_class = None
    x=0
    while(x < 2):
        past_top = top
        top = get_top_8(melee_id, top_8_id)
        if past_top != top:
            top8_class = Top8(top)
            print(top8_class)
            top8_class_past = Top8(past_top)
            print("Top 8 changed")
            diff = top8_class.compare(top8_class_past)
            print(diff)
        else:
            print("Top 8 did not change")
        time.sleep(10)
        x += 1


if __name__ == '__main__':
    slug = 'automation-test-tournament'
    slug = 'evo-2018'
    melee_id, top_8_id = graphql_queries.get_tournament(slug, False)
    print(melee_id)
    res = graphql_queries.get_top_8(melee_id, top_8_id)
    pp.pprint(res)
    # main('low-tier-city-7')
    # main('?evo-2018')
