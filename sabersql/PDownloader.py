#!/usr/bin/env python3

import os
from .Utilities import _download
from .Utilities import _shell


class PDownloader:
    """
    Manages player downloads.
    """

    def __init__(self, path):
        """
        Initializes a PDownloader based on the path to the SaberSQL data

        :param path: the path to the folder for all SaberSQL data
        """
        self._path = path

    def download(self, handler=lambda *args: None):
        """
        Downloads player file

        :param handler: a function that takes in a double, representing the completion percentage of the download
        """

        status = "Downloading people data"
        handler(0, status=status)
        source_url = "https://github.com/chadwickbureau/register/raw/master/data/people.csv"
        destination = os.path.join(self._path, "Person/people.csv")
        _download(source_url, destination)
        handler(1, status=status)

    def undownload(self, handler=lambda *args: None):
        """
        Undoes download of player file

        :param handler: a function that takes in a double, representing the completion percentage of the download undoing
        """

        status = "Undoing people download"
        handler(0, status=status)
        _shell("rm \"%s\"" % os.path.join(self._path, "Person/people.csv"))
        handler(1, status=status)
