#!/usr/bin/env python3

from datetime import datetime
import os
import Utilities
import math

class SImporter:

    def __init__(self, path, connection):
        """
        Initializes a SDownloader based on the path to the SaberSQL data and a MySQLConnection

        :param path: the path to the folder for all SaberSQL data
        :param connection: a MySQLConnection to the database to import data to
        """

        self._path = path
        self._connection = connection

    def import_statcast_data(self, year=None, handler=lambda *args: None):
        """
        Imports all downloaded BaseballSavant data to MySQL database

        :param year: the year to be imported; defaults to all years 1999 to present
        :param handler: a function that takes in a double, representing the completion percentage of the import
        :raises ConnectionError: if the connection fails
        """

        if year:
            years = [year]
        else:
            years = [y for y in range(1999, datetime.now().year + 1)]

        year_prog = 0
        for year in years:
            savant_path = os.path.join(self._path, "BaseballSavant", str(year))
            files = Utilities._shell("find \"%s\" -name \"*.csv\"" % savant_path)[0].split("\n")
            file_prog = 0
            for csv, started in self.__year_files(year):
                self.__start_progress(csv)
                if started:
                    self.__undo_progress(csv)
                self.__import_dataframe(Utilities._import_csv(csv))
                self.__end_progress(csv)

                file_prog += 1
                handler(((file_prog / len(files)) * (1 / len(years))) + (year_prog / len(years)))
            year_prog += 1
            handler(year_prog / len(years))

    def __import_dataframe(self, dataframe):
        """
        Imports data from dataframe to MySQL

        :param dataframe: the dataframe to import
        :raises ConnectionError: if the connection fails
        """

        def make_cell(cell):
            t = type(cell)
            if t is int or t is float:
                if math.isnan(cell):
                    return "NULL"
                else:
                    return str(cell)
            elif t is str:
                if cell == "null":
                    return "NULL"
                else:
                    return "\'" + cell.replace("\'", "\\\'") + "\'"
            else:
                raise TypeError("Unrecognized cell type: %s" % str(t))

        def make_row(row):
            for cell in row:
                yield make_cell(cell)

        def make_data(dataframe):
            for row in dataframe.values:
                yield make_row(row)

        self._connection.import_data("pitch", dataframe.columns, make_data(dataframe), batch_size=400)

    def __year_files(self, year):
        """
        Gets all the files in a year to be imported that haven't been to already

        :param year: the year to be imported
        :return: [(path to file, True iff file has been partially imported already)]
        """

        savant_path = os.path.join(self._path, "BaseballSavant", str(year))

        progress = {}
        progress_file_path = os.path.join(savant_path, "import_progress.dat")
        if os.path.isfile(progress_file_path):
            with open(progress_file_path) as progress_file:
                for line in progress_file:
                    arr = line.rstrip().split(" : ")
                    progress[arr[1]] = arr[0]

        files = []
        file_list = Utilities._shell("find \"%s\" -name \"*.csv\"" % savant_path)[0].split("\n")
        for csv in file_list:
            if csv:
                if csv in progress:
                    if progress[csv] == "started":
                        files.append((csv, True))
                else:
                    files.append((csv, False))

        return files

    def __start_progress(self, file):
        """
        Writes for the start of importing the file

        :param file: the file who's import began
        """

        message = "started : " + file
        progress_file_path = os.path.join(os.path.dirname(file), "import_progress.dat")
        Utilities._shell("echo \"%s\" >> \"%s\"" % (message, progress_file_path))

    def __end_progress(self, file):
        """
        Writes for the end of importing the file

        :param file: the file who's import finished
        """

        message = "finished : " + file
        progress_file_path = os.path.join(os.path.dirname(file), "import_progress.dat")
        Utilities._shell("echo \"%s\" >> \"%s\"" % (message, progress_file_path))

    def __undo_progress(self, file):
        """
        Undoes all import progress so far on a file

        :param file: the file to undo progress on
        :raises ConnectionError: if the connection fails
        """

        rest, first = os.path.split(file)
        _, second = os.path.split(rest)
        arr = first.split(".")[0].split("_")

        year = second
        inning = arr[0]
        outs = arr[1]

        self._connection._run("DELETE FROM pitch WHERE inning=%s and outs_when_up=%s and year(game_date)=%s;" %
                              (inning, outs, year))
