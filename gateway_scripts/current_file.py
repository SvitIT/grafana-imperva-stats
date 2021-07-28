import requests

a = open('.PerformanceMonitorIndicationsRotatorPersistentIndexes.bin')
magic_numbers = list(map(ord, a.readlines()[0]))
current = magic_numbers[33]*256+magic_numbers[32]


files = {'file': open('./stats/PerformanceMonitorIndications{}.csv'.format(current),'rb')}

requests.post('http://127.0.0.1:5000/upload', files=files)