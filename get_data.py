from crawler import Crawler
import pandas as pd
import gc

crawler = Crawler()

matchups = pd.read_csv('data/nba_odds_data.csv')

dfs = []
n = 0
for i, row in enumerate(matchups.values):
	j, season, date, odds, winner, loser, outcome, point_diff = row
	dfs.append(crawler.get_matchup(season, odds, outcome, date, winner, loser))
	print(f"\rMatchup: {i}")
	if (i+1) % 42 == 0:
		df = pd.concat(dfs)
		df.reset_index(drop=True).to_csv(f"data/matchups/output_{n}.csv")
		df.iloc[0:0]
		n = n + 1
		dfs = []
		# https://stackify.com/python-garbage-collection/
		gc.collect()

# Get the last little bit
df = pd.concat(dfs)
df.reset_index(drop=True).to_csv(f"data/matchups/output_{n}.csv")