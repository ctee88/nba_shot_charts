import shot_chart_functions as scf
import sys
from seasons import seasons


while True:
    print("e.g: LeBron James, Kentavious Caldwell-Pope, Jaren Jackson Jr., Stephen Curry")
    player = input("Enter a player's full name (CASE SENSITIVE): ")
    
    #FORMAT: LeBron James (Player full name with case or use PLAYER_SLUG)
    #Player_string error handling here:
    try:
        player_id = scf.fetch_player_id(player)
    except Exception:
        #Player spelling can be wrong
        print("Invalid player name (see e.g)")
        continue

    while True:
        season_type = input("Enter a season type (Playoffs/Regular Season): ").title()
        if season_type not in scf.season_types:
            print("Please enter a valid season type (Playoffs/Regular Season)\n")
        else:
            break
        
    while True:
        #FORMAT: YYYY-YY
        season = input("Enter a season in the form YYYY-YY (e.g: 2021-22): ")
        if season not in seasons:
            print("Please check date format (see e.g)")
            print("Earliest season available is 1996-97, latest is 2021-22.")
            continue
    
        #e.g case when player IS NOT IN playoffs (team didn't qualify) or NOT IN regular season (e.g injured)
        games_df = scf.fetch_games(player_id, season, season_type)

        if games_df.empty == True:
            print("Invalid player - May have been injured for the entire season or did not qualify for playoffs")
            print("Restarting program...")
           
        ##########REDUNDANT CODE##########
        #Player_id, season and season_type will all valid at this point. 
        #Unless player was not available (injured/did not qualify) -> df.empty == True
        #User is prompted again for previous inputs if fetch games is empty (handled in check_games)
        try:
            #Show user the game dates and matchups from that season+type (playergamelog.py)
            print(scf.fetch_games(player_id, season, season_type))
        except Exception:
            #Season can be wrong
            print("Invalid season, please ensure it is in the form YYYY-YY (see e.g)\n")
            continue
        else:
            break
        ##########REDUNDANT CODE##########

    while True:
        #Fetch shot dfs (made and missed) from specific game
        game_date = input("Enter a date in the form YYYYMMDD (e.g: 3rd May 2022 -> 20220503): ")

        shots_dfs = scf.fetch_shots(player_id, season, season_type, game_date)
        
        #Returns empty df if game_date is invalid
        if shots_dfs[0].empty == True:
            print("Invalid date, please ensure it is in the form of YYYYMMDD (see e.g)\n")
            continue
        else:
            scf.plot_shot_chart(shots_dfs[0], shots_dfs[1], season_type)
            break
            
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
