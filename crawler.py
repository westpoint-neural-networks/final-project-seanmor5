from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from urllib.parse import quote
import pandas as pd

EXE_PATH=r'/mnt/c/webdrivers/chromedriver.exe'

class Crawler:

	def __init__(self):
		self.options = Options()
		self.browser = webdriver.Chrome(chrome_options=self.options, executable_path=EXE_PATH)

	def make_url(self, stats, season, team, date_from, date_to):
		date_to = quote(date_to, safe='')
		date_from = quote(date_from, safe='')
		url = f'https://stats.nba.com/teams/{stats}/?sort=W_PCT&dir=-1&Season={season}&SeasonType=Regular&DateFrom={date_from}&DateTo={date_to}&TeamID={team}'
		return url

	def scrape_table(self, stats, season, team, date):
		date_from = '10/01/'+season[0:4]
		url = self.make_url(stats, season, team, date_from, date)
		self.browser.get(url)
		# https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
		delay = 10
		try:
			element = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'nba-stat-table__overflow')))
			# https://stackoverflow.com/questions/7263824/get-html-source-of-webelement-in-selenium-webdriver-using-python
			soup = BeautifulSoup(element.get_attribute('innerHTML'), 'html.parser')
			# https://stackoverflow.com/questions/18966368/python-beautifulsoup-scrape-tables
			tds = soup.find_all('td')
			new_tds = []
			for td in tds:
				new_tds.append(td.text.replace(' ', '').replace('\n', ''))
			return new_tds
		except TimeoutException:
			print("Loading took too much time! Retrying")
			# Only thing that worked was restarting and starting the browser again
			self.browser.quit()
			self.browser = webdriver.Chrome(chrome_options=self.options, executable_path=EXE_PATH)
			return self.scrape_table(stats, season, team, date)

	def get_traditional_stats(self, season, team, date):
		tds = self.scrape_table('traditional', season, team, date)
		df = pd.DataFrame()
		df['WINS'] = [tds[3]]
		df['LOSSES'] = [tds[4]]
		df['WIN%'] = [tds[5]]
		df['PTS'] = [tds[7]]
		df['FGM'] = [tds[8]]
		df['FGA'] = [tds[9]]
		df['FG%'] = [tds[10]]
		df['3PM'] = [tds[11]]
		df['3PA'] = [tds[12]]
		df['3P%'] = [tds[13]]
		df['FTM'] = [tds[14]]
		df['FTA'] = [tds[15]]
		df['FT%'] = [tds[16]]
		df['OREB'] = [tds[17]]
		df['DREB'] = [tds[18]]
		df['AST'] = [tds[20]]
		df['TOV'] = [tds[21]]
		df['STL'] = [tds[22]]
		df['BLK'] = [tds[23]]
		df['BLKA'] = [tds[24]]
		df['PF'] = [tds[25]]
		df['PFD'] = [tds[26]]
		df['+/-'] = [tds[27]]
		return df

	def get_advanced_stats(self, season, team, date):
		tds = self.scrape_table('advanced', season, team, date)
		df = pd.DataFrame()
		df['OFFRTG'] = [tds[6]]
		df['DEFRTG'] = [tds[7]]
		df['NETRTG'] = [tds[8]]
		df['AST%'] = [tds[9]]
		df['AST/TO'] = [tds[10]]
		df['ASTRATIO'] = [tds[11]]
		df['OREB%'] = [tds[12]]
		df['DREB%'] = [tds[13]]
		df['REB%'] = [tds[14]]
		df['TOV%'] = [tds[15]]
		df['EFG%'] = [tds[16]]
		df['TS%'] = [tds[17]]
		df['PACE'] = [tds[18]]
		df['PIE'] = [tds[19]]
		return df

	def get_four_factor_stats(self, season, team, date):
		tds = self.scrape_table('four-factors', season, team, date)
		df = pd.DataFrame()
		df['FTARATE'] = [tds[8]]
		df['OPPEFG%'] = [tds[11]]
		df['OPPFTARATE'] = [tds[12]]
		df['OPPTOV%'] = [tds[13]]
		df['OPPOREB%'] = [tds[14]]
		return df

	def get_misc_stats(self, season, team, date):
		tds = self.scrape_table('misc', season, team, date)
		df = pd.DataFrame()
		df['PTSOFFTO'] = [tds[6]]
		df['2NDPTS'] = [tds[7]]
		df['FBPS'] = [tds[8]]
		df['PITP'] = [tds[9]]
		df['OPPPTSOFFTO'] = [tds[10]]
		df['OPP2NDPTS'] = [tds[11]]
		df['OPPFBPS'] = [tds[12]]
		df['OPPPITP'] = [tds[13]]
		return df

	def get_scoring_stats(self, season, team, date):
		tds = self.scrape_table('scoring', season, team, date)
		df = pd.DataFrame()
		df['%FGA2PT'] = [tds[6]]
		df['%FGA3PT'] = [tds[7]]
		df['%PTS2PT'] = [tds[8]]
		df['%PTS2PT-MR'] = [tds[9]]
		df['%PTS3PT'] = [tds[10]]
		df['%PTSFBPS'] = [tds[11]]
		df['%PTSFT'] = [tds[12]]
		df['%PTSOFFTO'] = [tds[13]]
		df['%PTSPITP'] = [tds[14]]
		df['2FGM%AST'] = [tds[15]]
		df['2FGM%UAST'] = [tds[16]]
		df['3FGM%AST'] = [tds[17]]
		df['3FGM%UAST'] = [tds[18]]
		df['FGM%AST'] = [tds[19]]
		df['FGM%UAST'] = [tds[20]]
		return df

	def get_opposing_stats(self, season, team, date):
		tds = self.scrape_table('opponent', season, team, date)
		df = pd.DataFrame()
		df['OPPFGM'] = [tds[6]]
		df['OPPFGA'] = [tds[7]]
		df['OPPFG%'] = [tds[8]]
		df['OPP3PM'] = [tds[9]]
		df['OPP3PA'] = [tds[10]]
		df['OPP3P%'] = [tds[11]]
		df['OPPFTM'] = [tds[12]]
		df['OPPFTA'] = [tds[13]]
		df['OPPFT%'] = [tds[14]]
		df['OPPOREB'] = [tds[15]]
		df['OPPDREB'] = [tds[16]]
		df['OPPREB'] = [tds[17]]
		df['OPPAST'] = [tds[18]]
		df['OPPTOV'] = [tds[19]]
		df['OPPSTL'] = [tds[20]]
		df['OPPBLK'] = [tds[21]]
		df['OPPBLKA'] = [tds[22]]
		df['OPPPF'] = [tds[23]]
		df['OPPPFD'] = [tds[24]]
		df['OPPPTS'] = [tds[25]]
		df['OPP+/-'] = [tds[26]]
		return df

	def get_defense_stats(self, season, team, date):
		tds = self.scrape_table('defense', season, team, date)
		df = pd.DataFrame()
		df['OPPPTS2NDCHANCE'] = [tds[12]]
		df['OPPPTSFB'] = [tds[13]]
		df['OPPPTSPAINT'] = [tds[14]]
		return df

	def get_team(self, season, team, date):
		traditional = self.get_traditional_stats(season, team, date)
		advanced = self.get_advanced_stats(season, team, date)
		four_factors = self.get_four_factor_stats(season, team, date)
		misc = self.get_misc_stats(season, team, date)
		scoring = self.get_scoring_stats(season, team, date)
		opponent = self.get_opposing_stats(season, team, date)
		defense = self.get_defense_stats(season, team, date)
		return traditional.join([advanced, four_factors, misc, scoring, opponent, defense])

	def get_matchup(self, season, odds, outcome, date, winning_team, losing_team):
		df = pd.DataFrame()
		df['ODDS'] = [odds]
		df['OUTCOME'] = [outcome]
		w_team_df = self.get_team(season, winning_team, date)
		l_team_df = self.get_team(season, losing_team, date)
		team_df = w_team_df.join(l_team_df, lsuffix='_WINNER', rsuffix='_LOSER')
		return team_df.join(df)