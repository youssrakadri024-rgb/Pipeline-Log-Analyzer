import re

def extract(row):
    pattern =re.compile(r'(?P<month>\w{3})\s+(?P<day>\d{2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s.+:\s+(?P<message>\w+)')
    match =re.search(pattern,row)
    print(match)
    if match :
        print('test',match.groupdict())