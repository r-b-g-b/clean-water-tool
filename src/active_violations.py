import logging
import pandas as pd
from src.config import DATA_DIRECTORY
from src import utils

logger = logging.getLogger(__name__)


def get_last_ended_action(group):
    """Return the enforcement action with the most recent violation end date"""
    return group.sort_values(
        by="VIOL_END_DATE", na_position="first", ascending=False
    ).iloc[0]


def get_active_violations(violations):
    """Deduplicate violation data to only include active violations. Active violations are defined as water system/
    analyte combinations for the which the most recent action was any action other than "RETURN TO COMPLIANCE"

    Parameters
    ----------
    violations : pd.DataFrame

    Returns
    -------
    A pandas DataFrame of active violations
    """
    groups = violations.groupby(["WATER_SYSTEM_NUMBER", "ANALYTE_NAME"])
    last_ended_action = groups.apply(get_last_ended_action)
    active_violations = last_ended_action[
        last_ended_action.ENF_ACTION_TYPE_ISSUED != "RETURN TO COMPLIANCE"
    ]
    active_violations.reset_index(drop=True, inplace=True)
    return active_violations


def get_population_affected(active_violations):
    """Return the total number of population effected by the active violations"""
    return active_violations.drop_duplicates(
        subset=["WATER_SYSTEM_NUMBER"]
    ).POPULATION.sum()


def main():
    violations = pd.read_csv(DATA_DIRECTORY / "interim" / "hr2w_exceedance.csv")
    active_violations = get_active_violations(violations)
    population = get_population_affected(active_violations)
    logger.info("%d people affected", utils.millify(population))
    active_violations.to_csv(
        DATA_DIRECTORY / "processed" / "active_violations.csv", index=False
    )


if __name__ == "__main__":
    main()
