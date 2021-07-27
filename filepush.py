import requests

files = {'file': open('./stats/PerformanceMonitorIndications6.csv','rb')}

print(requests.post('http://127.0.0.1:5000/upload', files=files).status_code)