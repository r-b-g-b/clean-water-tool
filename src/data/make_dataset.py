# -*- coding: utf-8 -*-
import click
import io
import logging
import pandas as pd
import requests
import os

from src.config import (
    DATA_DIRECTORY,
    HR2W_EXCEEDANCE_URL,
    HR2W_RETURN_TO_COMPLIANCE_URL,
    TULARE_LAKE_BASIN_SHP_PATH,
    WATER_SYSTEM_LOCATIONS_URL,
)
from src import utils


def make_hr2w_data():
    data = requests.get(HR2W_EXCEEDANCE_URL)

    if not os.path.exists(DATA_DIRECTORY / "raw"):
        os.makedirs(DATA_DIRECTORY / "raw")
    if not os.path.exists(DATA_DIRECTORY / "interim"):
        os.makedirs(DATA_DIRECTORY / "interim")

    with open(DATA_DIRECTORY / "raw" / "hr2w_exceedance.xlsx", "wb") as f:
        f.write(data.content)

    data = requests.get(HR2W_RETURN_TO_COMPLIANCE_URL)

    with open(DATA_DIRECTORY / "raw" / "hr2w_return_to_compliance.xlsx", "wb") as f:
        f.write(data.content)

    df = pd.read_excel(DATA_DIRECTORY / "raw" / "hr2w_exceedance.xlsx")
    df.to_csv(DATA_DIRECTORY / "interim" / "hr2w_exceedance.csv", index=False)

    df = pd.read_excel(DATA_DIRECTORY / "raw" / "hr2w_return_to_compliance.xlsx")
    df.to_csv(DATA_DIRECTORY / "interim" / "hr2w_return_to_compliance.csv", index=False)


def make_water_system_locations():
    # from https://stackoverflow.com/questions/43119040/shapefile-into-geojson-conversion-python-3
    data = requests.get(WATER_SYSTEM_LOCATIONS_URL)

    output_path = DATA_DIRECTORY / "interim" / "water_system_locations.geojson"
    utils.convert_shp_to_geojson(io.BytesIO(data.content), output_path)


def make_tulare_lake_basin_location():
    output_path = DATA_DIRECTORY / "interim" / "tulare_lake_basin.geojson"
    utils.convert_shp_to_geojson(TULARE_LAKE_BASIN_SHP_PATH, output_path)


@click.command()
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)

    logger.info("making hr2w dataset")
    make_hr2w_data()

    logger.info("making water system location dataset")
    make_water_system_locations()

    logger.info("making Tulare Lake Basin location")
    make_tulare_lake_basin_location()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    main()
