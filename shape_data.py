#!usr/bin/env python
# -*- coding: utf-8 -*-
# Title: shape_data.py
# author: clasch
# class: Udacity SQL Project 3
# date: 1/28/2016
# 0 edits from parent /../p3_data_shape.py

import re
from clean_class import CleanValue

fc_cleaner = CleanValue()     # instantiate CleanValue class for fort_collins


def attrib_parser(element, fields):
    """Generate an attribute dictionary from an element"""
    attr_dict = {}

    # Fill attr_dict from element attributes but only attributes designated by fields
    for attr in element.attrib:
        if attr in fields:                              # picks elements specified in fields
            attr_dict[attr] = element.attrib[attr]      # and adds them to dict(attr_dict)

    return attr_dict

def tag_parser(element, default):
    """Adds an attribute dictionary for each child element to a list"""
    tags = []
    # append dicts to 'tags' list
    all_tags = element.findall('tag')
    for tag in all_tags:
        key = tag.attrib['k']
        val = tag.attrib['v']
        tag_dict = {'id' : element.attrib['id']}                # instantiate with 'id'

        tag_dict['value'] = fc_cleaner.process(key, val)        # imported cleaning module

        if ':' in key:                                     # split key around ':' if it exists
            first = re.compile(r"^[a-zA-Z_]+")                  # matches first letter or underscore sequence
            second = re.compile(r":+?.+")                       # matches first ':' and all after it
            tag_dict['type'] = first.search(key).group()        # assigns 'type' to 'k' before first ':'
            tag_dict['key'] = second.search(key).group()[1:]    # assigns 'key' to 'k' after first ':'

        else:
            tag_dict['type']  = default                         # if no ':', assign type to default
            tag_dict['key']   = key                             # if no ':', assign 'key' to 'k'

        tags.append(tag_dict)

    return tags

def shape_element(element, node_fields=['id'], way_fields=['id'],
                  default_tag_type='regular'):
    """Clean and shape node and way XML elements to Python dict for
    CSV insertion"""

    if element.tag == 'node':

        node_attribs = attrib_parser(element, node_fields)
        tags = tag_parser(element, default_tag_type)

        return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':

        way_attribs = attrib_parser(element, way_fields)
        tags = tag_parser(element, default_tag_type)

        # way_nodes defined
        way_nodes = []
        all_nd = element.findall('nd')
        for i, nd in enumerate(all_nd):
            nd_attrib = { 'node_id'  : nd.attrib['ref'],
                          'id'       : element.attrib['id'],
                          'position' : i }

            way_nodes.append(nd_attrib)

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
