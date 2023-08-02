"""Methods to interact with influxdb and imperva logs"""


from influxdb import InfluxDBClient
from itertools import islice

BATCHLEN = 100

def split_every(n, iterable):
    """
    For less amount of requests, groups data points into list with BATCHLEN length
    """
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

def create_or_connect():
    """
    Ensures database 'imperva' exists and returns client with connection to it
    """
    client = InfluxDBClient(host='influx', database='imperva')
    if not {'name': 'imperva'} in client.get_list_database():
        client.create_database('imperva')
    return client

def write_points(points):
    """
    Writes points to influxDB as chunks with BATCHLEN length
    """
    client = create_or_connect()
    results = [client.write_points(batch)for batch in split_every(BATCHLEN, points)]
    return results

