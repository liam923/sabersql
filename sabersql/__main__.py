#!/usr/bin/env python3

import SDownloader
import SImporter
import PDownloader
import PImporter
import RDownloader
import RImporter
import MySQLConnection
import sys
import argparse


def main(args=[]):
    parser = argparse.ArgumentParser(description="Download Retrosheet and Statcast data, along with player data, and import it into a MySQL database. More information at https://github.com/liam923/sabersql")

    parser.add_argument("path", help='the folder to store files downloaded and processed by sabersql', type=str)
    parser.add_argument("-y", "--year", help="process only the given year (default: process all years)", type=int)

    import_download_group = parser.add_mutually_exclusive_group()
    import_download_group.add_argument("--download", help="only download the files without importing to the database",
                                       action="store_true")
    import_download_group.add_argument("--import", help="only import to the database without downloading the files",
                                       action="store_true")

    data_source_group = parser.add_mutually_exclusive_group()
    data_source_group.add_argument("--retrosheet", help="only process Retrosheet data",
                                   action="store_true")
    data_source_group.add_argument("--statcast", help="only process Statcast data",
                                   action="store_true")
    data_source_group.add_argument("--people", help="only process people data",
                                   action="store_true")

    parser.add_argument("-u", "--user", help="the user of the MySQL database (default: %(default)s)",
                        default="root")
    parser.add_argument("-p", "--pass", help="the password of the MySQL database (default: %(default)s)",
                        default="password")
    parser.add_argument("-a", "--address", help="the address of the MySQL database (default: %(default)s)",
                        default="localhost")
    parser.add_argument("-n", "--database", help="the name of the MySQL database (default: %(default)s)",
                        default="sabersql")

    parsed = vars(parser.parse_args(args=args))
    if not parsed['import'] and not parsed['download']:
        parsed['import'] = True
        parsed['download'] = True
    if not parsed['retrosheet'] and not parsed['statcast'] and not parsed['people']:
        parsed['retrosheet'] = True
        parsed['statcast'] = True
        parsed['people'] = True

    path = parsed['path']

    if parsed['import']:
        connection = MySQLConnection.MySQLConnection(parsed['user'], parsed['pass'], parsed['database'],
                                                     parsed['address'])
        connection.create_database()

    if parsed['people']:
        if parsed['download']:
            pdownloader = PDownloader.PDownloader(path)
            pdownloader.download(handler=progress)
        if parsed['import']:
            pimporter = PImporter.PImporter(path, connection)
            pimporter.import_people_data(handler=progress)

    if parsed['statcast']:
        if parsed['download']:
            sdownloader = SDownloader.SDownloader(path)
            sdownloader.download(handler=progress, year=parsed['year'])
        if parsed['import']:
            simporter = SImporter.SImporter(path, connection)
            simporter.import_statcast_data(handler=progress, year=parsed['year'])

    if parsed['retrosheet']:
        if parsed['download']:
            rdownloader = RDownloader.RDownloader(path)
            rdownloader.download(handler=progress, year=parsed['year'])
        if parsed['import']:
            rimporter = RImporter.RImporter(path, connection)
            rimporter.import_retrosheet_data(handler=progress, year=parsed['year'])


def progress(fraction, status=''):
    bar_len = 40
    filled_len = int(round(bar_len * fraction))

    percents = round(100.0 * fraction, 1)
    bar = '=' * filled_len + ' ' * (bar_len - filled_len)

    text = '[%s] %s%% ...%s' % (bar, percents, status)
    sys.stdout.write(text)
    sys.stdout.write('\b' * len(text))
    sys.stdout.flush()

    if fraction >= 1:
        print()


if __name__ == "__main__":
    sys.exit(main(args=sys.argv[1:]) or 0)
