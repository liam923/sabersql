# SaberSQL

SaberSQL is a software tool to help scrape data on MLB games from [Retrosheet](https://www.retrosheet.org) (dating back
to 1903) and [BaseballSavant](https://baseballsavant.mlb.com), as well as information on players, umpires, and managers
(via the [Chadwick Baseball Bureau Register](https://github.com/chadwickbureau/register)). This data can then be
imported to a MySQL database, allowing you to do customized queries on over a century of data.

## Installation
### Requirements
For SaberSQL to work, you must have already installed [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
and [Chadwick](http://chadwick.sourceforge.net/doc/index.html). MySQL is straightforward to install, and there is an
excellent guide to install Chadwick
[here](https://www.pitchbypitch.com/2013/11/29/installing-chadwick-software-on-mac/).
### Install SaberSQL
To install:
```bash
pip3 install sabersql
```

## Usage
To download and import all data to your database, simply use the command:
```bash
sabersql [path] -u [username] -p [password] -a [address] -s [schema]
```
where:
- path is the directory on your computer where downloaded data should be stored (as of May 2019, all of the data is
about 18GB total)
- username is the user of the MySQL database
- password is the user's password to the MySQL database
- address is the network address of the MySQL database
- schema is the name of the schema to be used (the schema should already exist, without any tables in it)

##### Optional Arguments
- `--download` - only download the data from the web without importing it (the MySQL database information can
then be omitted)

- `--import` - only import the data (assumes data has already been downloaded)

- `-y [year]` - only download and/or import a specific year's data

- `--retrosheet` - only download and/or import Retrosheet data

- `--statcast` - only download and/or import BaseballSavant data

- `--people` - only download and/or import player, umpire, and manager data

#### Notes
- Data will not be re-downloaded or re-imported if a command is run multiple times. Additionally, a process will resume
from where it left off if restarted.
- These processes are not fast. It will take many hours to download and import all data.

## Schema
The structure of the database is five tables: [person](#person), [pitch](#pitch), [event](#event), [game](#game), and
[sub](#sub).

#### <a name="person"></a>person
Each entry in this table represents someone who was a player, umpire, and/or manager.
#### <a name="pitch"></a>pitch
Each entry in this table represents a pitch recorded by BaseballSavant. Descriptions of each field can be found
[here](https://baseballsavant.mlb.com/csv-docs).
#### <a name="event"></a>event
Each entry in this table represents an event that Chadwick processed from Retrosheet data. Descriptions of each field
can be found [here](http://chadwick.sourceforge.net/doc/cwevent.html).
#### <a name="game"></a>game
Each entry in this table represents a game that Chadwick processed from Retrosheet data. Descriptions of each field
can be found [here](http://chadwick.sourceforge.net/doc/cwgame.html).
#### <a name="sub"></a>sub
Each entry in this table represents a substitution in a game that Chadwick processed from Retrosheet data. Descriptions
of each field can be found [here](http://chadwick.sourceforge.net/doc/cwsub.html).

## License
Copyright 2019 William Stevenson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.