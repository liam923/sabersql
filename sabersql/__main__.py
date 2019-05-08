#!/usr/bin/env python3

import SDownloader
import SImporter
import PDownloader
import PImporter
import RDownloader
import RImporter
import MySQLConnection
import sys


def main(args=None):
    path = args[1]
    password = args[2]

    connection = MySQLConnection.MySQLConnection("root", password, "sabersql", "197.0.0.1")
    connection.create_database()

    # download statcast data
    sdownloader = SDownloader.SDownloader(path)
    sdownloader.download()
    print("downloaded statcast")

    # import statcast data
    simporter = SImporter.SImporter(path, connection)
    simporter.import_statcast_data()
    print("imported statcast")

    # download people data
    pdownloader = PDownloader.PDownloader(path)
    pdownloader.download()
    print("downloaded people")

    # import people data
    pimporter = PImporter.PImporter(path, connection)
    pimporter.import_people_data()
    print("imported people")

    # download retrosheet data
    rdownloader = RDownloader.RDownloader(path)
    rdownloader.download()
    print("downloaded retrosheet")

    # import retrosheet data
    rimporter = RImporter.RImporter(path, connection)
    rimporter.import_retrosheet_data(handler=print)
    print("imported retrosheet")


if __name__ == "__main__":
    sys.exit(main(args=sys.argv) or 0)
