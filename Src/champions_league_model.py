### Champions league model 
import importlib
import datapart

importlib.reload(datapart)
import math
import numpy as np 
import pandas as pd
from scipy.stats import poisson 
from datapart import *
from champions_league_poules import * 

def simulate_games():
    unique_matches = set() # so duplicates will be removed automatically
    games = valid_games()
    for game in games: 
        unique_matches.update(games[game]["Matches"])
    unique_matches = list(unique_matches)
    return unique_matches 



def champions_league_table(): 
    table = {}
    for team in Selected_teams:
        table[team] = {"P": 0, "Pts": 0, "W": 0, "D": 0, "L": 0, "GS": 0, "GC": 0, "GD": 0}
    return table

def simulation(): # This is the real simulation
    matches = simulate_games()
    table = champions_league_table()
    for hometeam, awayteam in matches: 
        lambda_home, lambda_away = Parameter(hometeam, awayteam)
        home_goals = poisson.rvs(lambda_home)
        away_goals = poisson.rvs(lambda_away)
        update_table(table, hometeam, awayteam, home_goals, away_goals)
    return table

def update_table(table, hometeam, awayteam, home_goals, away_goals):
    table[hometeam]["P"] += 1
    table[awayteam]["P"] += 1
    table[hometeam]["GS"] += home_goals
    table[hometeam]["GC"] += away_goals
    table[awayteam]["GS"] += away_goals
    table[awayteam]["GC"] += home_goals
    A = home_goals - away_goals
    table[hometeam]["GD"] += A
    table[awayteam]["GD"] += -A

    if home_goals > away_goals:
                table[hometeam]["W"] += 1
                table[awayteam]["L"] += 1
                table[hometeam]["Pts"] += 3
    elif away_goals > home_goals:
                table[awayteam]["W"] += 1
                table[hometeam]["L"] += 1
                table[awayteam]["Pts"] += 3
    else: 
                table[awayteam]["D"] += 1
                table[hometeam]["D"] += 1
                table[hometeam]["Pts"] += 1
                table[awayteam]["Pts"] += 1
    return table



def table_print(): 
    table = simulation()
    df_table = pd.DataFrame(table).T
    df_table = df_table.sort_values(
    by=["Pts", "GD", "GS"],
    ascending=False)
    df_table = df_table.reset_index()
    df_table = df_table.rename(columns={"index": "Team"})
    df_table.insert(0, "Pos", [f"{i}." for i in range(1, len(df_table) + 1)])
    print(df_table.to_string(index=False))


table_print()








