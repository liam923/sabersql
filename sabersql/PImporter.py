#!/usr/bin/env python3

import os
from . import Utilities
import math
import functools
from .ProgressHandler import ProgressHandler


class PImporter:

    def __init__(self, path, connection):
        """
        Initializes a PImporter based on the path to the SaberSQL data and a MySQLConnection

        :param path: the path to the folder for all SaberSQL data
        :param connection: a MySQLConnection to the database to import data to
        """

        self._path = path
        self._connection = connection

        self.__key_pair = [
            ("key_person", "person_id"),
            ("key_mlbam", "mlbam"),
            ("key_retro", "retro"),
            ("key_bbref", "bbref"),
            ("key_fangraphs", "fangraphs"),
            ("name_first", "firstname"),
            ("name_last", "lastname"),
            ("name_given", "givenname"),
            ("name_suffix", "name_suffix"),
            ("name_matrilineal", "matrilinealname"),
            ("name_nick", "nickname"),
            ("birth_year", "birth_year"),
            ("birth_month", "birth_month"),
            ("birth_day", "birth_day"),
            ("death_year", "death_year"),
            ("death_month", "death_month"),
            ("death_day", "death_day"),
            ("pro_played_first", "pro_played_first"),
            ("pro_played_last", "pro_played_last"),
            ("mlb_played_first", "mlb_played_first"),
            ("mlb_played_last", "mlb_played_last"),
            ("col_played_first", "col_played_first"),
            ("col_played_last", "col_played_last"),
            ("pro_managed_first", "pro_managed_first"),
            ("pro_managed_last", "pro_managed_last"),
            ("mlb_managed_first", "mlb_managed_first"),
            ("mlb_managed_last", "mlb_managed_last"),
            ("col_managed_first", "col_managed_first"),
            ("col_managed_last", "col_managed_last"),
            ("pro_umpired_first", "pro_umpired_first"),
            ("pro_umpired_last", "pro_umpired_last"),
            ("mlb_umpired_first", "mlb_umpired_first"),
            ("mlb_umpired_last", "mlb_umpired_last")
        ]

    def import_people_data(self, handler=lambda *args: None):
        """
        Imports all downloaded people data to MySQL database

        :param handler: a function that takes in a double, representing the completion percentage of the import
        :raises ConnectionError: if the connection fails
        """

        status = "Importing people data"
        handler(0, status=status)
        progress_handler = ProgressHandler(os.path.join(self._path, "Person"))
        progress = progress_handler.get_progress()
        if progress != ProgressHandler.FINISHED:
            if progress == ProgressHandler.STARTED:
                self.__undo_sql_import()
            progress_handler.start_progress()

            self.__import_people_from_file(os.path.join(self._path, "Person", "people.csv"), handler)

            progress_handler.end_progress()
        handler(1, status=status)

    def __import_people_from_file(self, url, handler):
        batch_size = 1000

        dataframe = Utilities._import_csv(url)

        indices = []
        for i in range(0, len(dataframe.columns)):
            if functools.reduce(lambda acc, e : acc or e[0] == dataframe.columns[i], self.__key_pair, False):
                indices.append(i)

        length = len(dataframe)

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
            for i in indices:
                yield make_cell(row[i])

        def make_data(dataframe):
            count = 0
            for row in dataframe.values:
                yield make_row(row)
                count += 1
                if count % batch_size == 0:
                    handler(count/length)

        self._connection.import_data("person", [x[1] for x in self.__key_pair], make_data(dataframe),
                                     batch_size=batch_size)

    def __undo_sql_import(self):
        """
        Undoes all import progress to the database so far on a year

        :param year: the year to undo progress on
        :raises ConnectionError: if the connection fails
        """

        self._connection._run("DELETE FROM person;")

        progress_file_path = os.path.join(self._path, "Person", "progress.dat")
        os.remove(progress_file_path)
