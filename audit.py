#!usr/bin/env python
# -*- coding: utf-8 -*-
# Title: p3_audit_and_fix_fx.py
# author: sle7in
# class: Udacity SQL Project 3
# date: 1/16/2016
# description: residual draft taking xml file and auditing it for irregular data (audit)
#   and then correcting it and outputing corercted data
#   issue: needed to be edited from the audit in between runs for completions - separated into separate pipelines


import xml.etree.ElementTree as ET
import re
from collections import defaultdict

FILEPATH = "C:\Users\LonelyMerc\Documents\python\udacity\P3"


MAP = "\osm_files\\map"
FOCO = "\osm_files\\fort_collins.osm"
MAP_SAMPLE = "\\sample.osm"
FOCO_SAMPLE = "\\p3f\\fc_sample.osm"

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

##########################Tag Number###########################
def count_tags(filename):
    """outputs dictionary of top level file types and number"""
    tags = {}

    for event, elem in ET.iterparse(filename):
        if elem.tag not in tags:
            tags[elem.tag] = 1
        else:
            tags[elem.tag] += 1
    return tags
# for key in count_tags(FILEPATH + FOCO_SAMPLE):
#     print key, ':', tags[key]


##########################Key Functions####################
def key_type(element, keys):

    # print 'tag:',element.tag
    # print '\t',element.attrib
    if element.tag == 'tag':
        k = element.attrib['k']
        if re.match(lower, k):
            keys["lower"] += 1
        elif re.match(lower_colon, k):
            keys["lower"] += 1
        elif re.match(problemchars, k):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
            print "other chars:", k
    return keys


def process_key_types(filename):
    keys = {"lower":0, "lower_colon":0, "problemchars":0, "other":0}
    ct = 0
    for _, elem in ET.iterparse(filename):
        keys = key_type(elem, keys)
        # print 'event:', _
        # ct+=1
        # if ct > 10: break

    return keys

# print process_key_types(FILEPATH + FOCO_SAMPLE)

################User Functions######################
def process_users(filename):
    all_users = set()
    for _, elem in ET.iterparse(filename):
        if elem.tag == "node" or elem.tag == "way" or elem.tag == "relation":
            all_users.add(elem.get('uid'))
            # try: print elem.get('user')
            # except: print elem.attrib

    return all_users

# x = process_users()
# print len(x)


#####################Audit Streets#####################
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Way", "Circle", "East", "West", "North", "South",
            "Southwest", "Alley", "Square"]


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

def audit_street_type(irreg_street_types, street_name):
    # purpose of this fuction is to detect and add to dict any irregular streets to print out
    """Determines type of street from street_name and returns dictionary
    irreg_street_types with sets of streets for each street type."""

    type_match = street_type_re.search(street_name)
    if type_match:
        street_type = type_match.group()         # street_type is the last word in street_name
        if street_type not in expected:
            irreg_street_types[street_type].add(street_name)

    return irreg_street_types


def check_streets(filename):
    # purpose of this function is to output a list to visually see and update mappings
    """Parses node and way child tags for attrib['v'] of the key 'addr:street'
    and then runs audit_street_type on it. Returns defaultdict of audited
    streets."""

    irreg_street_types = defaultdict(set)

    for _, elem in ET.iterparse(filename):
        if elem.tag == "node" or elem.tag == "way":

            for child_tag in elem.iter("tag"):
                child_tag_attr_key = child_tag.attrib['k']
#######         Here is where I should enter different audits: if "street":audit_street_types, elif "zip":audit_zip

                if child_tag_attr_key == "addr:street":

                    audit_street_type(irreg_street_types, child_tag.attrib["v"])

    return irreg_street_types



st_types = check_streets(FILEPATH + FOCO)
for val in st_types:
    print val,":", st_types[val]
