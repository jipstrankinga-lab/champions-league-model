import math
import numpy as np 
import pandas as pd
import os
current_folder = os.path.dirname(__file__)
csv_file1 = os.path.join(current_folder, "Matches.csv")

df1 = pd.read_csv(csv_file1)


## Import data
teams = sorted(pd.concat([df1["HomeTeam"], df1["AwayTeam"]]).unique())
Goals_scored = 0
teams_data = {}
Goals_conceded = 0
Totalgoals = df1["FTHome"].sum() + df1["FTAway"].sum()
TotalAverage = Totalgoals / len(df1)
ratings = {}


def Goalsscored(team):
        Goals_scored = 0
        for index, row in teams_data[team].iterrows():
            if row["HomeTeam"] == team:
                Goals_scored += row["FTHome"]
            else:
                Goals_scored += row["FTAway"]
        return Goals_scored

def Goalsconceded(team):
    Goals_conceded = 0
    for index, row in teams_data[team].iterrows():
            if row["HomeTeam"] == team:
                Goals_conceded += row["FTAway"]
            else:
                Goals_conceded += row["FTHome"]
    return Goals_conceded

def Matches_played(team):
    return len(teams_data[team])


def Rating(team):
    GS = Goalsscored(team)
    GC = Goalsconceded(team)
    GS_pergame = (GS)/Matches_played(team)
    GC_pergame = (GC)/Matches_played(team)
    Attack = GS_pergame / TotalAverage
    Defense = GC_pergame / TotalAverage
    ratings[team] = {"Attack": Attack, "Defense": Defense}
    return ratings[team]

for team in teams:
    Rating(team)

    
def Parameter(team1, team2):
    AttackTeam1 = ratings[team1]["Attack"]
    DefenseTeam1 =  ratings[team1]["Defense"]
    AttackTeam2 = ratings[team2]["Attack"]
    DefenseTeam2 =  ratings[team2]["Defense"]
    ParameterTeam1 = TotalAverage * AttackTeam1 * DefenseTeam2
    ParameterTeam2 = TotalAverage * AttackTeam2 * DefenseTeam1
    return ParameterTeam1, ParameterTeam2
    
