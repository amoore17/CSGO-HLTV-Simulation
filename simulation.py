'''
Copyright (C) 2018 Austin Moore

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import math # Using the floor() function
import random # Roll for kills and deaths
import sys
from collections import Counter
from hltv import *
from simulationFunctions import *

# Create the game
the_game = game()

# Open the URL and save it to page
print()
url = input('Enter the HLTV URL: ')
trials = int(input("Enter the number of trials: "))

print()
print('Getting team and player stats. This may take a few moments.')
print()

user_agent_spoof = {'User-Agent':'Mozilla/5.0'}
page = connect_to_url(url, user_agent_spoof)

get_all_game_data(the_game, user_agent_spoof, page)

# Get certain variables initialized before the simulation
required_won_matches = math.floor(0.5 * the_game.bestof + 1)
simulations = 3 # Go through kdr, kpr, and hltv_rating simulations
if (the_game.bestof % 2 == 0):
    even_bestof = True
else:
    even_bestof = False
the_game.ties = 0
arr_won_rounds = []

print('Starting the simulations')
print('This is a best of ' + str(the_game.bestof))
print(the_game.teams[0].name + ' vs. ' + the_game.teams[1].name)
last_complete_percent = -1
# Starting the simulations
for current_simulation in range(simulations):
    print()
    calculate_player_range(current_simulation, the_game)
    if (current_simulation == 0):
        print('Kill-Death Ratio Simulation:')
    elif (current_simulation == 1):
        print('Kill Per Round Simulation:')
    elif (current_simulation == 2):
        print('HLTV Rating Simulation:')

    # Start the simulation
    for current_trial in range(trials):
        while ((the_game.teams[0].won_matches != required_won_matches) and(the_game.teams[1].won_matches != required_won_matches)):
            the_game.rounds = 30
            required_won_rounds = math.floor(0.5 * the_game.rounds + 1)
            while ((the_game.teams[0].won_rounds != required_won_rounds) and (the_game.teams[1].won_rounds != required_won_rounds)):
                while (the_game.teams[0].alive == True and the_game.teams[1].alive == True):
                    # Roll a positive or negative value and select a player for the kill
                    positive = random.uniform(0, 1)
                    negative = random.uniform(0, 1)
                    for i in range(the_game.team_count):
                        for i2 in range(the_game.teams[i].player_count):
                            if ((positive >= the_game.teams[i].players[i2].lower_positive_range) and (positive <= the_game.teams[i].players[i2].upper_positive_range)):
                                # Select a player for death
                                if (i == 0): # Assuming that there are only two teams
                                    other_team_number = 1
                                else:
                                    other_team_number = 0
                                for player_number in range(the_game.teams[other_team_number].player_count):
                                    if ((negative >= the_game.teams[other_team_number].players[player_number].lower_negative_range) and (negative <= the_game.teams[other_team_number].players[player_number].upper_negative_range)):
                                        kill_player(the_game, other_team_number, player_number, current_simulation)
                                        check_team_alive_and_update(other_team_number, the_game)
                                        break
                                break
                if ((the_game.teams[0].won_rounds == (required_won_rounds - 1)) and (the_game.teams[1].won_rounds == (required_won_rounds - 1))):
                    the_game.rounds += 6
                    required_won_rounds = math.floor(0.5 * the_game.rounds + 1)
                for i in range(2):
                    revive_all_teams(current_simulation, the_game)
                    calculate_player_range(current_simulation, the_game)
            for i in range(the_game.team_count):
                if (the_game.teams[i].won_rounds == required_won_rounds):
                    the_game.teams[i].won_matches += 1
            arr_won_rounds.append(str(the_game.teams[0].won_rounds) + '-' + str(the_game.teams[1].won_rounds))
            reset_team_rounds(the_game)
            if (even_bestof == True and (the_game.teams[0].won_matches == the_game.teams[1].won_matches)):
                the_game.ties += 1
                break
        for i in range(the_game.team_count):
            if (the_game.teams[i].won_matches == required_won_matches):
                the_game.teams[i].won_trials += 1
        reset_team_matches(the_game)
        percent_complete = str(math.floor(100 * ((current_trial + 1) / trials)))
        if (percent_complete != last_complete_percent):
            sys.stdout.write('\r' + str(current_trial + 1) + ' / ' + str(trials) + ' --- ' + percent_complete + '% Complete')
            sys.stdout.flush()
        last_complete_percent = percent_complete

    print()
    print(the_game.teams[0].name + ' won ' + str(the_game.teams[0].won_trials) + ' trials.')
    print(the_game.teams[1].name + ' won ' + str(the_game.teams[1].won_trials) + ' trials.')
    if (even_bestof == True):
        print('Ties: ' + str(the_game.ties))
    the_game.tie_percentage[current_simulation] = 100 * (the_game.ties / trials)
    the_game.teams[0].win_percentage[current_simulation] = 100 * the_game.teams[0].won_trials / trials
    the_game.teams[1].win_percentage[current_simulation] = 100 * the_game.teams[1].won_trials / trials
    print(the_game.teams[0].name + ' win percentage: ' + str(the_game.teams[0].win_percentage[current_simulation]) + '%')
    print(the_game.teams[1].name + ' win percentage: ' + str(the_game.teams[1].win_percentage[current_simulation]) + '%')
    if (even_bestof == True):
        print('Tie percentage: ' + str(the_game.tie_percentage[current_simulation]) + '%')
    reset_team_trials(the_game)
    count = Counter(arr_won_rounds)
    common = count.most_common()[0]
    common = common[0]
    print('Predicted match score: ' + common)
    the_game.match_score[current_simulation] = common
answer = ''
while (answer != 'y' and answer != 'n'):
    print()
    answer = input('Do you want to export to ODS? (y or n): ')
if (answer == 'y'):
    export_to_ods(the_game)
else:
    print()
    quit()
