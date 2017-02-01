# coding utf-8
"""
Nodes
id,lat,lon,user,uid,version,changeset,timestamp
id,key,value,type
Ways
id,user,uid,version,changeset,timestamp
id,node_id,position
id,key,value,type
"""

import sqlite3

FILEPATH = 'C:\\Users\\LonelyMerc\\Documents\\python\\udacity\\P3\\p3f\\'
DB_FILE = 'fc_osm.db'


conn = sqlite3.connect(FILEPATH + DB_FILE)
c = conn.cursor()


## Overview of number of entries for each table in db
# look at database table entries:
print "< First to look at database table entries"
print '-'*25

for table in ["Nodes", "Nodes_Tags","Ways","Ways_Nodes","Ways_Tags"]:
    query = """SELECT count(*) FROM {0}""".format(table)
    c.execute(query)
    fetch = c.fetchall()
    print table, "contains", fetch[0][0], "entries."

print '-'*25

## look at users and percent contributions:
print "< Next to look at users:"
print '-'*25

# # retrieve top 10% contributions, users, and number of lines contribution
query = """
SELECT user, count(*), round(count(*)*1.0 / sub1.total_entries * 100, 3)
FROM Nodes, (SELECT count(*) AS total_entries FROM Nodes) AS sub1
GROUP BY uid
ORDER BY count(uid) DESC
LIMIT 10;"""
c.execute(query)
for result in c.fetchall():
    print result
#
# # how many users comprise less than 1% of additions
query = """
SELECT count(user)
FROM (SELECT user, round(count(*)*100.0 /total_entries, 3) AS percent_contrib
    FROM Nodes, (SELECT count(*) AS total_entries FROM Nodes) AS sub1
    GROUP BY user
    HAVING percent_contrib < 1) AS sub2;"""
c.execute(query)
result = c.fetchall()
print '-'*25
print "The number of users comprising less than 1 percent are:", result[0][0]

print "-"*25


# check total restaurants
print "< Next to look at total restaurants:"
print '-'*25
query = """
SELECT count(*)
FROM (SELECT key, value FROM Nodes_Tags UNION ALL SELECT key, value FROM Ways_Tags) as sub
WHERE key = 'cuisine';"""
c.execute(query)
results = c.fetchall()
print results[0][0]

print '-'*25


## Look at all types of keys
print "< Next to look at the most common types of restaurants:"
print '-'*25

query = """
SELECT key, value, count(*) as ct
FROM (SELECT key, value FROM Nodes_Tags UNION ALL SELECT key, value FROM Ways_Tags) as sub
WHERE key = 'cuisine'
GROUP BY value
ORDER BY ct DESC
LIMIT 5
;"""
c.execute(query)
results = c.fetchall()
for result in results:
    print result

print '-'*25


# check population
print "< Next to look at Population:"
print '-'*25

query = """
SELECT key, value
FROM Nodes_Tags
WHERE key = 'population'
;"""
c.execute(query)
results = c.fetchall()
print results[0]



conn.close()
