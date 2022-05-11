import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go
from nba_api.stats.endpoints import shotchartdetail

# response = shotchartdetail.ShotChartDetail(
#     team_id = 0, 
#     context_measure_simple = 'FGA',
#     player_id = 201935,
#     season_nullable = '2021-22',
#     season_type_all_star = 'Playoffs'
# )

# data = json.loads(response.get_json())
# shots = data['resultSets'][0]
# headers = shots['headers']
# rows = shots['rowSet']

# shots_df = pd.DataFrame(rows, columns=headers)

# #Get shots for James Harden on 20220508
# game_shots_df = shots_df[shots_df['GAME_DATE']=='20220508']

# game_shots_df.to_excel("C:/Users/camer/OneDrive/Desktop/git_ver/shot_chart/eh_ver/harden_game_shots.xlsx", index=False)

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

game_shots_df = pd.read_excel("C:/Users/camer/OneDrive/Desktop/git_ver/shot_chart/eh_ver/harden_game_shots.xlsx")

made_df = game_shots_df[game_shots_df['SHOT_MADE_FLAG']==1]
missed_df = game_shots_df[game_shots_df['SHOT_MADE_FLAG']==0]

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

made_df = join_game_times(made_df)
missed_df = join_game_times(missed_df)

custom_columns = ['PERIOD', 'TIME_REMAINING', 'ACTION_TYPE', 'SHOT_DISTANCE']

fig = go.Figure()
draw_plotly_court(fig)
#Add made trace for made and missed shots
fig.add_trace(go.Scatter(
    x=made_df['LOC_X'], 
    y=made_df['LOC_Y'], 
    mode='markers', 
    name='MADE',
    customdata=made_df[custom_columns],
    marker=dict(
        size=10,
        color='blue',
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

fig.update_layout(
    title_text=f'''
        {player_name} FGA - {home_team} vs {away_team} - on {game_date} - @{home_team} - Playoffs
        ''',
    title_x=0.5,
    title_y=0.97
)

fig.show(config=dict(displayModeBar=False))

#TODO:
# - hovertext with customdata
# - title formatted with correct values
# - total fgm/fga annotated on plot

# fig.update_layout(yaxis_range=[4, -4]) inverting y-range (mirrors plot horizontally so right side of hoop is right side of viewer)

# Add missed trace
