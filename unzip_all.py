import zipfile
def unzip(root):
    for i in range(4000):
        with zipfile.ZipFile(root+f"/PerformanceMonitorIndications{i}.csv.zip", 'r') as zip_ref:
            zip_ref.extractall()