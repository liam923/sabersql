
from unittest import TestCase
import sabersql.SDownloader

class TestSDownloader(TestCase):

    def test_download(self):
        downloader1 = sabersql.SDownloader.SDownloader("~/Documents")
        downloader2 = sabersql.SDownloader.SDownloader("/Volumes/Baseball Data/sabersql")
        self.assertEqual(30, len(downloader1._SDownloader__download_paths([1999])))
        self.assertEqual(120, len(downloader2._SDownloader__download_paths([1999, 2000, 20001, 2018])))
        self.assertEqual((("https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&s"
                           "tadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=1999%7C&hfSit=&player_type=pitcher&hfOuts=0"
                           "%7C&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfInfield=&t"
                           "eam=&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfPull=&metric_1=&hfInn=1%7C&min_pitche"
                           "s=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=h_launch_speed&sort_orde"
                           "r=desc&min_pas=0&chk_inning=on&chk_outs=on&type=details&"),
                          "~/Documents/BaseballSavant/1999/1_0.csv"),
                         downloader1._SDownloader__download_paths([1999])[0])
        self.assertEqual((("https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&s"
                           "tadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=1999%7C&hfSit=&player_type=pitcher&hfOuts=2"
                           "%7C&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfInfield=&t"
                           "eam=&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfPull=&metric_1=&hfInn=10%7C&min_pitch"
                           "es=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=h_launch_speed&sort_ord"
                           "er=desc&min_pas=0&chk_inning=on&chk_outs=on&type=details&"),
                          "~/Documents/BaseballSavant/1999/10_2.csv"),
                         downloader1._SDownloader__download_paths([1999])[-1])
        self.assertEqual((("https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&s"
                           "tadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2000%7C&hfSit=&player_type=pitcher&hfOuts=0"
                           "%7C&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfInfield=&t"
                           "eam=&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfPull=&metric_1=&hfInn=1%7C&min_pitche"
                           "s=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=h_launch_speed&sort_orde"
                           "r=desc&min_pas=0&chk_inning=on&chk_outs=on&type=details&"),
                          "/Volumes/Baseball Data/sabersql/BaseballSavant/2000/1_0.csv"),
                         downloader2._SDownloader__download_paths([2000, 2018])[0])
        self.assertEqual((("https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&s"
                           "tadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2018%7C&hfSit=&player_type=pitcher&hfOuts=2"
                           "%7C&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfInfield=&t"
                           "eam=&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfPull=&metric_1=&hfInn=10%7C&min_pitch"
                           "es=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=h_launch_speed&sort_ord"
                           "er=desc&min_pas=0&chk_inning=on&chk_outs=on&type=details&"),
                          "/Volumes/Baseball Data/sabersql/BaseballSavant/2018/10_2.csv"),
                         downloader2._SDownloader__download_paths([2000, 2018])[-1])
        self.assertEqual((("https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&s"
                           "tadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2010%7C&hfSit=&player_type=pitcher&hfOuts=1"
                           "%7C&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfInfield=&t"
                           "eam=&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfPull=&metric_1=&hfInn=6%7C&min_pitche"
                           "s=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=h_launch_speed&sort_orde"
                           "r=desc&min_pas=0&chk_inning=on&chk_outs=on&type=details&"),
                          "/Volumes/Baseball Data/sabersql/BaseballSavant/2010/6_1.csv"),
                         downloader2._SDownloader__download_paths([2010])[16])