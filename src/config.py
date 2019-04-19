from pathlib import Path


DATA_DIRECTORY = (Path(__file__).parents[1] / "data").resolve()

HR2W_EXCEEDANCE_URL = "https://www.waterboards.ca.gov/water_issues/programs/hr2w/docs/data/hr2w_web_data_active_2-2019.xlsx"
HR2W_RETURN_TO_COMPLIANCE_URL = "https://www.waterboards.ca.gov/water_issues/programs/hr2w/docs/data/hr2w_web_data_rtc_2-2019.xlsx"
WATER_SYSTEM_LOCATIONS_URL = "https://www.waterboards.ca.gov/water_issues/programs/hr2w/docs/data/ec_summary_feb2019.zip"
TULARE_LAKE_BASIN_SHP_PATH = DATA_DIRECTORY / "raw" / "TLB_HUC06_TulareLakeBasin.zip"
