#!/usr/bin/env python3

import os
from datetime import datetime
from .Utilities import _download


class RDownloader:
    """
    Manages Retrosheet downloads.
    """

    def __init__(self, path):
        """
        Initializes a RDownloader based on the path to the SaberSQL data

        :param path: the path to the folder for all SaberSQL data
        """
        self._path = path

    def download(self, year=None, handler=lambda *args: None):
        """
        Downloads Retrosheet files

        :param year: the year to be downloaded; defaults to all years 1903 to present
        :param handler: a function that takes in a double, representing the completion percentage of the download
        """

        if year:
            years = [year]
        else:
            years = [y for y in range(1903, datetime.now().year + 1)]
        paths = self.__download_paths(years)

        handler(0, status="Downloading Retrosheet data")
        for i in range(0, len(paths)):
            _download(paths[i][0], paths[i][1], unzip=paths[i][2])
            handler((i + 1) / len(paths), status="Downloading Retrosheet data for %s" % paths[i][3])

    def __download_paths(self, years):
        """Gets all urls to download and paths to download them to"""

        paths = []
        for year in years:
            for type in ["eve", "as", "post"]:
                url = "https://www.retrosheet.org/events/%s%s.zip" % (year, type)
                path = os.path.join(self._path, "Retrosheet/raw_event_files/%s/%s%s.zip" % (year, year, type))
                folder = os.path.join(self._path, "Retrosheet/raw_event_files/%s/%s%s" % (year, year, type))
                paths.append((url, path, folder, year))
        return paths
