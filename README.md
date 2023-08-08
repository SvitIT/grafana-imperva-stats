# Tool for imperva log visualization using grafana

## How to use

```
git clone https://github.com/Chmele/grafana-imperva-stats.git .
docker compose build
docker compose up
```

Api endpoint at `localhost:8000/upload_zip/\<measurement\>` to upload single archive with 4000 files to the desired measurement in influxdb

Grafana is up on `localhost:3000`, the user is default - admin, admin

Volumes mounted, so container remove/rebuild would not affect data in database.
