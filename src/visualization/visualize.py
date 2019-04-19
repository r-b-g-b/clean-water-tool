import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.config import DATA_DIRECTORY


def plot_num_analytes_per_water_system():
    active_violations = pd.read_csv(
        DATA_DIRECTORY / "processed" / "active_violations.csv"
    )

    num_analytes_per_water_system = (
        active_violations.groupby("WATER_SYSTEM_NUMBER")
        .apply(lambda x: len(x))
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots()
    num_analytes_per_water_system.hist(
        bins=np.arange(1, max(num_analytes_per_water_system) + 1, 1)
    )
    ax.set_xlabel("Number of analytes out of compliance")
    ax.set_ylabel("Number of water systems")
    fig.savefig(DATA_DIRECTORY / "processed" / "num_analytes_per_water_system.png")


def main():
    plot_num_analytes_per_water_system()


if __name__ == "__main__":
    main()
