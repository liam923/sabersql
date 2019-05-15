#!/usr/bin/env python3

from datetime import datetime
import os
from . import Utilities
import math
from .ProgressHandler import ProgressHandler

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
        handler(0, status="Importing Statcast data")
        for year in years:
            savant_path = os.path.join(self._path, "BaseballSavant", str(year))
            progress_handler = ProgressHandler(savant_path)
            progress = progress_handler.get_progress()
            if progress != ProgressHandler.FINISHED:
                if progress == ProgressHandler.STARTED:
                    self.__undo_sql_import(year)
                progress_handler.start_progress()

                files = self.__year_files(year)
                file_prog = 0
                for csv in files:
                    self.__import_dataframe(Utilities._import_csv(csv))
                    file_prog += 1
                    handler(((file_prog / len(files)) * (1 / len(years))) + (year_prog / len(years)),
                            status="Importing Statcast data for %s" % year)

                progress_handler.end_progress()
            year_prog += 1
            handler(year_prog / len(years), status="Importing Statcast data")

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

        files = []
        file_list = Utilities._shell("find \"%s\" -name \"*.csv\"" % savant_path)[0].split("\n")
        for csv in file_list:
            if csv:
                files.append(csv)

        return files

    def __undo_sql_import(self, year):
        """
        Undoes all import progress to the database so far on a year

        :param year: the year to undo progress on
        :raises ConnectionError: if the connection fails
        """

        self._connection._run("DELETE FROM pitch WHERE game_year=%s;" % year)

        os.remove(os.path.join(self._path, "BaseballSavant", "%s" % year, "progress.dat"))
