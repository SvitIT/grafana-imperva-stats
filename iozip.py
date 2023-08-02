"""
Implementation of a lazy reading of a zipfile with folder of zipped .csv`s, according to imperva log format
"""


from io import StringIO, BytesIO
from itertools import groupby, chain
from csv import DictReader
from zipfile import ZipFile
from datetime import datetime


class IOZip:
    """
    Represents a lazy generator over files in ZipFile
    """
    def __init__(self, tempfile):
        try:
            self.zipfile = ZipFile(tempfile._file)
        except AttributeError:
            self.zipfile = ZipFile(tempfile)

    @property
    def plain(self):
        """
        Gets generator of raw data
        """
        return self.get_plain_data()

    def get_first_file(self):
        return self.zipfile.read(self.zipfile.filelist[0])

    def get_plain_data(self):
        """
        General implementation for non-layered zipfiles (zipped zip, etc.)
        """
        return [self.get_first_file()]

    def make_payload(self, measurement):
        """
        Generates payload: iter[point] suitable for InfluxDB with given measurement
        """
        yield from (substitute_point(measurement, time, raw)
                    for row in self.plain 
                    for time, raw in group_bytes_by_time(row))

    def flat_payload(self, measurement):
        return chain.from_iterable(self.make_payload(measurement))


class ImpervaLog(IOZip):
    def get_plain_data(self):
        """Implementation for imperva logs (zip of with folder of zipped .csv`s)"""
        return [
            IOZip(BytesIO(self.zipfile.read(i))).get_first_file() 
            for i in self.zipfile.filelist]


def substitute_point(measurement, time, raw):
    """
    Creates influxdb point with data provided
    """
    yield {
        'measurement': measurement,
        'time': datetime.strptime(time, '%Y-%m-%d %H:%M:%S').isoformat()+'Z',
        'fields': substitute_fields(raw)
    }

def substitute_fields(raw):
    """
    Unfolds raw csv log data from imperva
    """
    data = {i["IndicationName"]: i for i in raw}
    postfix_field = {'Max': 'MaxValue', 'Avg': 'AverageValue'}
    return {row+postfix: int(data[row][field])for postfix, field in postfix_field.items() for row in data}

def bytes_to_csv_dict(b):
    """
    Reads zipped csv in a lazy way
    """
    return DictReader(StringIO(b.decode()))

def group_bytes_by_time(csv_dict):
    """
    Groups csv rows by exact time matching
    """
    return groupby(bytes_to_csv_dict(csv_dict), lambda x: x["TimeStamp"])

# list(ImpervaLog(open("unpack/spam.zip", 'rb')).flat_payload('gw1'))
