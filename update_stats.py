#!/usr/bin/env python

import fileinput
import sqlite3
from urllib.request import urlopen
from bs4 import BeautifulSoup

data = "data2.tsv"
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

#def get_stored_operating_systems():
    #"""Get the operating systems stored in the data file."""

    #stored_operating_systems = []

    #with open(data, 'r') as f:
        #header = f.readline()
        #stored_operating_systems = header.split(',')
        #del stored_operating_systems[0]
        #for i in range(len(stored_operating_systems)):
            #stored_operating_systems[i] = stored_operating_systems[i].strip()

    #return stored_operating_systems

#def extract_operating_systems(stats):
    #"""Make a list of the operating systems in the list of stat tuples."""
    #return [x[0] for x in stats]

def insert_stats_into_database(stats):
    """Insert the stats into the database."""

    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Add columns
        try:
            c.execute(
                """ALTER TABLE stats
                   ADD "{}" TEXT NOT NULL DEFAULT (0);""".format(
                       stat[0].replace(".", "_")))
        except sqlite3.OperationalError:
            pass

    # Insert row containing the month's stats
    columns = ""
    values = ""
    for stat in stats:
        columns += "'{}',".format(stat[0].replace(".", "_"))
        values += "'{}',".format(stat[1])
    c.execute("""INSERT INTO stats('date', {})
                 VALUES ('lol', {});""".format(columns[:-1], values[:-1]))
    conn.commit()
    c.close()

def update_operating_systems_in_data_file(operating_systems):
    """Open the data file and append new operating systems."""

    # Operating systems read from the Steam survey page
    operating_systems = set(operating_systems)

    # Operating systems already stored in the local data file
    stored_operating_systems = get_stored_operating_systems()

    # Operating systems that isn't in the local data file yet
    new_operating_systems = operating_systems.difference(
        stored_operating_systems)

    if len(new_operating_systems) > 0:

        #for

        content = []

        with open(data, 'r') as f:
            content = f.readlines()

        header = content[0].strip()
        header += ',' + ','.join(new_operating_systems) +'\n'
        content[0] = header

        zeroes = ""
        for i in range(len(new_operating_systems)):
            zeroes += ",0"
        for i in range(1, len(content)):
            content[i] = content[i].strip() + zeroes + '\n'

        with open(data, 'w') as f:
            f.write(''.join(content))

def write_csv_file():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    content = ""
    c.execute("PRAGMA table_info(stats)")
    for row in c:
        if row[1] != "id":
            content += "{},".format(row[1])
    content = content[:-1] + "\n"
    c.execute("SELECT * FROM stats ORDER BY id DESC")
    for row in c:
        for i in range(1, len(row)):
            content += "{},".format(row[i])
        content = content[:-1] + "\n"
    c.close()
    with open(data, "w") as f:
        f.write(content)


stats = get_stats(soup)
#insert_stats_into_database(stats)
write_csv_file()
#print(','.join([x[0] for x in stats]))

#update_operating_systems_in_data_file(extract_operating_systems(stats))

#with open('data2.tsv', 'w') as f:
    #for stat in stats:
        #f.write("{}\t{}\n".format(stat[0], stat[1]))
