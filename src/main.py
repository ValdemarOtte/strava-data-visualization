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
from utilits import files_from_directory


def load_gpx_file(path: Path) -> list[float, float, datetime]:
    data: list[float, float, datetime] = []
    gpx = gpxpy.parse(path)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append([point.latitude, point.longitude, point.time])
    return data


def aa(points):
    data = []
    for point_1, point_2 in zip(points[:-1], points[1:]):
        # point_i[2] is time. 
        time_travelled = point_2[2] - point_1[2]
        # point_i[0] is latitude and point_i[1] is longitude. 
        # We used meters (m).
        distance_travelled = geopy.distance.geodesic(
            (point_1[0], point_1[1]), 
            (point_2[0], point_2[1])
        ).m
        # We skip the data points where the distance travelled is zero to get a better pace.
        if distance_travelled != 0:
            data.append([time_travelled, distance_travelled])
    return data


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
        # TODO Add the lasted time, because the run has ended.
        # Used the formular: time = time * (distance / distance_ran)

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


def pace_for_run(path_to_gpx_file: Path):
    gpx_file = open(path_to_gpx_file, "r")
    data = load_gpx_file(gpx_file)
    aaaa = {"date": data[0][2].date()}
    data = aa(data)
    data = b(data)
    paces = calculate_pace(data)
    aaaa["paces"] = paces
    return aaaa


def pace_for_all_run(path_to_gpxs: Path):
    path_to_gpx_files = files_from_directory(path_to_gpxs)
    data = []
    for path_to_gpx_file in path_to_gpx_files:
        data.append(pace_for_run(path_to_gpx_file))
    return data


def main():
    path = Path("data")
    data = pace_for_all_run(path)

    sorted_data = sorted(data, key=lambda d: d["date"])
    a = []
    for d in sorted_data:
        a.append({
            "date": d["date"],
            "paces": [sum(d["paces"])/len(d["paces"])]
        })

    x = create_x_axis(a)
    y = create_y_axis(a)  
    print(x)
    print(y)


if __name__ == "__main__":
    main()
