import json
import pprint

pp = pprint.PrettyPrinter(indent=2)

round_dict = {
    'Grand Final Reset': 'Grand Finals Reset',
    'Grand Final': 'Grand Finals',
    'Winners Final':'Winners Finals',
    'Losers Final':'Losers Finals',
    'Losers Semi-Final':'Losers Semi-Finals',
    'Winners Semi-Final':'Winners Semi-Finals',
    'Losers Quarter-Final':'Losers Quarter-Finals',
    'Losers Round 1':'Losers Round 1'
}


def find_differences(old_data, new_data):
    old_sets = old_data['sets']['nodes']
    new_sets = new_data['sets']['nodes']
    pp.pprint(old_sets)
    pp.pprint(new_sets)
    changes = []
    #assumes that they will be in the same order.. could do O(n^2) iteration to not
    for new_set in new_sets:
        if 'preview' in str(new_set['id']):
            print("Bracket hasn't started yet")
            return []
        elif 'preview' in str(old_sets[0]['id']):
            #this means the bracket started since the last update
            if new_set['winnerId'] != None:
                print("Found a change after starting tourney")
                winnerId = new_set['winnerId']
                e1Score = new_set['entrant1Score']
                e2Score = new_set['entrant2Score']
                round = new_set['fullRoundText']
                round_good = round
                try:
                    round_good = round_dict[round]
                except:
                    rount_good = round
                if e1Score > e2Score:
                    count = '{}-{}'.format(e1Score, e2Score)
                else:
                    count = '{}-{}'.format(e2Score, e1Score)
                loser = ''
                for player in new_set['slots']:
                    if player['entrant']['id'] != winnerId:
                        loser = player['entrant']['name']
                    else:
                        winner = player['entrant']['name']
                change_tuple = (winner, loser, count, round_good)

                changes.append(change_tuple)
        else:
        # print("Finding match for:", old_set)
            for old_set in old_sets:
                # print(old_set['id'], new_set['id'])
            # if old_set['id'] == new_set['id']:
                try:
                    if str(old_set['id']) == str(new_set['id']):
                        print("Matched on:", old_set['id'], new_set['id'])
                        #check if winnerId or completedAt has changed
                        if old_set['winnerId'] == None and new_set['winnerId'] != None:
                            print("Found a change")
                            winnerId = new_set['winnerId']
                            e1Score = new_set['entrant1Score']
                            e2Score = new_set['entrant2Score']
                            round = new_set['fullRoundText']
                            try:
                                round_good = round_dict[round]
                            except:
                                rount_good = round
                            if e1Score > e2Score:
                                count = '{}-{}'.format(e1Score, e2Score)
                            else:
                                count = '{}-{}'.format(e2Score, e1Score)
                            loser = ''
                            for player in new_set['slots']:
                                if player['entrant']['id'] != winnerId:
                                    loser = player['entrant']['name']
                                else:
                                    winner = player['entrant']['name']
                            change_tuple = (winner, loser, count, round_good)

                            changes.append(change_tuple)
                except:
                    pass

    if changes == []:
        print("No changes")
    return changes



        #if yes, add to list of changes
