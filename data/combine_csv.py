from zipfile import ZipFile
import os
import pandas as pd

extension = 'csv'
files = []

with ZipFile('matchups.zip', 'r') as zipObj:
	fnames = zipObj.namelist()
	for name in fnames:
		if name.endswith(extension):
			f = zipObj.open(name, 'r')
			files.append(pd.read_csv(f, index_col=0))

pd.concat(files, ignore_index=True).to_csv("test_data.csv", encoding='utf-8-sig')