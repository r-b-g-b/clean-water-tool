import io
import json
from pathlib import Path
import math
import shapefile
import shapefile
import tempfile
import zipfile

millnames = ["", " thousand", " million", " billion", " trillion"]


def convert_shp_to_geojson(input_path, output_path):
    """Convert a shapefile to geojson

    Parameters
    ----------
    input_path : str or file stream
    output_path : str
    """
    zfile = zipfile.ZipFile(input_path)

    temp_directory = tempfile.TemporaryDirectory()
    zfile.extractall(temp_directory.name)

    shp_filename = [
        p.filename for p in zfile.infolist() if p.filename.endswith(".shp")
    ][0]

    reader = shapefile.Reader(str(Path(temp_directory.name) / shp_filename))
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

    temp_directory.cleanup()

    # write the GeoJSON file
    with open(output_path, "w") as f:
        f.write(
            json.dumps({"type": "FeatureCollection", "features": features}, indent=2)
            + "\n"
        )


def millify(n):
    """Human-readable large numbers

    Reference
    ---------
    https://stackoverflow.com/questions/3154460/python-human-readable-large-numbers

    """
    n = float(n)
    millidx = max(
        0,
        min(
            len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))
        ),
    )

    return "{:.0f}{}".format(n / 10 ** (3 * millidx), millnames[millidx])
