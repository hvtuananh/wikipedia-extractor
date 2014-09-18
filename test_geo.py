import sys
import re
import datetime

p = re.compile(r'[^a-z0-9#]+', re.I)
p_id = re.compile(r'id=(\d+)')
p_geo = re.compile(r'{{(coord|coorde|coordinate)s?\s?\|(.+?)\|([A-Z])\s*?\|(.+?)\|([A-Z])\s*?(\|?}}|\|(.+?)}})', re.I)
p_geo_a = re.compile(r'{{(coord|coorde|coordinate)s?\s?\|([^\|]+?)\|+?([^\|]+?)(\|?}}|\|+?(.+?)}})', re.I)

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
    if 'coord missing' in text.lower() or 'coords missing' in text.lower() or 'coords||' in text.lower() or 'coord||' in text.lower() or 'coord unknown' in text.lower() or 'coord|{{#expr' in text.lower() or '{{coord|}}' in text.lower() or 'coord ' in text.lower() or '{{coord|display' in text.lower() or '{{coorddisplay' in text.lower() or '{{coord|21.0367}}' in text.lower() or 'coord41' in text.lower() or '{{coordinates missing' in text.lower() or '{{coordinates|}}' in text.lower() or '{{coord}}' in text.lower() or '{{coordinate}}' in text.lower() or '{{coordinate/dms|' in text.lower():
        return None
    print text.strip()
    geo = []
    m1 = p_geo.search(text)
    if not m1:
        m2 = p_geo_a.search(text)
    if m1:
        geo.append(convert_arc(m1.group(2), m1.group(3).strip()))
        geo.append(convert_arc(m1.group(4), m1.group(5).strip()))
    elif m2:
        geo.append(convert_arc(m2.group(2)))
        geo.append(convert_arc(m2.group(3)))
    else:
        print "Cannot get correct geo location!"
        sys.exit(1)
        
    print geo
    print
    return geo

def process_data(input):
    for line in input:
        line = line.decode('utf-8')
        if '<doc' in line:
            geo = extract_geo(line)

def main():
    process_data(sys.stdin)

if __name__ == '__main__':
    main()