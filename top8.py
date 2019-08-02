class Top8:
    def __init__(self, res):
        self.titles = ['grand_final_reset','grand_final','winners_final','losers_final','losers_semi',
        'winners_semi1','winners_semi2','losers_quarters1','losers_quarters2','losers_r11','losers_r12']
        self.list = []
        self.losers_quarters1 = None
        self.winners_semi1 = None
        self.losers_r11 = None
        self.grand_final_reset = None
        self.bracket = {}
        if res == {}:
            return None
        sets = res['data']['phase']['sets']['nodes']
        for set in sets:
            if set['fullRoundText'] == 'Grand Final Reset':
                self.bracket['grand_final_reset'] = Set(set, 'Grand Finals Reset')
            elif set['fullRoundText'] == 'Grand Final':
                self.bracket['grand_final'] = Set(set, 'Grand Finals')
            elif set['fullRoundText'] == 'Winners Final':
                self.bracket['winners_final'] = Set(set, 'Winners Finals')
            elif set['fullRoundText'] == 'Losers Final':
                self.bracket['losers_final'] = Set(set, 'Losers Finals')
            elif set['fullRoundText'] == 'Losers Semi-Final':
                self.bracket['losers_semi'] = Set(set, 'Losers Semi-Finals')
            elif set['fullRoundText'] == 'Winners Semi-Final':
                if self.bracket.get('winners_semi1', '') == None:
                    self.bracket['winners_semi1'] = Set(set, 'Winners Semi-Finals')
                else:
                    self.bracket['winners_semi2'] = Set(set, 'Winners Semi-Finals')
            elif set['fullRoundText'] == 'Losers Quarter-Final':
                if self.bracket.get('losers_quarters1', '') == None:
                    self.bracket['losers_quarters1'] = Set(set, 'Losers Quarter-Finals')
                else:
                    self.bracket['losers_quarters2'] = Set(set, 'Losers Quarter-Finals')
            elif set['fullRoundText'] == 'Losers Round 1':
                if self.bracket.get('losers_r11', '') == None:
                    self.bracket['losers_r11'] = Set(set, 'Losers Round 1')
                else:
                    self.bracket['losers_r12'] = Set(set, 'Losers Round 1')

    def compare(self, old):
        changes = []
        for title in self.titles:
            if self.bracket.get(title, '') != old.bracket.get(title, ''):
                if old.bracket.get(title, '') == '':
                    old_games = 1
                else:
                    old_games = len(old.bracket[title].games) + 1
                new_games = len(self.bracket[title].games) + 1
                for x in range(old_games, new_games):
                    basestr = str(self.bracket[title].games[x])
                    basestr += ' in game ' + str(x)
                    changes.append(basestr)
        return changes


    def __str__(self):
        string = ''
        for x in self.bracket.values():
            string += str(x)
        return string


class Set:

    def __init__(self, set, name):
        self.name = name
        self.player1 = Player(set['slots'][0])
        self.player2 = Player(set['slots'][1])
        self.games = []
        if set['games'] != None:
            for game in set['games']:
                self.games.append(Game(game, [self.player1, self.player2]))
        self.winner = set['winnerId']

    def __str__(self):
        string = "Player1: " + str(self.player1) +  " Player2: " + str(self.player2) + " in " + self.name + "\n"
        count = 0
        for game in self.games:
            count += 1
            string += "\tGame " + str(count) +  " was won by: " + game.winnername + "\n"
        return string

class Game:

    def __init__(self, game, players):
        self.winnerid = game['winnerId']
        if players[0].id == self.winnerid:
            self.winnername = players[0].name
            self.losername = players[1].name
        else:
            self.winnername = players[1].name
            self.losername = players[0].name

    def __str__(self):
        if self.winnername != None:
            return self.winnername + ' defeated ' + self.losername


class Player:

    def __init__(self, slots):
        if slots['entrant'] != None:
            self.name = slots['entrant']['name']
            self.id = slots['entrant']['id']
        else:
            self.name = ''
            self.id = ''

    def __str__(self):
        return self.name
