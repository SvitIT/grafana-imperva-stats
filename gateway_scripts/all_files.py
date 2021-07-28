import requests

print(requests.post('http://10.10.2.91:5001/upload_zip/gateway1', files=files).status_code)
for i in xrange(4000):
    files = {'file': open('/data/GwStatistics/PerformanceMonitorIndications//PerformanceMonitorIndications' + str(i) + '.csv.zip','rb')}
    requests.post('http://10.10.2.91:5001/upload_zip/gateway1', files=files)