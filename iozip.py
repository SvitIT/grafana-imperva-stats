from io import StringIO, BytesIO
from itertools import groupby, chain
from csv import DictReader
from zipfile import ZipFile
from datetime import datetime


class IOZip:
    def __init__(self, tempfile):
        try:
            self.zipfile = ZipFile(tempfile._file)
        except AttributeError:
            self.zipfile = ZipFile(tempfile)

    @property
    def plain(self):
        return self.get_plain_data()

    def get_first_file(self):
        return self.zipfile.read(self.zipfile.filelist[0])

    def get_plain_data(self):
        return [self.get_first_file()]

    def make_payload(self, measurement):
        yield from (substitute_point(measurement, time, raw)
                    for row in self.plain 
                    for time, raw in group_bytes_by_time(row))

    def flat_payload(self, measurement):
        return chain.from_iterable(self.make_payload(measurement))


class ImpervaLog(IOZip):
    def get_plain_data(self):
        return [
            IOZip(BytesIO(self.zipfile.read(i))).get_first_file() 
            for i in self.zipfile.filelist]


def substitute_point(measurement, time, raw):
    yield {
        'measurement': measurement,
        'time': datetime.strptime(time, '%Y-%m-%d %H:%M:%S').isoformat()+'Z',
        'fields': substitute_fields(raw)
    }

def substitute_fields(raw):
    data = {i["IndicationName"]: i for i in raw}
    postfix_field = {'Max': 'MaxValue', 'Avg': 'AverageValue'}
    return {row+postfix: int(data[row][field])for postfix, field in postfix_field.items() for row in data}

def bytes_to_csv_dict(b):
    return DictReader(StringIO(b.decode()))

def group_bytes_by_time(csv_dict):
    return groupby(bytes_to_csv_dict(csv_dict), lambda x: x["TimeStamp"])

# list(ImpervaLog(open("unpack/spam.zip", 'rb')).flat_payload('gw1'))
