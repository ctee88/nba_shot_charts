from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playergamelog
import datetime
import plotly.graph_objects as go
import pandas as pd
import numpy as np
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
#Date format is in MMDDYYYY - Might not need to return games_df
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

    #TODO: SHOW ALL GAMES IN DF IN CONSOLE (there is a command for this) i.e for RS show all games (shortens df currently)
    #TODO: SHOW points for each game?
    #Maybe get FGM/FGA from here?

#Join game times with 1 zero padded to the left i.e: 7 MINUTES 1 SECOND = '07:01'
def join_game_times(df):
    game_times = {}
    game_times['TIME_REMAINING'] = []

    for row in range(0, len(df)):
        mins_and_secs = [df['MINUTES_REMAINING'], df['SECONDS_REMAINING']]
        #Declare mins and secs variables for readability, then format them by padding with one 0 to the left
        mins = mins_and_secs[0].values[row]
        secs = mins_and_secs[1].values[row]

        game_time = f'{mins:02}:{secs:02}'
        game_times['TIME_REMAINING'].append(game_time)

    #Add new column with correctly formatted time to df
    df = df.assign(TIME_REMAINING=game_times['TIME_REMAINING'])

    return df

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

    #Format game time correctly
    game_shots_df = join_game_times(game_shots_df)

    made_shots_df = game_shots_df.loc[game_shots_df['SHOT_MADE_FLAG']==1]
    missed_shots_df = game_shots_df.loc[game_shots_df['SHOT_MADE_FLAG']==0]

    return made_shots_df, missed_shots_df

# From: https://towardsdatascience.com/interactive-basketball-data-visualizations-with-plotly-8c6916aaa59e
def draw_plotly_court(fig, fig_width=900, margins=10):
        
    # From: https://community.plot.ly/t/arc-shape-with-path/7205/5
    def ellipse_arc(x_center=0.0, y_center=0.0, a=10.5, b=10.5, start_angle=0.0, end_angle=2 * np.pi, N=200, closed=False):
        t = np.linspace(start_angle, end_angle, N)
        x = x_center + a * np.cos(t)
        y = y_center + b * np.sin(t)
        path = f'M {x[0]}, {y[0]}'
        for k in range(1, len(t)):
            path += f'L{x[k]}, {y[k]}'
        if closed:
            path += ' Z'
        return path

    fig_height = fig_width * (470 + 2 * margins) / (500 + 2 * margins)
    fig.update_layout(width=fig_width, height=fig_height)

    fig.update_xaxes(range=[-250, 250])
    fig.update_yaxes(range=[422.5, -47.5])

    threept_break_y = 89.47765084
    three_line_col = "#777777"
    main_line_col = "#777777"

    fig.update_layout(
        # Line Horizontal
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        shapes=[
            dict(
                type="rect", x0=-250, y0=-52.5, x1=250, y1=417.5,
                line=dict(color=main_line_col, width=1),
                layer='below'
            ),
            dict(
                type="rect", x0=-80, y0=-52.5, x1=80, y1=137.5,
                line=dict(color=main_line_col, width=1),
                layer='below'
            ),
            dict(
                type="rect", x0=-60, y0=-52.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=1),
                layer='below'
            ),
            dict(
                type="circle", x0=-60, y0=77.5, x1=60, y1=197.5, xref="x", yref="y",
                line=dict(color=main_line_col, width=1),
                layer='below'
            ),
            dict(
                type="line", x0=-60, y0=137.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=1),
                layer='below'
            ),

            dict(
                type="rect", x0=-2, y0=-7.25, x1=2, y1=-12.5,
                line=dict(color="#ec7607", width=1),
                fillcolor='#ec7607',
            ),
            dict(
                type="circle", x0=-7.5, y0=-7.5, x1=7.5, y1=7.5, xref="x", yref="y",
                line=dict(color="#ec7607", width=1),
            ),
            dict(
                type="line", x0=-30, y0=-12.5, x1=30, y1=-12.5,
                line=dict(color="#ec7607", width=1),
            ),

            dict(type="path",
                 path=ellipse_arc(a=40, b=40, start_angle=0, end_angle=np.pi),
                 line=dict(color=main_line_col, width=1), layer='below'),
            dict(type="path",
                 path=ellipse_arc(a=237.5, b=237.5, start_angle=0.386283101, end_angle=np.pi - 0.386283101),
                 line=dict(color=main_line_col, width=1), layer='below'),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=220, y0=-52.5, x1=220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),

            dict(
                type="line", x0=-250, y0=227.5, x1=-220, y1=227.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=250, y0=227.5, x1=220, y1=227.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=17.5, x1=-80, y1=17.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=27.5, x1=-80, y1=27.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=57.5, x1=-80, y1=57.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=87.5, x1=-80, y1=87.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=17.5, x1=80, y1=17.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=27.5, x1=80, y1=27.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=57.5, x1=80, y1=57.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=87.5, x1=80, y1=87.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),

            dict(type="path",
                 path=ellipse_arc(y_center=417.5, a=60, b=60, start_angle=-0, end_angle=-np.pi),
                 line=dict(color=main_line_col, width=1), layer='below'),

        ]
    )
    return True

def plot_shot_chart(made_df, missed_df, season_type):
    fig = go.Figure()
    draw_plotly_court(fig)

    #Data used for hovertext
    custom_columns = ['PERIOD', 'TIME_REMAINING', 'ACTION_TYPE', 'SHOT_DISTANCE']
    #Add made trace for made and missed shots
    fig.add_trace(go.Scatter(
        x=made_df['LOC_X'], 
        y=made_df['LOC_Y'], 
        mode='markers', 
        name='MADE',
        customdata=made_df[custom_columns],
        marker=dict(
            size=10,
            color='green',
            symbol='circle-open'
            ),
        hovertemplate='<br>'.join([
            '<b>QUARTER %{customdata[0]}</b>',
            'Game Time: %{customdata[1]}',
            'Shot Description: %{customdata[2]}',
            'Distance: %{customdata[3]}ft'
        ])
        )
    )

    fig.add_trace(go.Scatter(
        x=missed_df['LOC_X'],
        y=missed_df['LOC_Y'], 
        mode='markers', 
        name='MISSED',
        customdata=missed_df[custom_columns],
        marker=dict(
            size=10,
            color='red',
            symbol='x-open'
            ),
        hovertemplate='<br>'.join([
            '<b>QUARTER %{customdata[0]}</b>',
            'Game Time: %{customdata[1]}',
            'Shot Description: %{customdata[2]}',
            'Distance: %{customdata[3]}ft'
        ])
        )
    )

    player_name = made_df['PLAYER_NAME'].values[0]
    home_team = made_df['HTM'].values[0]
    away_team = made_df['VTM'].values[0]
    game_date = made_df['GAME_DATE'].values[0]

    #format game date
    new_game_date = datetime.datetime.strptime(str(game_date), "%Y%m%d").strftime("%d/%m/%Y")

    fig.update_layout(
        title_text=f'''
            {player_name} FGA | {home_team} vs {away_team} | {new_game_date} | @{home_team} | {season_type}
            ''',
        title_x=0.5,
        title_y=0.97
    )

    fig.show(config=dict(displayModeBar=False))

