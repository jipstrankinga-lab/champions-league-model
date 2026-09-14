import math
import numpy as np 
import pandas as pd
import os
from champions_league_poules import * 

current_folder = os.path.dirname(__file__)
project_folder = os.path.dirname(current_folder)

csv_file1 = os.path.join(project_folder, "data", "Matches_clean.csv")

df1 = pd.read_csv(csv_file1)


## Import data
teams = sorted(pd.concat([df1["HomeTeam"], df1["AwayTeam"]]).unique())
Goals_scored = 0
teams_data = {}
Goals_conceded = 0
Totalgoals = float(df1["FTHome"].sum() + df1["FTAway"].sum())
TotalAverage = float(Totalgoals / len(df1))
TotalAverage_perTeam = TotalAverage / 2
Info = {}

def Goalsscored(team):
    homegoals = float(df1.loc[df1["HomeTeam"] == team, "FTHome"].sum())
    awaygoals = float(df1.loc[df1["AwayTeam"] == team, "FTAway"].sum())
    return homegoals + awaygoals


def Goalsconceded(team):
    homeconceded = float(df1.loc[df1["HomeTeam"] == team, "FTAway"].sum())
    awayconceded = float(df1.loc[df1["AwayTeam"] == team, "FTHome"].sum())
    return homeconceded + awayconceded

def Matches_played(team):
    return float(len(df1[(df1["HomeTeam"] == team) | (df1["AwayTeam"] == team)]))


def Statistics(team):
    Matches = Matches_played(team)
    GS = Goalsscored(team)
    GC = Goalsconceded(team)
    GS_pergame = (GS)/Matches
    GC_pergame = (GC)/Matches
    Attack = GS_pergame / TotalAverage_perTeam
    Defense = GC_pergame / TotalAverage_perTeam
    Info[team] = {"Matches": Matches, "Scored": GS, "Scored_pergame": GS_pergame, "Conceded": GC, "Conceded_pergame": GC_pergame, "Attack_rating": Attack, "Defense_rating": Defense}
    return Info[team]

for team in All_teams_1750:
    Statistics(team)
 
Elo_dict = df_1750.set_index("club")["elo"].to_dict()

def Parameter(team1, team2):
    if team1 not in Info:
        Statistics(team1)

    if team2 not in Info:
        Statistics(team2)
    EloTeam1 = Elo_dict[team1]
    EloTeam2 = Elo_dict[team2]
    EloCorrection_home = -0.07 * (EloTeam2 - 1700)/100
    EloCorrection_away = -0.05 * (EloTeam1 - 1700)/100
    AttackTeam1 = Info[team1]["Attack_rating"]
    DefenseTeam1 =  Info[team1]["Defense_rating"]
    AttackTeam2 = Info[team2]["Attack_rating"]
    DefenseTeam2 =  Info[team2]["Defense_rating"]
    ParameterTeam1 = TotalAverage_perTeam * AttackTeam1 * DefenseTeam2 + EloCorrection_home
    ParameterTeam2 = TotalAverage_perTeam * AttackTeam2 * DefenseTeam1 + EloCorrection_away
    return ParameterTeam1, ParameterTeam2

