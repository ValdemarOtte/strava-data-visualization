### Imports
# Standard library
from datetime import datetime
from pathlib import Path
import os

# Third-party libraries
import geopy.distance
import gpxpy
import matplotlib.pyplot as plt

# Local files
from config import PLT_STYLE


def load_gpx_file(path: Path):
    data = []
    gpx = gpxpy.parse(path)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append([point.latitude, point.longitude, point.time])
    return data


def aa(data):
    values = []
    for a, b in zip(data[:-1], data[1:]):
        timee = b[2] - a[2]
        coords_1 = (b[0], b[1])
        coords_2 = (a[0], a[1])
        a = geopy.distance.geodesic(coords_1, coords_2).m
        if a != 0:
            values.append([timee, a])
    return values


def b(data):
    data_ = []
    time_now = datetime.now()
    time_now_ = datetime.now()
    s = 0
    for d in data:
        s += d[1]
        time_now += d[0]
        #data_.append([time_now - time_now_, round(s, 3)])
        data_.append([time_now - time_now_, d[1]])
    return data_


def calculate_pace(data, distance: int = 1_000) -> list[float]:
    times = []
    distance_ran = 0
    for d in data:
        distance_ran += d[1]
        if distance_ran >= distance:
            distance_ran = 0
            times.append(d[0])

    # `times` are a list of the time from the start of the run and each distance (e.g. 1km, 2km , ...). 
    # To get the pace of each distance we can divide each element in the list with it's number in the sequence.
    # We add one to `i`, because enumerate starts counting from zero.
    return [(time / (i+1)).total_seconds() for i, time in enumerate(times)]


def create_x_axis(data: list[dict]) -> list[float]:
    x: list[float] = []
    for i, element in enumerate(data):
        x.extend([(i+1)]*len(element["paces"]))
    return x


def create_y_axis(data: list[dict]) -> list[float]:
    y: list[float] = []
    for element in data:
        y.extend(element["paces"])
    return y


def files_from_directory(path: Path) -> list[Path]:
    """
    Get relative paths for all files from a direcetory.

    :param Path path: Path to directory.
    :return list[str]: A list of relative paths for all the files in the directory.
    """
    return [Path(path / file) for file in os.listdir(path)]



def main():
    path = Path("data")
    files = files_from_directory(path)


    aaa = []

    

    for file in files:
        gpx_file = open(file, "r")
        data = load_gpx_file(gpx_file)
        aaaa = {"date": data[0][2].date()}
        data = aa(data)
        data = b(data)
        paces = calculate_pace(data)
        aaaa["paces"] = paces
        aaa.append(aaaa)

    sorted_data = sorted(aaa, key=lambda d: d["date"])
    x = create_x_axis(sorted_data)
    y = create_y_axis(sorted_data)  
    print(x)
    print(y)


if __name__ == "__main__":
    main()
