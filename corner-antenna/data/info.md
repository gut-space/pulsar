# Estimating corner antenna selectivity

There is a list of 94 observations in skorcz-obs.txt. This is a CSV with the first
line explaining the columns (observation id, AOS, LOS, TLE line1, TLE line2, image filename)

The skorcz-obs.txt file was generated using the following SQL:

```sql
\copy (SELECT o.obs_id, o.aos, o.los, o.tle[1],o.tle[2], f.filename from observations o, observation_files f
       WHERE o.obs_id = f.obs_id AND station_id = 5 AND o.obs_id <= 4972 AND o.obs_id>=4734)
       to 'skorcz.csv' CSV HEADER;

```
python3 -m venv venv
source venv/bin/activate

python 0-script-gen.py skorcz-obs.txt 1 > 1-download.sh
python 0-script-gen.py skorcz-obs.txt 2 > 2-estimate.sh
```

The above will generate 2 scripts:

- **1-download.sh** that will download the image files
- **2-estimate.sh** that will estimate noise on all of those files

After both are run, the images will be downloaded and for each observation
there will be 3 files, e.g. for observation 4971, there will be:

- 4971.png - the original observation
- 4971-noise.png - the observation with noise estimates marked on it
- 4971.csv - the CSV with noise estimates (timestamp, azimuth, elevation, delta time, noise)

The `*.csv` files can be then plotted using `4-plot.py`. This file generates
polar-char.png with results.
