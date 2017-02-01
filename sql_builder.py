#!usr/bin/env python
# -*- coding: utf-8 -*-
# Title: sql_builder.py
# author: clasch
# class: Udacity SQL Project 3
# date: 1/30/2016
# Description: Create SQLite db and tables, then populates them from csv files

import csv, sqlite3
from make_csv import process_map

FILEPATH = 'C:\\Users\\LonelyMerc\\Documents\\python\\udacity\\P3\\p3f\\'
OSM_FILE = 'fort_collins.osm'
DB_FILE = 'fc_osm.db'


# ================================================== #
#         OSM cleaning and CSV formatting            #
# ================================================== #


process_map(FILEPATH + OSM_FILE, True)
# process map calls osm xml file
  # cleans the xml file with extendable class CleanValue
  # shapes the values to value type specified in schema using cerberus.Validator, if True
  # writes the cleaned xml to csv format
  # with each element and element tag written to individual csv


# ================================================== #
#              Database/Table Creation               #
# ================================================== #

# connect to database / create db if it doesn't exist
conn = sqlite3.connect(FILEPATH + DB_FILE)
conn.text_factory = str
c = conn.cursor()


# if tables exist, purge them from the database
for drop in ["DROP TABLE Nodes;","DROP TABLE Nodes_Tags;","DROP TABLE Ways;","DROP TABLE Ways_Tags;","DROP TABLE Ways_Nodes;"]:
    try:
        c.execute(drop)
    except sqlite3.OperationalError as error:
        print "Cannot drop table:", error

# Create Database Tables for:
# Nodes
c.execute("""CREATE TABLE Nodes(
                id INTEGER PRIMARY KEY,
                lat REAL,
                lon REAL,
                user TEXT,
                uid INTEGER,
                version INTEGER,
                changeset INTEGER,
                timestamp TEXT);    """)
# Nodes_Tags
c.execute("""CREATE TABLE Nodes_Tags(
                id INTEGER,
                key TEXT,
                value TEXT,
                type TEXT,
                FOREIGN KEY(id) REFERENCES Nodes(id));    """)
# Ways
c.execute("""CREATE TABLE Ways(
                id INTEGER PRIMARY KEY,
                user TEXT,
                uid INTEGER,
                version INTEGER,
                changeset INTEGER,
                timestamp TEXT);    """)
# Way_Tags
c.execute("""CREATE TABLE Ways_Tags(
                id INTEGER,
                key TEXT,
                value TEXT,
                type TEXT,
                FOREIGN KEY(id) REFERENCES Ways(id));    """)
# Way_Nodes
c.execute("""CREATE TABLE Ways_Nodes(
                id INTEGER,
                node_id INTEGER,
                position INTEGER,
                FOREIGN KEY(id) REFERENCES Ways(id));    """)

print "Success building database:", DB_FILE

# ================================================== #
#                Populate Database                   #
# ================================================== #

# build and execute table populate query from csv

CSV_FILES = { "Nodes" : FILEPATH + "nodes.csv",
                "Nodes_Tags" : FILEPATH + "nodes_tags.csv",
                "Ways" : FILEPATH + "ways.csv",
                "Ways_Tags" : FILEPATH + "ways_tags.csv",
                "Ways_Nodes" : FILEPATH + "ways_nodes.csv" }


def populate_db_from_csv(table, csv_path):

    with open(csv_path, 'r') as csv_f:
        reader = csv.reader(csv_f)
        columns = next(reader)
        query = 'INSERT INTO {0}({1}) VALUES ({2});'
        query = query.format(table, ','.join(columns), ','.join('?' * len(columns)))
        for data in reader:
            c.execute(query, data)
        conn.commit()


for key in CSV_FILES:
    populate_db_from_csv(key, CSV_FILES[key])
    print "Success populating", key

conn.commit()
conn.close()
