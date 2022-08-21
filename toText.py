import pandas as pd
import numpy as np

file = r"running_score.csv"

d = {'r':[0], 'b': [0]}
df = pd.DataFrame(d)
df.to_csv(file)

def get_wins():
	df = pd.read_csv(file)
	print(df)
	rwins = np.array(df['r'])[-1]
	bwins = np.array(df['b'])[-1]
	return rwins, bwins

def update_wins(rwins, bwins):
	df = pd.read_csv(file)
	df.append(pd.DataFrame([rwins, bwins], columns = ['r', 'b']))
	df.to_csv(file)

rwins, bwins = get_wins()
print(f'rwins:{rwins}, bwins:{bwins}')

rwins = 2
bwins = 3

update_wins(rwins, bwins)