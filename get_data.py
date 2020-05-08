from crawler import Crawler
import pandas as pd
import gc
import datetime

crawler = Crawler()

matchups = pd.read_csv('data/test_data.csv')

dfs = []
n = 0
for i, row in enumerate(matchups.values):
	season, date, winner, loser, odds, outcome = row
	new_date = datetime.datetime.strptime(date, '%m/%d/%Y')
	new_date = new_date - datetime.timedelta(days=1)
	new_date = new_date.strftime('%m/%d/%Y')
	dfs.append(crawler.get_matchup(season, odds, outcome, new_date, winner, loser))
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