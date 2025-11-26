### Imports
# Standard library

# Third-party libraries
import matplotlib.pyplot as plt

# Local files
from config import PLT_STYLE


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


def plot_paces_for_each_run(data):
    x = create_x_axis(data)
    y = create_y_axis(data)  
    print(x)
    print(y)