#!/usr/bin/env python

import sqlite3
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta

data = "data.csv"
database = "raw_stats.db"
url = "http://store.steampowered.com/hwsurvey"
soup = BeautifulSoup(urlopen(url))

def get_stats(soup):
    """Fetch the operating system stats from the soup."""

    # Find the div that contains the OSes and their percentages
    os_cat = soup.find(id="cat0_details")

    # Extract the OSes
    operating_systems = os_cat.find_all("div", class_="stats_col_mid")
    for i in range(len(operating_systems)):
        operating_systems[i] = operating_systems[i].string

    # Extract the percentages
    percentages = os_cat.find_all("div", class_="stats_col_right")
    for i in range(len(percentages)):
        percentages[i] = percentages[i].string[:-1]

    # Return a list of tuples of the OSes and their percentages
    return [(operating_systems[x], percentages[x]) for x in
            range(len(operating_systems))]

def insert_stats_into_database(stats):
    """Insert the stats into the database."""

    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Add columns
    for stat in stats:
        try:
            c.execute(
                """ALTER TABLE stats
                   ADD "{}" TEXT NOT NULL DEFAULT (0);""".format(
                       stat[0].replace(".", "_")))
        except sqlite3.OperationalError:
            pass

    # Insert a row containing the month's stats
    columns = ""
    values = ""
    for stat in stats:
        columns += "'{}',".format(stat[0].replace(".", "_"))
        values += "'{}',".format(stat[1])
    # If it's September 2013, then time = 20130801. Because the Steam Stats
    # page shows the stats for the previous month.
    time = (date.today() - timedelta(28)).strftime("%Y%m") + "01"
    c.execute("""INSERT INTO stats('date', {})
                 VALUES ({}, {});""".format(columns[:-1], time, values[:-1]))
    conn.commit()
    c.close()

def write_csv_file():
    """Create/update the csv file containing the OS stats."""

    # For keeping track of what OS every column is
    cells = {}

    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Header in the csv file
    content = "date,Windows,Linux,Mac,Other\n"

    # The columns in the stats table
    # The result looks like this:
    #     0|date|TEXT|1|0|0
    #     1|Windows 7 64 bit|TEXT|1|0|0
    #     2|Windows 8 64 bit|TEXT|1|0|0
    #     ...
    rows = c.execute("PRAGMA table_info(stats)").fetchall()
    # Ignore id and date on position 0 and 1
    for i in range(1, len(rows)):
        name = rows[i][1].split(" ")[0]
        os = ""
        if name == "Windows":
            os = "Windows"
        elif name == "MacOS":
            os = "Mac"
        elif name == "Other":
            os = "Other"
        else:
            os = "Linux"
        # The column position and what OS it is
        cells[i] = os

    # Fill the content variable with data for the OSes for the different months
    rows = c.execute("SELECT * FROM stats ORDER BY date ASC").fetchall()
    for row in rows:
        # Stats for this month
        stats = {'Linux': 0, 'Windows': 0, 'Mac': 0, 'Other': 0}
        for i in range(1, len(row)):
            # Calculate the sum for each OS
            stats[cells[i]] += float(row[i])
        content += "{},{},{},{},{}\n".format(
            row[0], stats["Windows"], stats["Linux"], stats["Mac"],
            stats["Other"])

    c.close()

    with open(data, "w") as f:
        f.write(content)

stats = get_stats(soup)
insert_stats_into_database(stats)
write_csv_file()
