#!/usr/bin/env python3

import os
from datetime import datetime
from .Utilities import _download


class SDownloader:
    """
    Manages Statcast downloads.
    """

    def __init__(self, path):
        """
        Initializes a SDownloader based on the path to the SaberSQL data

        :param path: the path to the folder for all SaberSQL data
        """
        self._path = path

    def download(self, year=None, handler=lambda *args: None):
        """
        Downloads BaseballSavant files

        :param year: the year to be downloaded; defaults to all years 1999 to present
        :param handler: a function that takes in a double, representing the completion percentage of the download
        """

        if year:
            years = [year]
        else:
            years = [y for y in range(1999, datetime.now().year + 1)]
        paths = self.__download_paths(years)
        handler(0, status="Downloading Statcast data")
        for i in range(0, len(paths)):
            _download(*paths[i])
            handler((i + 1) / len(paths), status="Downloading Statcast data")

    def __download_paths(self, years):
        """Gets all urls to download and paths to download them to"""

        paths = []
        for year in years:
            for inning in range(1, 11):
                for outs in range(0, 3):
                    url = ("https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&s"
                           "tadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=") + str(year) +\
                          "%7C&hfSit=&player_type=pitcher&hfOuts=" + str(outs) +\
                          ("%7C&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfInfield=&t"
                            "eam=&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfPull=&metric_1=&hfInn=") +\
                          str(inning) + ("%7C&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_s"
                                         "ort=h_launch_speed&sort_order=desc&min_pas=0&chk_inning=on&chk_outs=on&type=d"
                                         "etails&")
                    path = os.path.join(self._path, "BaseballSavant/%s/%s_%s.csv" % (year, inning, outs))
                    paths.append((url, path))
        return paths
