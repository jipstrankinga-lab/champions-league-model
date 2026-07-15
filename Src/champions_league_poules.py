import math
import numpy as np 
import pandas as pd
import os
current_folder = os.path.dirname(__file__)
csv_file = os.path.join(current_folder, "Champions_league_2015_2026.csv")
csv_file = os.path.join(current_folder, "Clubspercountry.csv")

df = pd.read_csv(csv_file)


