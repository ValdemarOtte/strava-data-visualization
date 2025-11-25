### Imports
# Standard library
from datetime import datetime
from pathlib import Path

# Third-party libraries
import geopy.distance
import gpxpy

# Local files
from utilits import files_from_directory
from plots import plot_paces_for_each_run


def load_gpx_file(path: Path) -> list[float, float, datetime]:
    data: list[float, float, datetime] = []
    gpx = gpxpy.parse(path)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                data.append([point.latitude, point.longitude, point.time])
    return data


def transform_gpx_data(points):
    sequence: list[float, float] = []
    for point_1, point_2 in zip(points[:-1], points[1:]):
        # point_i[2] is time. 
        time_travelled = (point_2[2] - point_1[2]).total_seconds()
        # point_i[0] is latitude and point_i[1] is longitude. 
        # We used meters (m).
        distance_travelled = geopy.distance.geodesic(
            (point_1[0], point_1[1]), 
            (point_2[0], point_2[1])
        ).m
        # We skip the data points where the distance travelled is zero to get a better pace.
        if distance_travelled != 0:
            sequence.append([time_travelled, distance_travelled])
    return sequence


def calculate_pace(data, distance: int = 1_000) -> list[float]:
    times: list[float] = []
    time: float = 0
    distance_ran: float = 0
    for element in data:
        distance_ran += element[1]
        time += element[0]
        if distance_ran >= distance:
            times.append(time)
            distance_ran = 0
            time = 0
    if distance_ran > 0:
        times.append(time * (distance / distance_ran))
    return times


def pace_for_run(path_to_gpx_file: Path):
    gpx_file = open(path_to_gpx_file, "r")
    points = load_gpx_file(gpx_file)
    data = {"date": points[0][2].date()}
    sequence = transform_gpx_data(points)
    paces = calculate_pace(sequence)
    data["paces"] = paces
    return data


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

    plot_paces_for_each_run(data)


if __name__ == "__main__":
    main()
