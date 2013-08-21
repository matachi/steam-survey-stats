Steam Survey Stats
==================

License: [GNU GPL version 3 or later](LICENSE)

Charts
------

Checkout the charts at
[matachi.github.io/steam-survey-stats](http://matachi.github.io/steam-survey-stats/)

Setup
-----

1. `virtualenv env`
2. `source env/bin/activate`
3. `pip install beautifulsoup4`

Add current Steam survey stats
------------------------------

To update the database and the csv file with the latest/current Steam survey
data from
[http://store.steampowered.com/hwsurvey](http://store.steampowered.com/hwsurvey),
run:

1. `source env/bin/activate`
2. `./update_stats.py`

Add stats from previous Steam survey
------------------------------------

Edit and add rows to the SQLite 3 database [raw_stats.db](raw_stats.db) more or
less easily with [Sqliteman](http://sqliteman.com/). Install it on Arch Linux
with `sudo pacman -S sqliteman`. Data from previous Steam surveys can be found
in articles from doing some searches on the net.

To update the csv file without retrieving the current stats from the hwsurvey
page, comment out the line `insert_stats_into_database(stats)` in
[update_stats.py](update_stats.py).

Libraries
---------

* [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/) licensed
  under the [MIT
License](http://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/view/head:/COPYING.txt)
* [Data-Driven Documents](http://d3js.org/) licensed under the [Modified BSD
  License](https://github.com/mbostock/d3/blob/master/LICENSE)

