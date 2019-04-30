#!/usr/bin/env python3

import SDownloader
import SImporter
import PDownloader
import PImporter
import RDownloader
import MySQLConnection
import sys


def main(args=None):
    path = args[1]
    password = args[2]

    connection = MySQLConnection.MySQLConnection("root", password, "sabersql", "localhost")
    connection.create_database()

    # # download statcast data
    # sdownloader = SDownloader.SDownloader(path)
    # sdownloader.download(handler=print)
    #
    # # import statcast data
    # simporter = SImporter.SImporter(path, connection)
    # simporter.import_statcast_data(handler=print)
    #
    # # download people data
    # pdownloader = PDownloader.PDownloader(path)
    # pdownloader.download(handler=print)
    #
    # # import people data
    # pimporter = PImporter.PImporter(path, connection)
    # pimporter.import_people_data(handler=print)

    # download retrosheet data
    rdownloader = RDownloader.RDownloader(path)
    rdownloader.download(handler=print)


if __name__ == "__main__":
    sys.exit(main(args=sys.argv) or 0)
