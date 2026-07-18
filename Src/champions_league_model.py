### Champions league model 
import importlib
import datapart

importlib.reload(datapart)
import math
import numpy as np 
import pandas as pd
from scipy.stats import poisson 
from datapart import *

team1 = input("Voer het thuisteam in: ")
team2 = input("Voer het uitteam in: ")

def Chances(team1, team2):
    Q1, Q2 = Parameter(team1, team2)
    ChanceTeam1 = 0
    DrawChance = 0
    ChanceTeam2 = 0 
    # Chance that team1 wins
    for i in range(1, 100):
        for k in range(0, i): 
            A = poisson.pmf(i, Q1)*poisson.pmf(k, Q2)
            ChanceTeam1 += A
    # Chance for a draw
    for i in range(0, 100):
        B = poisson.pmf(i, Q1)*poisson.pmf(i, Q2)
        DrawChance += B
    # Chance that team2 wins 
    for i in range(1, 100):
        for k in range(0, i): 
            C = poisson.pmf(k, Q1)*poisson.pmf(i, Q2)
            ChanceTeam2 += C
    print(ChanceTeam1, DrawChance, ChanceTeam2)
    







Chances(team1, team2)
