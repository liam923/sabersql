#!/usr/bin/env python3

from datetime import datetime
import os
from . import Utilities
import math
import re
import pandas
from .ProgressHandler import ProgressHandler


class RImporter:

    def __init__(self, path, connection):
        """
        Initializes a RDownloader based on the path to the SaberSQL data and a MySQLConnection

        :param path: the path to the folder for all SaberSQL data
        :param connection: a MySQLConnection to the database to import data to
        """

        self._path = path
        self._connection = connection

    def import_retrosheet_data(self, year=None, handler=lambda *args: None):
        """
        Imports all downloaded Retrosheet data to MySQL database

        :param year: the year to be imported; defaults to all years 1903 to present
        :param handler: a function that takes in a double, representing the completion percentage of the import
        :raises ConnectionError: if the connection fails
        """

        if year:
            years = [year]
        else:
            years = [y for y in range(1903, datetime.now().year + 1)]

        handler(0, status="Importing Retrosheet data")
        year_prog = 0
        for year in years:
            self.__chadwick(year)
            self.__sql(year)

            year_prog += 1
            handler(year_prog / len(years), status="Importing Retrosheet data for %s" % year)

    def __chadwick(self, year):
        in_folder = os.path.join(self._path, "Retrosheet", "raw_event_files", "%s" % year)
        out_folder = os.path.join(self._path, "Retrosheet", "processed", "%s" % year)

        progress_handler = ProgressHandler(in_folder)
        if progress_handler.get_progress() != ProgressHandler.FINISHED:
            progress_handler.start_progress()

            # regular season
            Utilities._shell("mkdir -p \"%s\"" % os.path.join(out_folder, "REG"))
            Utilities._shell("(cd \"%s\" && cwevent -n -f 0-96 -x 0-62 -y %s %s*.EV* > \"%s\")"
                             % (os.path.join(in_folder, "%seve" % year), year, year,
                                os.path.join(out_folder, "REG", "all%s.csv" % year)))
            Utilities._shell("(cd \"%s\" && cwgame -n -f 0-83 -x 0-94 -y %s %s*.EV* > \"%s\")"
                             % (os.path.join(in_folder, "%seve" % year), year, year,
                                os.path.join(out_folder, "REG", "games%s.csv" % year)))
            Utilities._shell("(cd \"%s\" && cwsub -n -f 0-9 -y %s %s*.EV* > \"%s\")"
                             % (os.path.join(in_folder, "%seve" % year), year, year,
                                os.path.join(out_folder, "REG", "sub%s.csv" % year)))

            # all star game
            Utilities._shell("mkdir -p \"%s\"" % os.path.join(out_folder, "AS"))
            Utilities._shell("(cd \"%s\" && cwevent -n -f 0-96 -x 0-62 -y %s %s*.EV* > \"%s\")"
                             % (os.path.join(in_folder, "%sas" % year), year, year,
                                os.path.join(out_folder, "AS", "all%s.csv" % year)))
            Utilities._shell("(cd \"%s\" && cwgame -n -f 0-83 -x 0-94 -y %s %s*.EV* > \"%s\")"
                             % (os.path.join(in_folder, "%sas" % year), year, year,
                                os.path.join(out_folder, "AS", "games%s.csv" % year)))
            Utilities._shell("(cd \"%s\" && cwsub -n -f 0-9 -y %s %s*.EV* > \"%s\")"
                             % (os.path.join(in_folder, "%sas" % year), year, year,
                                os.path.join(out_folder, "AS", "sub%s.csv" % year)))

            # post season
            try:
                for filename in os.listdir(os.path.join(in_folder, "%spost" % year)):
                    m = re.search('%s(.+?).EVE' % year, filename)
                    if m:
                        series = m.group(1)
                        Utilities._shell("mkdir -p \"%s\"" % os.path.join(out_folder, series))
                        Utilities._shell("(cd \"%s\" && cwevent -n -f 0-96 -x 0-62 -y %s %s%s.EVE > \"%s\")"
                                         % (os.path.join(in_folder, "%spost" % year), year, year, series,
                                            os.path.join(out_folder, series, "all%s.csv" % year)))
                        Utilities._shell("(cd \"%s\" && cwgame -n -f 0-83 -x 0-94 -y %s %s%s.EVE > \"%s\")"
                                         % (os.path.join(in_folder, "%spost" % year), year, year, series,
                                            os.path.join(out_folder, series, "games%s.csv" % year)))
                        Utilities._shell("(cd \"%s\" && cwsub -n -f 0-9 -y %s %s%s.EVE > \"%s\")"
                                         % (os.path.join(in_folder, "%spost" % year), year, year, series,
                                            os.path.join(out_folder, series, "sub%s.csv" % year)))
            except FileNotFoundError:
                pass

            if len(os.listdir(os.path.join(out_folder, "REG"))) == 0:
                os.rmdir(os.path.join(out_folder, "REG"))
            if len(os.listdir(os.path.join(out_folder, "AS"))) == 0:
                os.rmdir(os.path.join(out_folder, "AS"))

            progress_handler.end_progress()
            ProgressHandler(out_folder).start_progress()

    def __sql(self, year):
        in_folder = os.path.join(self._path, "Retrosheet", "processed", "%s" % year)

        progress_handler = ProgressHandler(in_folder)
        progress = progress_handler.get_progress()
        if progress != ProgressHandler.FINISHED:
            if progress == ProgressHandler.STARTED:
                self.__undo_sql_import(year)
            progress_handler.start_progress()

            for series in os.listdir(in_folder):
                if series != "progress.dat" and series != ".DS_Store":
                    csv_template = os.path.join(in_folder, series, "%s%s.csv")
                    all_data = None
                    games_data = None
                    sub_data = None
                    try:
                        all_data = Utilities._import_csv(csv_template % ("all", year))
                        games_data = Utilities._import_csv(csv_template % ("games", year))
                        sub_data = Utilities._import_csv(csv_template % ("sub", year))
                    except pandas.errors.EmptyDataError:
                        pass

                    if all_data is not None and games_data is not None and sub_data is not None:
                        self.__import_dataframe(all_data, "event")
                        self.__import_dataframe(games_data, "game", fields={"TYPE": series})
                        self.__import_dataframe(sub_data, "sub")

            progress_handler.end_progress()

    def __import_dataframe(self, dataframe, table, fields={}):
        """
        Imports data from dataframe to MySQL

        :param dataframe: the dataframe to import
        :param table: the name of the table to import into
        :param fields: additional fields that are constant for the entire dataframe
        :raises ConnectionError: if the connection fails
        """

        keys = fields.keys()

        cols = []
        for col in dataframe.columns:
            if table == "game" and col == "AWAY_BI_CT":
                cols.append("AWAY_RBI_CT")
            elif table == "game" and col == "HOME_BI_CT":
                cols.append("HOME_RBI_CT")
            else:
                cols.append(col)
        for col in keys:
            cols.append(col)

        def make_cell(cell, key):
            t = type(cell)
            if t is int or t is float:
                if math.isnan(cell):
                    return "NULL"
                else:
                    return str(cell)
            elif t is str:
                if cell == "null" or cell == "" or cell == "(unknown)":
                    return "NULL"
                else:
                    if table == "game" and (key == "INPUT_RECORD_TS" or key == "EDIT_RECORD_TS"):
                        try:
                            arr = cell.split(" ")
                            pre = arr[0].split("/")
                            arr2 = arr[1].split(":")
                            post = arr2[1]
                            hours = int(arr2[0])
                            ampm = post[-2:]
                            minutes = int(post[:-2])

                            if hours == 12:
                                hours -= 12
                            if ampm == "PM":
                                hours += 12

                            dt = datetime(year=int(pre[0]), month=int(pre[1]), day=int(pre[2]), hour=hours, minute=minutes)
                            return dt.strftime("\'%Y/%m/%d %-H:%M:00\'")
                        except:
                            return "NULL"
                    else:
                        return "\'" + cell.replace("\'", "\\\'") + "\'"
            else:
                raise TypeError("Unrecognized cell type: %s" % str(t))

        def make_row(row):
            i = 0
            for cell in row:
                yield make_cell(cell, cols[i])
                i += 1
            for key in keys:
                yield make_cell(fields[key], key)

        def make_data(dataframe):
            for row in dataframe.values:
                yield make_row(row)

        self._connection.import_data(table, cols, make_data(dataframe), batch_size=100)

    def __undo_sql_import(self, year):
        """
        Undoes all import progress to the database so far on a year

        :param year: the year to undo progress on
        :raises ConnectionError: if the connection fails
        """

        self._connection._run("DELETE FROM event WHERE GAME_ID REGEXP '.{3}%s.{5}';" % year)
        self._connection._run("DELETE FROM game WHERE GAME_ID REGEXP '.{3}%s.{5}';" % year)
        self._connection._run("DELETE FROM sub WHERE GAME_ID REGEXP '.{3}%s.{5}';" % year)

        os.remove(os.path.join(self._path, "Retrosheet", "processed", "%s" % year, "progress.dat"))
