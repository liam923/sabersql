#!/usr/bin/env python3

__pitch = """
CREATE TABLE IF NOT EXISTS pitch (

  pitch_id INT AUTO_INCREMENT,
  pitch_type CHAR(2) COMMENT \'The type of pitch derived from Statcast.\',
  game_date DATE COMMENT \'Date of the Game.\',
  release_speed DECIMAL(4,1) COMMENT \'Pitch velocities from 2008-16 are via Pitch F/X, and adjusted to roughly out-of-hand release point. All velocities from 2017 and beyond are Statcast, which are reported out-of-hand.\',
  release_pos_x DECIMAL(5,1) COMMENT \'Horizontal Release Position of the ball measured in feet from the catcher\\\'s perspective.\',
  release_pos_z DECIMAL(5,1) COMMENT \'Vertical Release Position of the ball measured in feet from the catcher\\\'s perspective.\',
  player_name VARCHAR(100) COMMENT \'Player\\\'s name tied to the event of the search.\',
  batter MEDIUMINT COMMENT \'MLB Player Id tied to the play event.\',
  pitcher MEDIUMINT COMMENT \'MLB Player Id tied to the play event.\',
  events VARCHAR(30) COMMENT \'Event of the resulting Plate Appearance.\',
  description VARCHAR(50) COMMENT \'Description of the resulting pitch.\',
  spin_dir CHAR(0) COMMENT \'* Deprecated field from the old tracking system.\',
  spin_rate_deprecated CHAR(0) COMMENT \'* Deprecated field from the old tracking system. Replaced by release_spin\',
  break_angle_deprecated CHAR(0) COMMENT \'* Deprecated field from the old tracking system.\',
  break_length_deprecated CHAR(0) COMMENT \'* Deprecated field from the old tracking system.\',
  zone TINYINT COMMENT \'Zone location of the ball when it crosses the plate from the catcher\\\'s perspective. https://baseballsavant.mlb.com/sections/statcast_search_v2/images/zones.png\',
  des TEXT COMMENT \'Plate appearance description from game day.\',
  game_type CHAR(1) COMMENT \'Type of Game. E = Exhibition, S = Spring Training, R = Regular Season, F = Wild Card, D = Divisional Series, L = League Championship Series, W = World Series\',
  stand CHAR(1) COMMENT \'Side of the plate batter is standing.\',
  p_throws CHAR(1) COMMENT \'Hand pitcher throws with.\',
  home_team VARCHAR(3) COMMENT \'Abbreviation of home team.\',
  away_team VARCHAR(3) COMMENT \'Abbreviation of away team.\',
  type CHAR(1) COMMENT \'Short hand of pitch result. B = ball, S = strike, X = in play.\',
  hit_location TINYINT COMMENT \'Position of first fielder to touch the ball.\',
  bb_type VARCHAR(15) COMMENT \'Batted ball type, ground_ball, line_drive, fly_ball, popup.\',
  balls TINYINT COMMENT \'Pre-pitch number of balls in count.\',
  strikes TINYINT COMMENT \'Pre-pitch number of strikes in count.\',
  game_year SMALLINT COMMENT \'Year game took place.\',
  pfx_x DECIMAL(5,4) COMMENT \'Horizontal movement in feet from the catcher\\\'s perspective.\',
  pfx_z DECIMAL(5,4) COMMENT \'Vertical movement in feet from the catcher\\\'s perpsective.\',
  plate_x DECIMAL(5,4) COMMENT \'Horizontal position of the ball when it crosses home plate from the catcher\\\'s perspective.\',
  plate_z DECIMAL(5,4) COMMENT \'Vertical position of the ball when it crosses home plate from the catcher\\\'s perspective.\',
  on_3b MEDIUMINT COMMENT \'Pre-pitch MLB Player Id of Runner on 3B.\',
  on_2b MEDIUMINT COMMENT \'Pre-pitch MLB Player Id of Runner on 2B.\',
  on_1b MEDIUMINT COMMENT \'Pre-pitch MLB Player Id of Runner on 1B.\',
  outs_when_up TINYINT COMMENT \'Pre-pitch number of outs.\',
  inning TINYINT COMMENT \'Pre-pitch inning number.\',
  inning_topbot CHAR(3) COMMENT \'Pre-pitch top or bottom of inning.\',
  hc_x DECIMAL(5,2) COMMENT \'Hit coordinate X of batted ball.\',
  hc_y DECIMAL(5,2) COMMENT \'Hit coordinate Y of batted ball.\',
  tfs_deprecated CHAR(0) COMMENT \'* Deprecated field from old tracking system.\',
  tfs_zulu_deprecated CHAR(0) COMMENT \'* Deprecated field from old tracking system.\',
  umpire CHAR(0) COMMENT \'* Deprecated field from old tracking system.\',
  sv_id VARCHAR(15) COMMENT \'Non-unique Id of play event per game.\',
  vx0 DECIMAL(5,4) COMMENT \'The velocity of the pitch, in feet per second, in x-dimension, determined at y=50 feet.\',
  vy0 DECIMAL(7,4) COMMENT \'The velocity of the pitch, in feet per second, in y-dimension, determined at y=50 feet.\',
  vz0 DECIMAL(6,4) COMMENT \'The velocity of the pitch, in feet per second, in z-dimension, determined at y=50 feet.\',
  ax DECIMAL(6,4) COMMENT \'The acceleration of the pitch, in feet per second per second, in x-dimension, determined at y=50 feet.\',
  ay DECIMAL(6,4) COMMENT \'The acceleration of the pitch, in feet per second per second, in y-dimension, determined at y=50 feet.\',
  az DECIMAL(6,4) COMMENT \'The acceleration of the pitch, in feet per second per second, in z-dimension, determined at y=50 feet.\',
  sz_top DECIMAL(5,4) COMMENT \'Top of the batter\\\'s strike zone set by the operator when the ball is halfway to the plate.\',
  sz_bot DECIMAL(5,4) COMMENT \'Bottom of the batter\\\'s strike zone set by the operator when the ball is halfway to the plate.\',
  hit_distance SMALLINT COMMENT \'Projected hit distance of the batted ball.\',
  launch_speed DECIMAL(4,1) COMMENT \'Exit velocity of the batted ball as tracked by Statcast. For the limited subset of batted balls not tracked directly, estimates are included based on the process described here.\',
  launch_angle TINYINT COMMENT \'Launch angle of the batted ball as tracked by Statcast. For the limited subset of batted balls not tracked directly, estimates are included based on the process described here.\',
  effective_speed DECIMAL(6,3) COMMENT \'Derived speed based on the the extension of the pitcher\\\'s release.\',
  release_spin SMALLINT COMMENT \'Spin rate of pitch tracked by Statcast.\',
  release_extension DECIMAL(5,3) COMMENT \'Release extension of pitch in feet as tracked by Statcast.\',
  game_pk MEDIUMINT COMMENT \'Unique Id for Game.\',
  fielder_2 MEDIUMINT COMMENT \'MLB Player Id for catcher.\',
  fielder_3 MEDIUMINT COMMENT \'MLB Player Id for 1B.\',
  fielder_4 MEDIUMINT COMMENT \'MLB Player Id for 2B.\',
  fielder_5 MEDIUMINT COMMENT \'MLB Player Id for 3B.\',
  fielder_6 MEDIUMINT COMMENT \'MLB Player Id for SS.\',
  fielder_7 MEDIUMINT COMMENT \'MLB Player Id for LF.\',
  fielder_8 MEDIUMINT COMMENT \'MLB Player Id for CF.\',
  fielder_9 MEDIUMINT COMMENT \'MLB Player Id for RF.\',
  release_pos_y DECIMAL(6,4) COMMENT \'Release position of pitch measured in feet from the catcher\\\'s perspective.\',
  estimated_ba_using_speedangle DECIMAL(4,3) COMMENT \'Estimated Batting Avg based on launch angle and exit velocity.\',
  estimated_woba_using_speedangle DECIMAL(4,3) COMMENT \'Estimated wOBA based on launch angle and exit velocity.\',
  woba_value DECIMAL(3,2) COMMENT \'wOBA value based on result of play.\',
  woba_denom DECIMAL(3,2) COMMENT \'wOBA denominator based on result of play.\',
  babip_value DECIMAL(3,2) COMMENT \'BABIP value based on result of play.\',
  iso_value DECIMAL(3,2) COMMENT \'ISO value based on result of play.\',
  launch_speed_angle DECIMAL(3,2) COMMENT \'Launch speed/angle zone based on launch angle and exit velocity.\',
  at_bat_number SMALLINT COMMENT \'Plate appearance number of the game.\',
  pitch_number SMALLINT COMMENT \'Total pitch number of the plate appearance.\',
  pitch_name VARCHAR(30) COMMENT \'The name of the pitch derived from the Statcast Data.\',
  home_score TINYINT COMMENT \'Pre-pitch home score\',
  away_score TINYINT COMMENT \'Pre-pitch away score\',
  bat_score TINYINT COMMENT \'Pre-pitch bat team score\',
  fld_score TINYINT COMMENT \'Pre-pitch field team score\',
  post_home_score TINYINT COMMENT \'Post-pitch home score\',
  post_away_score TINYINT COMMENT \'Post-pitch away score\',
  post_bat_score TINYINT COMMENT \'Post-pitch bat team score\',
  if_fielding_alignment VARCHAR(30) COMMENT \'Infield fielding alignment at the time of the pitch.\',
  of_fielding_alignment VARCHAR(30) COMMENT \'Outfield fielding alignment at the time of the pitch.\',
  PRIMARY KEY (pitch_id)

) COMMENT \'Represents a pitch from Statcast data\';
"""

schemas = [__pitch]
