# pylint: disable=R0201
import os
from datetime import datetime

from flask import Flask, render_template

import cfg
import shared
from bb import import_data, get_date_from_filename


APP = Flask(__name__)


def get_highchart_value_str(date, value):
    return "[Date.UTC({}, {}, {}, {}, {}), {}]"\
            .format(date.year, date.month, date.day, date.hour, date.minute,
                    value)


def filter_by(data, last_days):
    delta = last_days * 24 * 3600
    now = datetime.now()
    return [point for point in data if (now - point).total_seconds() <= delta ]


def get_hc_listdata(dictdata, days):
    counts = ['0'] * len(dictdata)
    for key, items in dictdata.items():
        idx = int(key)
        counts[idx] = str(int(len(items) / days))
    data = '{{ name: "{}", data: [{}] }}'.format('total', ','.join(counts))
    return "[{}]".format(data)


def get_hc_stacklistdata(data, days):
    result = []
    for stack, dictdata in enumerate(data):
        counts = ['0'] * len(dictdata)
        for key, items in dictdata.items():
            idx = int(key)
            counts[idx] = str(int(len(items) / (days[stack] or 1)))
        string = '{{ name: "{}", data: [{}] }}'\
                .format(shared.WEEKDAY_STACK_NAMES[stack], ','.join(counts))
        result.append(string)
    return "[{}]".format(",".join(result))


def load_data():
    _data = []
    for _file in os.listdir(cfg.DATA_ROOT):
        if not _file.endswith('.dat'):
            continue
        path = os.path.join(cfg.DATA_ROOT, _file)
        date = get_date_from_filename(_file)
        day_data = import_data(path)
        for hour, row in enumerate(day_data):
            for minute, value in enumerate(row):
                if value:
                    point = datetime(date.year, date.month, date.day, hour, \
                            minute)
                    _data.append(point)
    shared.DATA = _data
    shared.FIRST_TIME = shared.DATA[0] if shared.DATA else datetime.now()
    shared.TOTAL_DAYS = 1 + \
            int((datetime.now() - shared.FIRST_TIME).total_seconds() /
            (24 * 3600))


def get_data_by_hour(data):
    data_by_hour = {str(hour): [] for hour in xrange(0, 24)}
    for point in data:
        data_by_hour[str(point.hour)].append(point)
    return data_by_hour


def get_data_by_weekday_stack(data):
    data_by_weekday_stack = \
            [{str(day): [] for day in xrange(0, 7)}
             for _ in xrange(cfg.WEEKDAY_STACKS)]
    exist_days_by_weekday = [set() for _ in xrange(0, 7)]
    for point in data:
        weekday_stack = point.hour /\
                shared.WEEKDAY_STACK_INTERVAL
        data_by_weekday_stack[weekday_stack][str(point.weekday())]\
                .append(point)
        exist_days_by_weekday[point.weekday()].add(point.strftime('%Y-%m-%d'))
    days_by_weekday = \
            [len(exist_days) for exist_days in exist_days_by_weekday]
    return data_by_weekday_stack, days_by_weekday


@APP.route('/')
def index():
    load_data()
    
    weekdata = get_hc_stacklistdata(*get_data_by_weekday_stack(shared.DATA))
    hourdata = get_hc_listdata(get_data_by_hour(shared.DATA),
            shared.TOTAL_DAYS)

    recent_days = min(7, shared.TOTAL_DAYS)
    recent_data = filter_by(shared.DATA, last_days=recent_days)
    recent_weekdata = \
            get_hc_stacklistdata(*get_data_by_weekday_stack(recent_data))
    recent_hourdata = get_hc_listdata(
            get_data_by_hour(recent_data), recent_days)

    return render_template('stats.html',
            weekdata=weekdata,
            recent_weekdata=recent_weekdata,
            hourdata=hourdata,
            recent_hourdata=recent_hourdata,
            )
