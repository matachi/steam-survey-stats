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

Libraries
---------

* [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/) licensed
  under the [MIT
License](http://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/view/head:/COPYING.txt)
* [Data-Driven Documents](http://d3js.org/) licensed under the [Modified BSD
  License](https://github.com/mbostock/d3/blob/master/LICENSE)

