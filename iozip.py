from zipfile import ZipFile
import io
import csv
import itertools
from datetime import datetime


class IOZip:
    def __init__(self, tempfile):
        try:
            self.zipfile = ZipFile(tempfile._file)
        except AttributeError:
            self.zipfile = ZipFile(tempfile)
        self.plain = self.get_plain_data()

    def get_first_file(self):
        return self.zipfile.read(self.zipfile.filelist[0])

    def get_plain_data(self):
        pass


class ImpervaLog(IOZip):
    def get_plain_data(self):
        return [
            IOZip(io.BytesIO(self.zipfile.read(i))).get_first_file() 
            for i in self.zipfile.filelist]

    def make_payload(self, measurement):
        yield from (substitute(measurement, time, raw) for row in self.plain for time, raw in group_bytes_by_time(row))

    def flat_payload(self, measurement):
        return itertools.chain.from_iterable(self.make_payload(measurement))

def substitute(measurement, time, raw):
    fields = {i["IndicationName"]: i for i in raw}
    yield from ({
        'measurement': measurement,
        'time': datetime.strptime(time, '%Y-%m-%d %H:%M:%S').isoformat()+'Z',
        'fields': {
                field+'Max': int(fields[field]['MaxValue']),
                field+'Avg': int(fields[field]['AverageValue']),
            }
    }for field in fields)

def bytes_to_csv_dict(b):
    return csv.DictReader(io.StringIO(b.decode()))

def group_bytes_by_time(csv_dict):
    return itertools.groupby(bytes_to_csv_dict(csv_dict), lambda x: x["TimeStamp"])



f = open("unpack/spam.zip", 'rb')
i = ImpervaLog(f)
i.get_plain_data()
i.make_payload('gw1')