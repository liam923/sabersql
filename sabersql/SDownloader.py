#!/usr/bin/env python

class SDownloader:
    """
    Manages Statcast downloads.
    """

    def __init__(self, path: str):
        """
        Initializes a SDownloader based on the path to the SaberSQL data
        :param path: the path to the folder for all SaberSQL data
        """
        self.path = path

    def download(self):
        pass