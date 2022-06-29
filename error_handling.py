import shot_chart_functions as scf
import sys
from seasons import seasons

#Validates player name is correct
def check_player_name():
    while True:

        print("e.g: LeBron James, Kentavious Caldwell-Pope, Jaren Jackson Jr., Stephen Curry")
        player = input("Enter a player's full name (CASE SENSITIVE): ")

        try:
            player_id = scf.fetch_player_id(player)
            return player_id
        except Exception:
            print("Invalid player name (see e.g)")
            continue

#Validates season is correct
def check_season():
    while True:
        season = input("Enter a season in the form YYYY-YY (e.g: 2021-22): ")
        if season not in seasons:
            print("Please check date format (see e.g)")
            print("Earliest season available is 1996-97, latest is 2021-22.")
            continue

        return season

#Validates season type is correct
def check_season_type():
    while True:
        season_type = input("Enter a season type (Playoffs/Regular Season): ").title()
        if season_type not in scf.season_types:
            print("Please enter a valid season type (Playoffs/Regular Season)\n")
            continue
            
        return season_type

#Validates that the player was present in Regular Season or Playoffs for specific season
#Prompts user again for player_id, season and season_type again if not.
def check_games(player_id, season, season_type):
    while True:
        games_df = scf.fetch_games(player_id, season, season_type)

        #Returns empty df if player was unavailable for given season and season_type
        if games_df.empty == True:
            print("Invalid player - May have been injured for the entire season or did not qualify for playoffs")
            print("Please ensure your desired player is/was active with respect to your season and season type")
            print("Restarting program...")
            player_id = check_player_name()
            season = check_season()
            season_type = check_season_type()
            continue
        
        print("AVAILABLE GAMES:")
        print(games_df)
        return player_id, season, season_type

#Validates that the game_date is correct
def check_game_date(player_id, season, season_type):
    while True:
        game_date = input("Enter a date in the form YYYYMMDD (e.g: 3rd May 2022 -> 20220503): ")

        shots_dfs = scf.fetch_shots(player_id, season, season_type, game_date)

        #Returns empty df if game_date is invalid 
        #CAN ALSO BE EMPTY IF THE PLAYER PLAYED GARBAGE MINUTES AND DIDN'T SCORE ANY POINTS
        if shots_dfs[0].empty == True:
            print("Invalid date, please ensure it is in the form of YYYYMMDD (see e.g)\n")
            continue
    
        return shots_dfs

#Repeat loop to initialise another plot if desired        
def check_repeat():
    while True:
        repeat = input("\nWould you like to plot another shot chart? (Y/N): ").upper()

        if repeat == 'N':
            print("\nExiting program...")
            sys.exit()
        elif repeat == 'Y':
            print("\nStarting another visualisation...")
            break
        else:
            print("\nPlease provide your answer with either Y or N")
