#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# =============================================================================
#  Version: 0.1 (Sep 18, 2014)
#  Author: Tuan-Anh Hoang-Vu (tuananh@nyu.edu), New York University
#
# =============================================================================
#  Copyright (c) 2014. Tuan-Anh Hoang-Vu (tuananh@nyu.edu).
# =============================================================================

import sys
import re
import datetime

p = re.compile(r'[^a-z0-9#]+', re.I)
p_id = re.compile(r'id=(\d+)')
p_geo = re.compile(r'{{coords?\s?\|(.+?)\|([A-Z])\|(.+?)\|([A-Z])(\|?}}|\|(.+?)}})', re.I)
p_geo_a = re.compile(r'{{coords?\s?\|([^\|]+?)\|([^\|]+?)(\|?}}|\|(.+?)}})', re.I)

def text_filter(word):
    word = unicode(word)
    if len(word) < 3:
        return False
    if word[0] == '&' and word[-1] == ';':
        return False
    if word[0] == "@":
        return False
    if word[:7] == 'http://' or word[:8] == 'https://':
        return False
    return True

def csv_format(string):
    return " ".join(string.replace('|', '').split())
    
def csv_format_kdtree(string):
    string = " ".join(filter(text_filter, csv_format(string).lower().split()))
    string = " ".join(filter(text_filter, p.split(csv_format(string))))
    string = " ".join(sorted(list(set(string.split()))))
    return string
    
def extract_id(text):
    matches = p_id.search(text)
    if matches:
        return matches.group(1)
    else:
        return -1
        
def convert_arc(text, direction = None):
    result = None
    try:
        text = text.split('|')
        if len(text) == 1:
            result = float(text[0])
        elif len(text) == 2:
            result = float(text[0]) + float(text[1])/60
        elif len(text) == 3:
            result = float(text[0]) + float(text[1])/60 + float(text[1])/3600
        else:
            return None
        if direction and (direction == 'S' or direction == 'W'):
            result = -result
    except:
        return None
        
    return result
        
def extract_geo(text):
    # test malformed cases
    # if 'coord missing' in text.lower() or 'coords missing' in text.lower() or 'coords||' in text.lower() or 'coord||' in text.lower() or 'coord unknown' in text.lower() or 'coord|{{#expr' in text.lower() or '{{coord|}}' in text.lower() or 'coord ' in text.lower() or '{{coord|display' in text.lower() or '{{coorddisplay' in text.lower() or '{{coord|21.0367}}' in text.lower():
    #     return None
    # print text.strip()
    geo = []
    m1 = p_geo.search(text)
    if not m1:
        m2 = p_geo_a.search(text)
    if m1:
        geo.append(convert_arc(m1.group(1), m1.group(2)))
        geo.append(convert_arc(m1.group(3), m1.group(4)))
    elif m2:
        geo.append(convert_arc(m2.group(1)))
        geo.append(convert_arc(m2.group(2)))
    else:
        pass
        # print "Cannot get correct geo location!"
        # sys.exit(1)
        
    # print geo
    # print
    return geo

def process_data(input):
    for line in input:
        line = line.decode('utf-8')
        if '<doc' in line:
            # start an article
            content = ""
            id = extract_id(line)
            username = "tuananh"
            date = datetime.datetime.utcnow().strftime('%a %b %d %H:%M:%S +0000 %Y')
            geo = extract_geo(line)
        elif '</doc>' in line:
            # finish an article, need to write to stdout
            if len(geo) == 0 or geo[0] is None:
                continue
            results = []
            results.append(str(id))
            results.append(str(geo[0]))
            results.append(str(geo[1]))
            results.append(username)
            results.append(date)
            results.append(csv_format(content))
            results.append(csv_format_kdtree(content))
            sys.stdout.write(("|".join(results) + "\n").encode("utf-8"))
        else:
            content += line
def main():
    process_data(sys.stdin)

if __name__ == '__main__':
    main()