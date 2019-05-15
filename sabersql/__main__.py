#!/usr/bin/env python3

from . import SDownloader
from . import SImporter
from . import PDownloader
from . import PImporter
from . import RDownloader
from . import RImporter
from . import MySQLConnection
import sys
import argparse


def run(args=[]):
    parser = argparse.ArgumentParser(description="Download Retrosheet and BaseballSavant data, along with player data, and import it into a MySQL database. More information at https://github.com/liam923/sabersql")

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
    data_source_group.add_argument("--statcast", help="only process BaseballSavant data",
                                   action="store_true")
    data_source_group.add_argument("--people", help="only process people data",
                                   action="store_true")

    parser.add_argument("-u", "--user", help="the user of the MySQL database (default: %(default)s)",
                        default="root")
    parser.add_argument("-p", "--pass", help="the password of the MySQL database (default: %(default)s)",
                        default="password")
    parser.add_argument("-a", "--address", help="the address of the MySQL database (default: %(default)s)",
                        default="localhost")
    parser.add_argument("-s", "--schema", help="the name of the MySQL database schema (default: %(default)s)",
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
        connection = MySQLConnection.MySQLConnection(parsed['user'], parsed['pass'], parsed['schema'],
                                                     parsed['address'])
        connection.create_database()

    if parsed['people']:
        if parsed['download']:
            p_downloader = PDownloader.PDownloader(path)
            p_downloader.download(handler=progress)
        if parsed['import']:
            p_importer = PImporter.PImporter(path, connection)
            p_importer.import_people_data(handler=progress)

    if parsed['statcast']:
        if parsed['download']:
            s_downloader = SDownloader.SDownloader(path)
            s_downloader.download(handler=progress, year=parsed['year'])
        if parsed['import']:
            s_importer = SImporter.SImporter(path, connection)
            s_importer.import_statcast_data(handler=progress, year=parsed['year'])

    if parsed['retrosheet']:
        if parsed['download']:
            r_downloader = RDownloader.RDownloader(path)
            r_downloader.download(handler=progress, year=parsed['year'])
        if parsed['import']:
            r_importer = RImporter.RImporter(path, connection)
            r_importer.import_retrosheet_data(handler=progress, year=parsed['year'])


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
        sys.stdout.write('\n')
        sys.stdout.flush()


def main():
    sys.exit(run(args=sys.argv[1:]) or 0)


if __name__ == "__main__":
    main()
