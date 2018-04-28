'''
Copyright (C) 2018 Austin Moore

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

class player:
    def __init__(self):
        self.name = 'Kirk'
        self.kills = 0
        self.deaths = 0
        self.rounds = 0
        self.kdr = 0.0 # Kill-Death Ratio
        self.dkr = 0.0 # Death-Kill Ratio
        self.kpr = 0.0 # Kills Per Round
        self.dpr = 0.0 # Deaths Per Round
        self.hltv_rating = 0.0
        self.inv_hltv_rating = 0.0
        self.url = ' '
        self.stats_url = ' '
        self.negative = 0.0 # Either dkr, dpr, or inv_hltv_rating
        self.positive = 0.0 # Either kdr, kpr, or hltv_rating
        self.lower_negative_range = 0.0
        self.upper_negative_range = 0.0
        self.lower_positive_range = 0.0
        self.upper_positive_range = 0.0
        self.alive = True

class team:
    def __init__(self):
        self.win_percentage = [0.0, 0.0, 0.0]
        self.lost_percentage = [0.0, 0.0, 0.0]
        self.won_matches = 0
        self.lost_matches = 0
        self.won_trials = 0
        self.lost_trials = 0
        self.won_rounds = 0
        self.lost_rounds = 0
        self.wins = 0
        self.losses = 0
        self.name = 'A-Team'
        self.player_count = 5
        self.players = [player() for i in range(self.player_count)]
        self.url = ' '
        self.total_negative = 0.0 # The addition of all negative on ONE team
        self.alive = True

class game:
    def __init__(self):
        self.match_score = ['0-0', '0-0', '0-0']
        self.tie_percentage = [0.0, 0.0, 0.0]
        self.ties = 0
        self.bestof = 1
        self.rounds = 30
        self.team_count = 2
        self.teams = [team() for i in range(self.team_count)]
        self.score = ['0-0']
        self.score_index = 0
        self.data = ''
