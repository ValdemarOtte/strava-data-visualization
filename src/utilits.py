### Imports
# Standard library
from pathlib import Path
import os

# Third-party libraries

# Local files


def files_from_directory(path: Path) -> list[Path]:
    """
    Get relative paths for all files from a direcetory.

    :param Path path: Path to directory.
    :return list[str]: A list of relative paths for all the files in the directory.
    """
    return [Path(path / file) for file in os.listdir(path)]