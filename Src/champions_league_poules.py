import math
import numpy as np 
import pandas as pd
import os
import random
current_folder = os.path.dirname(__file__)
project_folder = os.path.dirname(current_folder)

csv_file = os.path.join(project_folder, "Data", "EloRatings_clean.csv")
df = pd.read_csv(csv_file)


df["club"] = df["club"].replace({"FC Kobenhavn": "FC Copenhagen", "Steaua": "FCSB"})
df_1750 = (df[(df["elo"] > 1750) & (df["country"] != "RUS") & (df["club"] != "Recreativo")]
    .sort_values(by="elo", ascending=False)
    .drop_duplicates(subset="club"))

All_teams_1750 = df_1750["club"].tolist()
Selected_teams = random.sample(All_teams_1750, 36)


clubs = list(sorted(df["club"].unique())) 
clubs_country = df.set_index("club")["country"].to_dict()
sorted_clubs_country = dict(sorted(clubs_country.items(), key = lambda item: item[1]))


def country_code():
    Club_code = {}
    for team in Selected_teams:
        Club_code[team] = clubs_country[team]
    return Club_code


def initialize_games():
    teams = {}
    for team in Selected_teams:
        teams[team] = {"Matches": [] }
    return teams 

def generate_all_games():
    all_games = []
    for teamA in Selected_teams:
        for teamB in Selected_teams:
            if teamA != teamB:
                home_team = teamA
                away_team = teamB
                game = (home_team, away_team)
                all_games.append(game)
    return all_games
    

def shuffle_games():
    all_games = generate_all_games()
    random.shuffle(all_games)
    return all_games

def is_valid_game(home_team, away_team, teams):
    game = (home_team, away_team)
    game_switch = (away_team, home_team)
    Club_code = country_code()
    if game in teams[home_team]["Matches"]:
        return False
    elif game in teams[away_team]["Matches"]:
        return False
    elif home_team == away_team:
        return False
    elif game_switch in teams[home_team]["Matches"]:
        return False
    elif game_switch in teams[away_team]["Matches"]:
        return False 
    elif Club_code[home_team] == Club_code[away_team]:
        return False 
    elif len(teams[home_team]["Matches"]) > 7:
        return False
    elif len(teams[away_team]["Matches"]) > 7:
        return False
    else:
        return True 
    
def all_teams_complete(teams):
    for team in teams:
        if len(teams[team]["Matches"]) < 8:
            return False
    return True


def valid_games():
    while True: 
        teams = initialize_games()
        all_games = shuffle_games()
        for game in all_games:
            home_team, away_team = game
            if is_valid_game(home_team, away_team, teams): 
                teams[home_team]["Matches"].append(game) 
                teams[away_team]["Matches"].append(game)
                if all_teams_complete(teams):
                    return teams
                 
        




