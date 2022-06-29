import error_handling as eh
import shot_chart_functions as scf

def run_app():
    while True:
        player_id = eh.check_player_name()
        season = eh.check_season()
        season_type = eh.check_season_type()
        
        player_id, season, season_type = eh.check_games(player_id, season, season_type)
        
        shots_dfs = eh.check_game_date(player_id, season, season_type)

        scf.plot_shot_chart(shots_dfs[0], shots_dfs[1], season_type)

        eh.check_repeat()

if __name__ == "__main__":
    run_app()
