import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.config import DATA_DIRECTORY
from src import utils

def get_last_ended_action(group):
	"""Return the enforcement action with the most recent VIOL_END_DATE"""
	return group.sort_values(by='VIOL_END_DATE', na_position='first', ascending=False).iloc[0]

def get_active_violations(DATA_DIRECTORY):
	"""Load the hr2w data, dedupe the data, return only active violation water systems, save table in output"""
	df = pd.read_csv(DATA_DIRECTORY / 'interim' / 'hr2w_exceedance.csv')
	groups = df.groupby(['WATER_SYSTEM_NUMBER', 'ANALYTE_NAME'])
	last_ended_action = groups.apply(get_last_ended_action)
	active_violations = last_ended_action[last_ended_action.ENF_ACTION_TYPE_ISSUED != 'RETURN TO COMPLIANCE']
	active_violations.reset_index(drop=True, inplace=True)
	return active_violations

def get_population_affected(active_violations):
	"""Return the total number of population effected by the active violations"""
	return active_violations.drop_duplicates(subset=['WATER_SYSTEM_NUMBER']).POPULATION.sum()

def get_analytes_OOC_violations(active_violations):
	"""Return the number of analytes out of compliance for all water systems"""
	return active_violations.groupby('WATER_SYSTEM_NUMBER').apply(lambda x: len(x)).sort_values(ascending=False)

def main(DATA_DIRECTORY):
	"""Main will have to connect to the dashboard to return results directly into the dashboard"""
	active_violations = get_active_violations(DATA_DIRECTORY)
	population = get_population_affected(active_violations)
	ooc_violations = get_analytes_OOC_violations(active_violations)
	save_output(active_violations, population, ooc_violations)
	return active_violations, population, ooc_violations

def save_output(active_violations, population, ooc_violations):
	active_violations.to_csv(DATA_DIRECTORY / 'output' / 'active_violations.csv', index=False)
	print(f"{utils.millify(population)} people affected")
	fig, ax = plt.subplots();
	ooc_violations.hist(bins=np.arange(1, max(ooc_violations) + 1, 1));
	ax.set_xlabel('Number of analytes out of compliance');
	ax.set_ylabel('Number of water systems');
	fig.savefig(DATA_DIRECTORY / 'output' / 'ooc_violations.png')
	return

if __name__ == '__main__':
	main(DATA_DIRECTORY)