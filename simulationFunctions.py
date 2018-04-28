import numpy # Using nextafter() function
import re # Regular expression parsing
import urllib.request # Opening page URLs
import pyexcel

# Print all stats for all players on all teams
def print_all_player_stats(the_game):
    for i in range(the_game.team_count):
            for i2 in range(the_game.teams[i].player_count):
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' Name: ' + the_game.teams[i].players[i2].name)
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' Kills: ' + str(the_game.teams[i].players[i2].kills))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' Deaths: ' + str(the_game.teams[i].players[i2].deaths))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' KDR: ' + str(the_game.teams[i].players[i2].kdr))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' DKR: ' + str(the_game.teams[i].players[i2].dkr))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' KPR: ' + str(the_game.teams[i].players[i2].kpr))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' DPR: ' + str(the_game.teams[i].players[i2].dpr))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' HLTV Rating: ' + str(the_game.teams[i].players[i2].hltv_rating))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' Inverse HLTV Rating: ' + str(the_game.teams[i].players[i2].inv_hltv_rating))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' URL: ' + the_game.teams[i].players[i2].url)
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' Detailed URL: ' + the_game.teams[i].players[i2].stats_url)
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' Negative: ' + str(the_game.teams[i].players[i2].negative))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' Positive: ' + str(the_game.teams[i].players[i2].positive))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' Lower Negative Range: ' + str(the_game.teams[i].players[i2].lower_negative_range))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' Upper Negative Range: ' + str(the_game.teams[i].players[i2].upper_negative_range))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' Lower Positive Range: ' + str(the_game.teams[i].players[i2].lower_positive_range))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' Upper Positive Range: ' + str(the_game.teams[i].players[i2].upper_positive_range))
                print('Team ' + str(i + 1) + ' Player ' + str(i2 + 1) + ' Alive: ' + str(the_game.teams[i].players[i2].alive))
                print()

# Calculate the likelihood that a player is to get a kill or die
def calculate_player_range(current_simulation, the_game):
    assign_positive_negative(current_simulation, the_game)
    negative_upper = 0.0 # The current number to set the next player's lower_negative_range
    positive_upper = 0.0 # The current number to set the next player's lower_positive_range
    for i in range(the_game.team_count):
        the_game.teams[i].total_negative = 0.0 # The addition of all negative on ONE team
    total_positive = 0.0 # The addition of all positive on each team

    # Find total_positive and total_negative (for the teams)
    for i in range(the_game.team_count):
            for i2 in range(the_game.teams[i].player_count):
                if (the_game.teams[i].players[i2].alive == True):
                    the_game.teams[i].total_negative += the_game.teams[i].players[i2].negative
                    total_positive += the_game.teams[i].players[i2].positive

    # Find the lower and upper ranges for both negative and positive
    for i in range(the_game.team_count):
        negative_upper = 0.0
        for i2 in range(the_game.teams[i].player_count):
            if (the_game.teams[i].players[i2].alive == True):
                the_game.teams[i].players[i2].lower_negative_range = negative_upper
                the_game.teams[i].players[i2].upper_negative_range = the_game.teams[i].players[i2].lower_negative_range + (the_game.teams[i].players[i2].negative / the_game.teams[i].total_negative)
                negative_upper = numpy.nextafter(the_game.teams[i].players[i2].upper_negative_range, 1)
                the_game.teams[i].players[i2].lower_positive_range = positive_upper
                the_game.teams[i].players[i2].upper_positive_range = the_game.teams[i].players[i2].lower_positive_range + (the_game.teams[i].players[i2].positive / total_positive)
                positive_upper = numpy.nextafter(the_game.teams[i].players[i2].upper_positive_range, 1)

# Assign KDR, KPR, and HLTV Rating to players based on the current simulation
def assign_positive_negative(current_simulation, the_game):
    if (current_simulation == 0):
        for i in range(the_game.team_count):
            for i2 in range(the_game.teams[i].player_count):
                the_game.teams[i].players[i2].negative = the_game.teams[i].players[i2].dkr
                the_game.teams[i].players[i2].positive = the_game.teams[i].players[i2].kdr
    elif (current_simulation == 1):
        for i in range(the_game.team_count):
            for i2 in range(the_game.teams[i].player_count):
                the_game.teams[i].players[i2].negative = the_game.teams[i].players[i2].dpr
                the_game.teams[i].players[i2].positive = the_game.teams[i].players[i2].kpr
    elif (current_simulation == 2):
        for i in range(the_game.team_count):
            for i2 in range(the_game.teams[i].player_count):
                the_game.teams[i].players[i2].negative = the_game.teams[i].players[i2].inv_hltv_rating
                the_game.teams[i].players[i2].positive = the_game.teams[i].players[i2].hltv_rating

# Function to check if a team is alive or dead. Update the class if the team is alive or dead.
def check_team_alive_and_update(team_number, the_game):
    for player_number in range(the_game.teams[team_number].player_count):
        if(the_game.teams[team_number].players[player_number].alive == True):
            the_game.teams[team_number].alive = True
            return
    the_game.teams[team_number].alive = False
    if (team_number == 0):
        the_game.teams[0].lost_rounds += 1
        the_game.teams[1].won_rounds += 1
        return
    elif (team_number == 1):
        the_game.teams[1].lost_rounds += 1
        the_game.teams[0].won_rounds += 1
        return

# Changes player status of team to be alive for the next round
def revive_all_teams(current_simulation, the_game):
    for team_number in range(the_game.team_count):
        the_game.teams[team_number].alive = True
        for player_number in range(the_game.teams[team_number].player_count):
            the_game.teams[team_number].players[player_number].alive = True
    calculate_player_range(current_simulation, the_game)

# Resets the won and lost rounds for a new trial to take place
def reset_team_rounds(the_game):
    for team_number in range(the_game.team_count):
        the_game.teams[team_number].won_rounds = 0
        the_game.teams[team_number].lost_rounds = 0

def reset_team_matches(the_game):
    for team_number in range(the_game.team_count):
        the_game.teams[team_number].won_matches = 0
        the_game.teams[team_number].lost_matches = 0

# Resets the won and lost trials to start a new simulation
def reset_team_trials(the_game):
    the_game.ties = 0
    for team_number in range(the_game.team_count):
        the_game.teams[team_number].won_trials = 0
        the_game.teams[team_number].lost_trials = 0

# Function to kill a player. Run calculate_player_range() to find the new range of all players
def kill_player(the_game, team_number, player_number, current_simulation):
    the_game.teams[team_number].players[player_number].alive = False
    the_game.teams[team_number].players[player_number].positive = 0.0
    the_game.teams[team_number].players[player_number].negative = 0.0
    the_game.teams[team_number].players[player_number].lower_negative_range = 0.0
    the_game.teams[team_number].players[player_number].upper_negative_range = 0.0
    the_game.teams[team_number].players[player_number].lower_positive_range = 0.0
    the_game.teams[team_number].players[player_number].upper_positive_range = 0.0
    calculate_player_range(current_simulation, the_game)

def date_converter(date):
    day = re.findall(r'(\d*)\w*', date)
    day = day[0]
    month = re.findall(r'of (\w*) ', date)
    month = month[0]
    if (month == 'January'):
        month = '1'
    elif (month == 'February'):
        month = '2'
    elif (month == 'March'):
        month = '3'
    elif (month == 'April'):
        month = '4'
    elif (month == 'May'):
        month = '5'
    elif (month == 'June'):
        month = '6'
    elif (month == 'July'):
        month = '7'
    elif (month == 'August'):
        month = '8'
    elif (month == 'September'):
        month = '9'
    elif (month == 'October'):
        month = '10'
    elif (month == 'November'):
        month = '11'
    elif (month == 'December'):
        month = '12'
    year = re.findall(r'.* of \w* (\d*)', date)
    year = year[0]
    year = year[2:4]
    date = month + '/' + day + '/' + year
    return date

def get_all_game_data(the_game, user_agent_spoof, page):
    # Get the best of count
    bestof = re.findall(r'<div class="padding preformatted-text">Best of (\d)', page)
    bestof = bestof[0]
    bestof = int(bestof)
    the_game.bestof = bestof

    the_game.date = re.findall(r'<div class="date".*?data-unix="\d*">(.*?)</div', page)
    the_game.date = the_game.date[0]
    the_game.date = date_converter(the_game.date)

    # Find and save team names
    for i in range(the_game.team_count):
        the_game.teams[i].name = re.findall(r'<div class="team' + str(i + 1) + '-gradient">.*<img alt="(.*?)" src', page)
        the_game.teams[i].name = the_game.teams[i].name[0]

    # Find the url to all teams
    for i in range(the_game.team_count):
        the_game.teams[i].url = re.findall(r'<div class="team' + str(i + 1) + '-gradient"><a href="(/\w*/\d*/.*?)"><img', page)
        the_game.teams[i].url = the_game.teams[i].url[0]
        the_game.teams[i].url = 'https://www.hltv.org' + the_game.teams[i].url

    # Team loop
    # Get player stats
    for i in range(the_game.team_count): # Open the URL to the teams one at a time
        page = connect_to_url(the_game.teams[i].url, user_agent_spoof)

        # Get player names and URLs
        player_names = re.findall(r'class="text-ellipsis bold">(.*?)</span>', page)
        player_urls = re.findall(r'<a href="(/player/\d*?/.*?)">', page)
        # Append hltv.org to all URLs
        for i2 in range(len(player_urls)):
            player_urls[i2] = 'https://www.hltv.org' + player_urls[i2]

        # Player loop
        # Assign player names, URLs, and stats to player objects
        for i2 in range(the_game.teams[i].player_count):
            # Assign names and main page URLs
            the_game.teams[i].players[i2].name = player_names[i2]
            the_game.teams[i].players[i2].url = player_urls[i2]

            # Open main player URLs and assign the URL to their detailed stats
            page = connect_to_url(the_game.teams[i].players[i2].url, user_agent_spoof)

            # Assign detailed stats URLs
            the_game.teams[i].players[i2].stats_url = re.findall(r'<a href="(/stats/players/\d*?/.*?)" class', page)
            the_game.teams[i].players[i2].stats_url = the_game.teams[i].players[i2].stats_url[0]
            the_game.teams[i].players[i2].stats_url = 'https://www.hltv.org' + the_game.teams[i].players[i2].stats_url

            # Open the detailed stats URLs
            page = connect_to_url(the_game.teams[i].players[i2].stats_url, user_agent_spoof)

            # Grab player stats
            # Grab kills
            the_game.teams[i].players[i2].kills = re.findall(r'<div class="stats-row"><span>Total kills</span><span>(\d*?)</span>', page, re.I)
            the_game.teams[i].players[i2].kills = int(the_game.teams[i].players[i2].kills[0])
            #print('Player ' + str(i2 + 1) + ' kills: ' + str(the_game.teams[i].players[i2].kills))

            # Grab deaths
            the_game.teams[i].players[i2].deaths = re.findall(r'<div class="stats-row"><span>Total deaths</span><span>(\d*)', page, re.I)
            the_game.teams[i].players[i2].deaths = int(the_game.teams[i].players[i2].deaths[0])
            #print('Player ' + str(i2 + 1) + ' deaths: ' + str(the_game.teams[i].players[i2].deaths))

            # Grab rounds
            the_game.teams[i].players[i2].rounds = re.findall(r'<div class="stats-row"><span>Rounds played</span><span>(\d*)', page, re.I)
            the_game.teams[i].players[i2].rounds = int(the_game.teams[i].players[i2].rounds[0])
            #print('Player ' + str(i2 + 1) + ' rounds: ' + str(the_game.teams[i].players[i2].rounds))

            # Grab HLTV Rating
            the_game.teams[i].players[i2].hltv_rating = re.findall(r'"strong">(.*?)</span></div>', page, re.I)
            the_game.teams[i].players[i2].hltv_rating = float(the_game.teams[i].players[i2].hltv_rating[0])
            #print('Player ' + str(i2 + 1) + ' HLTV Rating: ' + str(the_game.teams[i].players[i2].hltv_rating))

            # Calculate kdr
            the_game.teams[i].players[i2].kdr = the_game.teams[i].players[i2].kills / the_game.teams[i].players[i2].deaths

            # Calculate dkr
            the_game.teams[i].players[i2].dkr = the_game.teams[i].players[i2].deaths / the_game.teams[i].players[i2].kills

            # Calculate kpr
            the_game.teams[i].players[i2].kpr = the_game.teams[i].players[i2].kills / the_game.teams[i].players[i2].rounds

            # Calculate dpr
            the_game.teams[i].players[i2].dpr = the_game.teams[i].players[i2].deaths / the_game.teams[i].players[i2].rounds

            # Calculate inv_hltv_rating
            the_game.teams[i].players[i2].inv_hltv_rating = pow(the_game.teams[i].players[i2].hltv_rating, (-1))

def connect_to_url(url, user_agent_spoof):
    req = urllib.request.Request(url, headers=user_agent_spoof)
    try:
        print('Trying to connect to: ' + url)
        page = urllib.request.urlopen(req)
        print('URL opened successfully.')
        print()
    except:
        print('Failed to connect to: ' + url)
        print()
    page = page.read()
    page = page.decode('utf-8')
    return page

def export_to_ods(the_game):
    sheet = pyexcel.get_sheet(file_name='SimulationsCopy.ods')
    if ((the_game.bestof % 2) != 0):
        if (the_game.teams[0].win_percentage[0] > the_game.teams[1].win_percentage[0]):
            kdr_team_win = the_game.teams[0].name
        elif (the_game.teams[1].win_percentage[0] > the_game.teams[0].win_percentage[0]):
            kdr_team_win = the_game.teams[1].name
        else:
            kdr_team_win = 'Either'

        if (the_game.teams[0].win_percentage[1] > the_game.teams[1].win_percentage[1]):
            kpr_team_win = the_game.teams[0].name
        elif (the_game.teams[1].win_percentage[1] > the_game.teams[0].win_percentage[1]):
            kpr_team_win = the_game.teams[1].name
        else:
            kpr_team_win = 'Either'

        if (the_game.teams[0].win_percentage[2] > the_game.teams[1].win_percentage[2]):
            hltv_rating_team_win = the_game.teams[0].name
        elif (the_game.teams[1].win_percentage[2] > the_game.teams[0].win_percentage[2]):
            hltv_rating_team_win = the_game.teams[1].name
        else:
            hltv_rating_team_win = 'Either'
    else:
        if ((the_game.tie_percentage[0] > the_game.teams[0].win_percentage[0]) and (the_game.tie_percentage[0] > the_game.teams[1].win_percentage[0])):
            kdr_team_win = 'Tie'
        elif (the_game.teams[0].win_percentage[0] > the_game.teams[1].win_percentage[0]):
            kdr_team_win = the_game.teams[0].name
        elif (the_game.teams[1].win_percentage[0] > the_game.teams[0].win_percentage[0]):
            kdr_team_win = the_game.teams[1].name
        else:
            kdr_team_win = 'Either'

        if ((the_game.tie_percentage[1] > the_game.teams[0].win_percentage[1]) and (the_game.tie_percentage[1] > the_game.teams[1].win_percentage[1])):
            kpr_team_win = 'Tie'
        elif (the_game.teams[0].win_percentage[1] > the_game.teams[1].win_percentage[1]):
            kpr_team_win = the_game.teams[0].name
        elif (the_game.teams[1].win_percentage[1] > the_game.teams[0].win_percentage[1]):
            kpr_team_win = the_game.teams[1].name
        else:
            kpr_team_win = 'Either'

        if ((the_game.tie_percentage[2] > the_game.teams[0].win_percentage[2]) and (the_game.tie_percentage[1] > the_game.teams[1].win_percentage[2])):
            hltv_rating_team_win = 'Tie'
        elif (the_game.teams[0].win_percentage[2] > the_game.teams[1].win_percentage[2]):
            hltv_rating_team_win = the_game.teams[0].name
        elif (the_game.teams[1].win_percentage[2] > the_game.teams[0].win_percentage[2]):
            hltv_rating_team_win = the_game.teams[1].name
        else:
            hltv_rating_team_win = 'Either'

    if ((the_game.bestof % 2) != 0):
        sheet.row += [the_game.bestof, the_game.date, the_game.teams[0].name + ' vs. ' + the_game.teams[1].name,
        str(the_game.teams[0].win_percentage[0]) + ' - ' + str(the_game.teams[1].win_percentage[0]), str(the_game.teams[0].win_percentage[1]) + ' - ' + str(the_game.teams[1].win_percentage[1]),
        str(the_game.teams[0].win_percentage[2]) + ' - ' + str(the_game.teams[1].win_percentage[2]), kdr_team_win, kpr_team_win, hltv_rating_team_win,
        the_game.match_score[0], the_game.match_score[1], the_game.match_score[2]]
        sheet.save_as('SimulationsCopy.ods')
        print(sheet)
    else:
        sheet.row += [the_game.bestof, the_game.date, the_game.teams[0].name + ' vs. ' + the_game.teams[1].name,
        str(the_game.teams[0].win_percentage[0]) + ' - ' + str(the_game.teams[1].win_percentage[0]) + ' - ' + str(the_game.tie_percentage[0]),
        str(the_game.teams[0].win_percentage[1]) + ' - ' + str(the_game.teams[1].win_percentage[1]) + ' - ' + str(the_game.tie_percentage[0]),
        str(the_game.teams[0].win_percentage[2]) + ' - ' + str(the_game.teams[1].win_percentage[2]) + ' - ' + str(the_game.tie_percentage[0]),
        kdr_team_win, kpr_team_win, hltv_rating_team_win,
        the_game.match_score[0], the_game.match_score[1], the_game.match_score[2]]
        sheet.save_as('SimulationsCopy.ods')
        print(sheet)
