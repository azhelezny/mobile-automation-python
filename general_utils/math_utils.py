__author__ = 'andrey'


def in_range(number, range_number, radius=2):
    return range_number + radius >= number >= range_number - radius