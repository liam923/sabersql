#!/usr/bin/env python3

import os
from . import Utilities


class ProgressHandler:

    STARTED = "started"
    FINISHED = "finished"
    NONE = "none"

    def __init__(self, folder):
        """
        Tracks progress made on process files within a folder.

        :param folder: the folder to track progress on
        """
        self._folder = folder

    def get_progress(self):
        """
        Determines the progress so far on processing the folder.

        :return:
        """

        try:
            with open(os.path.join(self._folder, "progress.dat")) as f:
                return f.readline().replace("\n", "")
        except FileNotFoundError:
            return ProgressHandler.NONE

    def start_progress(self):
        """
        Tells the handler that progress has begun on processing the folder.
        """

        self.__write_message(ProgressHandler.STARTED)

    def end_progress(self):
        """
        Tells the handler that progress has ended on processing the folder.
        """

        self.__write_message(ProgressHandler.FINISHED)

    def __write_message(self, message):
        progress_file_path = os.path.join(self._folder, "progress.dat")
        Utilities._shell("echo \"%s\" > \"%s\"" % (message, progress_file_path))
