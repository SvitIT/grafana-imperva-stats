import csv
import os
from itertools import groupby
from influxdb import InfluxDBClient
from datetime import datetime


client = InfluxDBClient(database='imperva')
filenames = [_ for _ in os.listdir('stats')]


def timeSplit(file):
    print('get file {}'.format(file.name))
    sect = groupby(csv.DictReader(file), lambda x: x["TimeStamp"])
    for i in sect:
        rework(*i)


def rework(time, data):
    fields = {i["IndicationName"]: i for i in data}
    ret = nullPayload(time)
    for f, v in fields.items():
        ret[0]['fields'].update(
            {
                f+'Max': int(v['MaxValue']),
                f+'Avg': int(v['AverageValue']),
            })
    client.write_points(ret)
    print('written {}'.format(ret))


def nullPayload (time):
    return [{
        'measurement': '8th',
        'time': datetime.strptime(time, '%Y-%m-%d %H:%M:%S').isoformat()+'Z',
        'fields': {}
    }]

if __name__ == "__main__":
    for i in filenames:
        timeSplit(open("stats/"+i))