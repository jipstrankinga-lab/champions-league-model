import pandas as pd
import os
import matplotlib.pyplot as plt 

current_folder = os.path.dirname(__file__)
project_folder = os.path.dirname(current_folder)

csv_file = os.path.join(project_folder, "data", "Matches_clean.csv")

df = pd.read_csv(csv_file)

home = pd.DataFrame({
    "Team": df["HomeTeam"],
    "Opponent": df["AwayTeam"],
    "Goals": df["FTHome"],
    "OpponentElo": df["AwayElo"],
    "Home": 1
})

away = pd.DataFrame({
    "Team": df["AwayTeam"],
    "Opponent": df["HomeTeam"],
    "Goals": df["FTAway"],
    "OpponentElo": df["HomeElo"],
    "Home": 0
})



df_long = pd.concat([home, away], ignore_index=True)


df_long = df_long.dropna(subset=["OpponentElo"]) # Dropping the teams without Elo 




df_long["OpponentEloGroup"] = pd.cut(df_long["OpponentElo"],[0, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100], 
labels = ["1200", "1300", "1400", "1500", "1600", "1700", "1800", "1900","2000", "2100"])
print(df_long.head(20))
Q = df_long.groupby("OpponentEloGroup").size()
print(Q)
Home = df_long[df_long["Home"] == 1]
Away = df_long[df_long["Home"] == 0]
A = Home.groupby("OpponentEloGroup")["Goals"].mean()
B = Away.groupby("OpponentEloGroup")["Goals"].mean()
print(A)
print(B)
C = A -B 
print(C)

# Basevalue at 1700 Elo
Base_home = A["1700"]
Base_away = B["1700"]

# Elo-groups to tabels
Elo = A.index.astype(int)

# Predicted goals 
Predicted_home = Base_home - 0.07 * (Elo - 1700) / 100
Predicted_away = Base_away - 0.05 * (Elo - 1700) / 100

# One table to check
Results = pd.DataFrame({
    "Actual_home": A.values,
    "Predicted_home": Predicted_home,
    "Difference_home": A.values - Predicted_home,

    "Actual_away": B.values,
    "Predicted_away": Predicted_away,
    "Difference_away": B.values - Predicted_away
}, index=Elo)

print(Results)
# Is not really accurate but good enough to go on with the model 


# Graph (used AI to generate this)
#Home
plt.plot(Elo, A.values, label="Actual home")
plt.plot(Elo, Predicted_home, label="Predicted home")

plt.xlabel("Opponent Elo")
plt.ylabel("Goals")
plt.legend()
plt.show()
#Away
plt.plot(Elo, B.values, label="Actual away")
plt.plot(Elo, Predicted_away, label="Predicted away")

plt.xlabel("Opponent Elo")
plt.ylabel("Goals")
plt.legend()
plt.show()