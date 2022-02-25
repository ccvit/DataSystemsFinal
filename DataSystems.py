# Charles Cvitkovich

# pip install requests
import requests

# pip install pandas
import pandas as pd

import json

# pip install scipy (needed this for the Kernel Density Chart)
import scipy
import matplotlib.pyplot as plt

# We are contacting the Riot API to get the relevant information
# The documentation for this API can be found here: https://developer.riotgames.com/apis

# api_key is our auth code for the Riot Api for League of Legends.
# because this project can get its data in real time, we will also include a csv file with the match history we used for
# our analysis

# This will not work without an api_key. I am not including one because it is a security risk 
# for both Riot and me if I was to keep it in.
# Despite this not longor working because of the api_key, I am keeping it in regardless
# api_key = ""
# 
# # Get account ids for the user jmblake4. His account will have the information for this project
# account = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/jmblake4?api_key=" + api_key)
# 
# # get the puuid from results
# result_in_json = account.json()
# puuid = result_in_json['puuid']
# 
# # get match ids to get information
# matchIds = requests.get('https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids?api_key=' + api_key)
# match_ids_list = matchIds.json()
# 
# # get match info from match ids and parse through the data to get the required information
# match_data_list = []
# for matchId in match_ids_list:
#     match = requests.get('https://americas.api.riotgames.com/lol/match/v5/matches/' + matchId + '?api_key=' + api_key)
#     match_json = match.json()
# 
#     # There is an extremely large amount of data in each json, so I am just going to pull out the most important information
#     champion = ""
#     championLevel = ""
#     lane = ""
#     kills = 0
#     deaths = 0
#     won = False
#     goldEarned = 0
# 
#     match_info = match_json['info']['participants']
#     participants = match_json['metadata']['participants']
#     i = 0
#     for participant in participants:
#         if participant == puuid:
#             champion = match_info[i]['championName']
#             championLevel = match_info[i]['champLevel']
#             lane = match_info[i]['lane']
#             kills = match_info[i]['kills']
#             deaths = match_info[i]['deaths']
#             won = match_info[i]['win']
#             goldEarned = match_info[i]['goldEarned']
# 
#             matchData = {
#                 "matchId": matchId,
#                 "champion": champion,
#                 "championLevel": championLevel,
#                 "lane": lane, "kills": kills,
#                 "deaths": deaths,
#                 "won": won,
#                 "goldEarned": goldEarned
#             }
# 
#             match_data_list.append(matchData)
#             break
#         i = i + 1
# 
# match_data = json.dumps(match_data_list)
# df = pd.json_normalize(match_data_list)

# make sure to have the matchData in the same directory when running.
df = pd.read_csv("matchData.csv") 

# 1. histogram. Not many different levels, but this will show which levels are most common.
#  (have plt.show after each because they were not coming up for me without doing this. just
#  uncomment them if the same happens to you.)
# close the chart to continue to the next

df["championLevel"].hist()
plt.show()

# 2. Scatter plot. Shows that as kills increase, the amount of gold a player gets will also increase
df.plot.scatter(x='kills', y='goldEarned')
plt.show()

# 3. pie chart shows the user's win/lose ratio for the past 20 games
wins = df['won'].values.sum()
looses = (~df['won']).values.sum()
df_series = pd.Series([wins, looses], index=['Won', 'Lost'], name='Win/lose ratio')
df_series.plot.pie()
plt.show()

# 4. Kernel Density Chart. Shows the average gold earned as the character 'Riven'.
kdc = df.loc[df['champion'] == "Riven"]
kdc["goldEarned"].plot.kde()
plt.show()

# adding k/d ratio from kills and deaths in each match
df['k/d ratio'] = df['kills'] / df['deaths']

# adding average gold per level
df['avg gold per level'] = df['goldEarned'] / df['championLevel']

# how many times was Riven played?
Riven = len(df[df['champion'] == 'Riven'])
print("User played Riven " + str(Riven) + " times.")

# how many wins did the player have on Riven?
Riven = len(df[df['won']])
print("With Riven, the user won " + str(Riven) + " times.")

# what was the largest amount of gold gained in a game?
most_gold = df['goldEarned'].max()
print("The most gold gained was " + str(most_gold) + ".")

# what was the smallest amount of gold gained in a win?
least_gold = df.loc[df['won']]
least_gold = least_gold['goldEarned'].min()
print("The least amount of gold gained in a win was " + str(least_gold) + ".")

# which game had the lowest level Orianna?
game = df.loc[df['champion'] == 'Orianna']
game = game[game['championLevel'].min() == game['championLevel']]
print("The game with the lowest level Orianna was " + game['matchId'].to_string() + ".")

# which champion had the lowest k/d? (print out as data frame with champion and kd only).
lowest_kd = df.loc[df['k/d ratio'].min() == df['k/d ratio']]
print(lowest_kd[['champion', 'k/d ratio']])

# which lane, besides top, was played the most?
most_played = df.loc[df['lane'] != 'TOP']
most_played = most_played['lane'].mode()
print(most_played)

# how many unique champions were played? List them
unique_champions = df['champion'].nunique()
print("there were " + str(unique_champions) + " unique champions")
print(df['champion'].unique())

# Using correlation to show the relationship between gold earned and the level of the champion
# source: https://realpython.com/numpy-scipy-pandas-correlation-python/#example-pandas-correlation-calculation
gold_series = df['goldEarned']
level_series = df['championLevel']

# Pearson's r
print("Pearson's: " + str(gold_series.corr(level_series)))

# Spearman's rho
print("Spearman's: " + str(gold_series.corr(level_series, method='spearman')))

# Kendall's tau
print("Kendall's: " + str(gold_series.corr(level_series, method='kendall')))

# Correlation between deaths and kills. Pearson's only
print("Correlation between kills and deaths: " + str(df['deaths'].corr(df['kills'])))

# Correlation between gold earned and deaths
print("Correlation between gold earned and deaths: " + str(df['goldEarned'].corr(df['deaths'])))

# Correlation between levels and kills
print("Correlation between levels and kills: " + str(df['championLevel'].corr(df['kills'])))

# Correlation between levels and deaths
print("Correlation between levels and deaths: " + str(df['championLevel'].corr(df['deaths'])))

# Correlation between kills and gold earned
print("Correlation between kills and gold earned: " + str(df['kills'].corr(df['goldEarned'])))
