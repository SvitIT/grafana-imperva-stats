import argparse
import all_files

parser = argparse.ArgumentParser(description="Upload the imperva log files to grafana")

parser.add_argument('--url', type=str, default="http://10.10.2.91:5001/upload_zip", help="url of api for logs retrieve")
parser.add_argument('--measurement', type=str, default="gateway1", help="measurement in influxdb, appends to url")
parser.add_argument('--path', type=str, default="/data/GwStatistics/PerformanceMonitorIndications", help="path where performance indications located")
#default="/data/GwStatistics/PerformanceMonitorIndications/"
args = parser.parse_args()

url = args.url + '/' + args.measurement
path = args.path + '/PerformanceMonitorIndications{}.csv.zip'
if __name__ == "__main__":
    all_files.call(url, path)
