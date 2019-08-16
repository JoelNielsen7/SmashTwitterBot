import requests
import json
import pprint
import time

api_token = 'eb81ad79e7fd95db2ede0470cac03757'
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

def get_active(slug):
    query_string = '''
    query TournamentQuery($slug: String)
    {tournament(slug: $slug){
    state
    name
    }
    }'''

    vars = {
    "slug": slug,
    }

    res = query(query_string, vars)
    return res['data']['tournament']['state'], res['data']['tournament']['name']

def get_tournament_by_id(id):
    query_string = '''
    query TournamentQuery($id: String)
    {tournament(id: $id){
    state
    name
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
    "id": id,
    }

    res = query(query_string, vars)
    return res

def get_tournament_by_name(name):
    query_string = '''
    query TournamentsByCountry($name: String!, $perPage: Int!) {
      tournaments(query: {
        perPage: $perPage
        filter: {
          name: $name
        }
      }) {
        nodes {
          id
          name
        }
      }
    }'''
    vars = {
      "name": name,
      "perPage": 500
    }
    res = query(query_string, vars)
    for result in res['data']['tournaments']['nodes']:
        print(result['name'])
        if result['name'].lower() == name.lower():
            return result['id']
    return None

def get_tournament(slug, ultimate):
    game = ''
    if ultimate == False:
        game = "melee"
    else:
        game = "ultimate"
    #first try to find by slug
    query_string = '''
    query TournamentQuery($slug: String)
    {tournament(slug: $slug){
    state
    name
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
    }

    res = query(query_string, vars)
    if res['data']['tournament'] == None:
        id = get_tournament_by_name(slug)
        if id == None:
            print("Couldn't find tourney with that slug/name")
            return None, None, None
        else:
            res = get_tournament_by_id(id)
    melee_id = ''
    melee_name = ''
    top_8_id = 0
    for x in res['data']['tournament']['events']:
        if game in x['name'].lower():
            if melee_id == '':
                melee_id = x['id']
                melee_name = x['name']
                for phase in x['phases']:
                    if ('8' in phase['name'].lower() or 'eight' in phase['name'].lower() or 'finals' in phase['name'].lower() or 'final' in phase['name'].lower() or '16' in phase['name'].lower() or 'sixteen' in phase['name'].lower()):
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
    active = res['data']['tournament']['state']
    if melee_id == '':
        print("Couldn't locate melee top 8 for this event")
        return None, None, None
    return melee_id, top_8_id, active

def get_top_8(melee_id, top_8_id):
    event_query = '''
    query PhaseSets($phaseId: ID!, $page:Int!, $perPage:Int!){
    phase(id:$phaseId){
        id
        name
        sets(
          page: $page
          perPage: $perPage
          sortType: STANDARD
        ){
          pageInfo{
            total
          }
          nodes{
            winnerId
            round
            fullRoundText
            completedAt
            id
            entrant1Score
            entrant2Score
            games{
                winnerId
            }
            slots{
              id
              standing{
                placement
              }
              entrant{
                id
                name
              }
            }
          }
        }
      }
    }'''

    event_vars = {
    'phaseId': top_8_id,
    'page': '1',
    'perPage':'100'
    }

    res = query(event_query, event_vars)
    # pp.pprint(res)
    return res

if __name__ == '__main__':
    melee_id, top_8_id, state = get_tournament('super-smash-con-2019', False)
    print(state)
    # pp.pprint(get_top_8(melee_id, top_8_id))
    # print(get_tournament('super-smash-con-2019', False))
    # print(get_tournament_by_name('Evo 2018'))
    # print(get_tournament('evo-2019', True))
    # get_tournament('evo-2019', True)
# get_tournament('evo-2018')
