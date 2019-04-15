# -*- coding: utf-8 -*-
import shapefile
from json import dumps
import urllib
from pathlib import Path
import io
import zipfile
import click
import logging
import pandas as pd
import requests
import os

from src.config import (
    DATA_DIRECTORY,
    HR2W_EXCEEDANCE_URL,
    HR2W_RETURN_TO_COMPLIANCE_URL,
    WATER_SYSTEM_LOCATIONS_URL,
)


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


def make_water_system_latlon():
    # from https://stackoverflow.com/questions/43119040/shapefile-into-geojson-conversion-python-3
    data = requests.get(WATER_SYSTEM_LOCATIONS_URL)
    zpfile = zipfile.ZipFile(io.BytesIO(data.content))

    output_directory = Path(
        DATA_DIRECTORY
        / "raw"
        / Path(urllib.parse.urlparse(WATER_SYSTEM_LOCATIONS_URL).path).stem
    )
    output_directory.mkdir(parents=True, exist_ok=True)

    zpfile.extractall(output_directory)

    shp_filename = [
        p.filename for p in zpfile.infolist() if p.filename.endswith(".shp")
    ][0]

    reader = shapefile.Reader(str(output_directory / shp_filename))
    fields = reader.fields[1:]

    field_names = [field[0] for field in fields]
    features = []
    for record in reader.shapeRecords():
        atr = dict(zip(field_names, record.record))
        features.append(
            {
                "type": "Feature",
                "geometry": record.shape.__geo_interface__,
                "properties": atr,
            }
        )

    # write the GeoJSON file
    with open(DATA_DIRECTORY / "interim" / "water_system_latlon.geojson", "w") as f:
        f.write(
            dumps({"type": "FeatureCollection", "features": features}, indent=2) + "\n"
        )


@click.command()
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)

    logger.info("making hr2w dataset")
    make_hr2w_data()

    logger.info("making water system latitude/longitude dataset")
    make_water_system_latlon()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    main()
