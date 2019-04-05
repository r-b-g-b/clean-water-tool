# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
import requests
import os

from src.config import (
    HR2W_EXCEEDANCE_URL, HR2W_RETURN_TO_COMPLIANCE_URL, DATA_DIRECTORY
)


@click.command()
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    data = requests.get(HR2W_EXCEEDANCE_URL)

    if not os.path.exists(DATA_DIRECTORY / 'raw'):
        os.makedirs(DATA_DIRECTORY / 'raw')
    if not os.path.exists(DATA_DIRECTORY / 'interim'):
        os.makedirs(DATA_DIRECTORY / 'interim')

    with open(DATA_DIRECTORY / 'raw' / 'hr2w_exceedance.xlsx', 'wb') as f:
        f.write(data.content)

    data = requests.get(HR2W_RETURN_TO_COMPLIANCE_URL)

    with open(DATA_DIRECTORY / 'raw' / 'hr2w_return_to_compliance.xlsx', 'wb') as f:
        f.write(data.content)

    df = pd.read_excel(DATA_DIRECTORY / 'raw' / 'hr2w_exceedance.xlsx')
    df.to_csv(DATA_DIRECTORY / 'interim' / 'hr2w_exceedance.csv')

    df = pd.read_excel(DATA_DIRECTORY / 'raw' / 'hr2w_return_to_compliance.xlsx')
    df.to_csv(DATA_DIRECTORY / 'interim' / 'hr2w_return_to_compliance.csv')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    main()
