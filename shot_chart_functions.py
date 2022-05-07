from matplotlib.patches import Circle, Rectangle, Arc
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playergamelog
import matplotlib.pyplot as plt
import pandas as pd
import json

season_types = ('Playoffs', 'Regular Season')

#Fetch player ID from player full name
def fetch_player_id(player_name):
    response = commonallplayers.CommonAllPlayers()
    data = json.loads(response.get_json())

    #Define rows and columns before (readability)
    players = data['resultSets'][0]

    players_df = pd.DataFrame(players['rowSet'], columns=players['headers'])

    # player_df = players_df[players_df.DISPLAY_FIRST_LAST==player_name]
    # return player_df['PERSON_ID'].values[0]

    # player_id = players_df[players_df['DISPLAY_FIRST_LAST']==player_name]
    # return player_id['PERSON_ID'].values[0]

    player_series = players_df.loc[players_df['DISPLAY_FIRST_LAST']==player_name, 'PERSON_ID']

    return player_series.iloc[0]

# print(fetch_player_id('James Harden'))
# print(type(fetch_player_id('James Harden')))

#Return df for all games (PO/RS) for specific season
#Date format is in MMDDYYYY - Might not need ot return games_df
#Could just print the df to user and fiddle around with date conversion
#NBA only started tracking PBP date from the 1996-97 season - so this is earliest possible season
def fetch_games(player_id, season, season_type):
    response = playergamelog.PlayerGameLog(
        player_id = player_id,
        season = season,
        season_type_all_star = season_type
    )
    
    data = json.loads(response.get_json())

    game_logs = data['resultSets'][0]
    game_dates = [row[3] for row in game_logs['rowSet']]
    matchups = [row[4] for row in game_logs['rowSet']]
    
    rows = zip(game_dates, matchups)
    headers = [game_logs['headers'][3], game_logs['headers'][4]]

    games_df = pd.DataFrame(rows, columns=headers)

    return games_df

    #SHOW ALL GAMES IN DF IN CONSOLE (there is a command for this) i.e for RS show all games (shortens df currently)

# show_games(201935, '2021-22', 'Regular Season')

#Return made and missed dfs for specific game
def fetch_shots(player_id, season, season_type, game_date):
    response = shotchartdetail.ShotChartDetail(
        team_id = 0,
        context_measure_simple = 'FGA',
        player_id = player_id,
        season_nullable = season,
        season_type_all_star = season_type,
    )
    
    data = json.loads(response.get_json())
    shots = data['resultSets'][0]
    headers = shots['headers']
    rows = shots['rowSet']
    
    shots_df = pd.DataFrame(rows, columns=headers)
    game_shots_df = shots_df.loc[shots_df['GAME_DATE']==game_date]
    made_shots_df = game_shots_df.loc[game_shots_df['SHOT_MADE_FLAG']==1]
    missed_shots_df = game_shots_df.loc[game_shots_df['SHOT_MADE_FLAG']==0]

    return made_shots_df, missed_shots_df

# print(fetch_shots(201935, '2021-22', 'Playoffs', '20220416'))
# print(fetch_shots(893, '1985-86', 'Playoffs', '19860420'))
# print(fetch_shots(201935, '2021-22', 'Playoffs', '     '))

def draw_court(ax=None, color='black', lw=2):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, width=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # Outer lines (Baseline, Halfcourt and Sidelines)
    outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                            color=color, fill=False)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc, outer_lines]

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

made_shots_df = pd.read_excel("C:/Users/camer/OneDrive/Desktop/git_ver/shot_chart/made_shots.xlsx")
missed_shots_df = pd.read_excel("C:/Users/camer/OneDrive/Desktop/git_ver/shot_chart/missed_shots.xlsx")

def plot_shot_chart(made_df, missed_df, season_type):
    plt.figure(figsize=(12, 11))
    plt.scatter(made_df.LOC_X, made_df.LOC_Y, c='b')
    plt.scatter(missed_df.LOC_X, missed_df.LOC_Y, c='r', marker='x')
    #Format date GAME_DATE??
    #Title text values
    player_name = made_df['PLAYER_NAME'].values[0]
    home_team = made_df['HTM'].values[0]
    away_team = made_df['VTM'].values[0]
    game_date = made_df['GAME_DATE'].values[0]

    plt.title(label=f'''
        {player_name} FGA\n
        {home_team} vs {away_team} on {game_date}\n
        @{home_team}\n
        {season_type}
        ''',
        fontsize=10
    )

    draw_court()
    plt.xlim(-250, 250)
    plt.ylim(422.5, -47.5)

    plt.show()

# plot_shot_chart(made_shots_df, missed_shots_df, 'Playoffs')