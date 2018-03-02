import time

__author__ = 'andrey'

import re


def smart_compare(text_one, text_two):
    if type(text_one) == "unicode":
        text_one.encode('ascii', 'replace')
    if type(text_two) == "unicode":
        text_two.encode('ascii', 'replace')
    n = len(text_one)
    if len(text_two) != n:
        return False
    for i in range(n):
        if text_one[i] == "?" or text_two[i] == "?":
            continue
        if text_one[i] != text_two[i]:
            return False
    return True


def get_json_key_value(method, key):
    counter = 5
    while 1:
        if counter <= 0:
            break
        try:
            time.sleep(2)
            result = method()[key]
            return result
        except KeyError:
            counter -= 1
    raise RuntimeError("Number of attempts to get value from JSON was exceeded")


def return_log_time_ms(log_line):
    t = re.search("[0-9]*:[0-9]*:[0-9]*.[0-9]*",log_line).group(0)
    h = int(t[:2])
    m = int(t[3:5])
    s = int(t[6:8])
    ms = int(t[9:12])
    return (h*3600+m*60+s)*1000+ms

