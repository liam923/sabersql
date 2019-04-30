#!/usr/bin/env python3

import os
from Utilities import _download


class PDownloader:
    """
    Manages people downloads.
    """

    def __init__(self, path):
        """
        Initializes a PDownloader based on the path to the SaberSQL data

        :param path: the path to the folder for all SaberSQL data
        """
        self._path = path

    def download(self, handler=lambda *args: None):
        """
        Downloads people file

        :param handler: a function that takes in a double, representing the completion percentage of the download
        """

        handler(0)
        source_url = "https://github.com/chadwickbureau/register/raw/master/data/people.csv"
        destination = os.path.join(self._path, "Person/people.csv")
        _download(source_url, destination, True)
        handler(1)
