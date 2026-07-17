import math
import numpy as np 
import pandas as pd
import os
current_folder = os.path.dirname(__file__)
project_folder = os.path.dirname(current_folder)

csv_file = os.path.join(project_folder, "Data", "EloRatings_clean.csv")
df = pd.read_csv(csv_file)

clubs = sorted(df["club"].unique())

club_data = {}

for club in clubs:
    club_data[club] = df[df["club"] == club]
print(club_data)

teams_countries = {}


