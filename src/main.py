import gpxpy
import matplotlib.pyplot as plt
import geopy.distance
from pathlib import Path
from datetime import datetime


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
        a = geopy.distance.geodesic(coords_1, coords_2).km
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


def main():
    p = []
    for i in ["1", "2", "3"]:
        gpx_file = open(f"data\\{i}.gpx", 'r')
        data = load_gpx_file(gpx_file)
        data = aa(data)
        data = b(data)
        
        s = 0
        times = []
        for d in data:
            s += d[1]
            if s >= 1:
                s = 0
                times.append(d[0])
        
        lst = []
        for i, time in enumerate(times):
            value =(time / (i+1)).total_seconds()
            lst.append((time / (i+1)).total_seconds())
            p.append(value)
        print(len(lst))
    
    x = [1]*14
    x.extend([2]*21)
    x.extend([3]*8)
    
    plt.plot(x, p, 'o')
    plt.show()

if __name__ == "__main__":
    main()
