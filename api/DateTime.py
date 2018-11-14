from datetime import time, datetime, date, timedelta


def valid_date(datestring):
    try:
        datetime.datetime.strptime(datestring, '%Y/%m/%d')
        return True
    except ValueError:
        return False

def string_to_date(datestring):
        return datetime.datetime.strptime(datestring, '%Y/%m/%d')

def check_valid_timediff(datestring1, datestring2):
    first = string_to_date(datestring1)
    second = string_to_date(datestring2)
    diff = (first - second) / timedelta(days=1)
    if diff < 0:
        return False
    return True