import os
import pandas as pd
from mapboxgl.utils import create_color_stops, df_to_geojson
from mapboxgl.viz import CircleViz
import dotenv
import geopandas
import pandas as pd
from src.config import DATA_DIRECTORY


_ = dotenv.load_dotenv(dotenv.find_dotenv())

token = os.getenv("MAPBOX_ACCESS_TOKEN")


def load_violations():
    violations = pd.read_csv(DATA_DIRECTORY / "interim" / "hr2w_exceedance.csv")
    return violations[
        [
            "WATER_SYSTEM_NUMBER",
            "WATER_SYSTEM_NAME",
            "VIOLATION_NUMBER",
            "VIOLATION_TYPE_NAME",
            "ANALYTE_NAME",
            "RESULT",
            "MCL",
            "VIOL_BEGIN_DATE",
            "VIOL_END_DATE",
            "ENF_ACTION_NUMBER",
            "ENF_ACTION_TYPE_ISSUED",
        ]
    ]


def deduplicate_violations(violations):
    def get_last_ended_action(group):
        """Return the enforcement action with the most recent VIOL_END_DATE"""
        return group.sort_values(
            by="VIOL_END_DATE", na_position="first", ascending=False
        ).iloc[0]

    groups = violations.groupby(["WATER_SYSTEM_NUMBER", "ANALYTE_NAME"])
    last_ended_action = groups.apply(get_last_ended_action)

    active_violations = last_ended_action[
        last_ended_action.ENF_ACTION_TYPE_ISSUED != "RETURN TO COMPLIANCE"
    ]
    active_violations.reset_index(drop=True, inplace=True)
    return active_violations


def load_water_system_locations():

    locations = geopandas.read_file(
        DATA_DIRECTORY / "interim" / "water_system_latlon.geojson"
    )
    locations["POPULATION"] = locations.POPULATION.astype(int)
    locations.rename(columns={"WATER_SYST": "WATER_SYSTEM_NUMBER"}, inplace=True)
    locations.set_index("WATER_SYSTEM_NUMBER", inplace=True)

    return locations


def make_mapbox_view(violations):
    data = df_to_geojson(
        violations,
        filename="points.geojson",
        properties=["ANALYTE_NAME", "POPULATION"],
        lat="lat",
        lon="lon",
        precision=3,
    )
    color_breaks = [0, 10, 100, 1000]
    color_stops = create_color_stops(color_breaks, colors="YlGnBu")

    viz = CircleViz(
        data,
        access_token=token,
        width="600px",
        height="800px",
        radius=5,
        color_property="POPULATION",
        color_stops=color_stops,
        center=(violations.lon.median(), violations.lat.median()),
        zoom=5,
    )

    viz.create_html("points.html")


def main():
    violations = load_violations()
    active_violations = deduplicate_violations(violations)
    locations = load_water_system_locations()

    active_violations = active_violations.join(
        locations, on="WATER_SYSTEM_NUMBER", how="inner"
    )
    active_violations = geopandas.GeoDataFrame(active_violations)
    active_violations["lon"], active_violations["lat"] = zip(
        *[point.coords[0] for point in active_violations.geometry]
    )

    make_mapbox_view(active_violations)


if __name__ == "__main__":
    main()
