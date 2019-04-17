import numpy as np
import pandas as pd
from src.config import DATA_DIRECTORY
from src import utils

def get_last_ended_action(group):
	"""Return the enforcement action with the most recent VIOL_END_DATE"""
	return group.sort_values(by='VIOL_END_DATE', na_position='first', ascending=False).iloc[0]

def main(DATA_DIRECTORY):
	"""Load the hr2w data, dedupe the data, return only active violation water systems, save table in output"""
	df = pd.read_csv(DATA_DIRECTORY / 'interim' / 'hr2w_exceedance.csv')
	groups = df.groupby(['WATER_SYSTEM_NUMBER', 'ANALYTE_NAME'])
	last_ended_action = groups.apply(get_last_ended_action)
	active_violations = last_ended_action[last_ended_action.ENF_ACTION_TYPE_ISSUED != 'RETURN TO COMPLIANCE']
	active_violations.reset_index(drop=True, inplace=True)
	active_violations.to_csv(DATA_DIRECTORY / 'output' / 'active_violations.csv', index=False)
	return active_violations

if __name__ == '__main__':
	main(DATA_DIRECTORY)
