#!/usr/bin/env python
import time
import os
from datetime import datetime

from basicplib.util import logger
from basicplib.util import fileutil


LOGGER = logger.create_default_logger()


def get_date_from_filename(filename):
    return datetime.strptime(filename, '%Y-%m-%d.dat')


def get_datafile_name():
    return "{}.dat".format(datetime.now().strptime('%Y-%m-%d'))


def get_datafile_path():
    return "../data/{}".format(get_datafile_name())


def import_data(path):
    data = []
    for hour in xrange(1, 25):
        data.append([False] * 60)
    if os.path.exists(path):
        with open(path) as _file:
            for hour, line in enumerate(_file.readlines()):
                if hour > 23:
                    break
                for minute in xrange(0, 60):
                    data[hour][minute] = line[minute] == '*'
    return data


def export_data(path, data):
    with open(path, 'w') as _file:
        for hourindex, hour in enumerate(data):
            for minute in hour:
                char = '*' if minute else ' '
                _file.write(char)
            _file.write('|{}'.format(hourindex))
            _file.write(os.linesep)
        for minute in xrange(0, 60):
            _file.write('{}'.format(minute % 10))
        _file.write(os.linesep)


def count_data(data):
    total = 0
    for hour in data:
        for minute in hour:
            if minute:
                total += 1
    return total


def main():
    LOGGER.info("----------------")
    LOGGER.info("start")
    LOGGER.info("----------------")
    while True:
        path = get_datafile_path()
        fileutil.ensure_path(path)
        data = import_data(path)
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        data[hour][minute] = True
        LOGGER.info("  export to {}, {} stars".format(path, count_data(data)))
        export_data(path, data)
        time.sleep(50)
    LOGGER.info("")


if __name__ == "__main__":
    main()
