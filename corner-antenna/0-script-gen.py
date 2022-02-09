

# Downloads all the images

import pathlib
import sys
pathlib.Path("data/").mkdir(parents=True, exist_ok=True)

BASE_URL="https://svarog.space/data/"
OPTIONS="--lat 53.7875 --lon 18.5273"

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} file.txt [1/2]")
    print("")
    print("The file.txt is supposed to be comma separated values with observation id, aos, los, tle1, tle2, image filename")
    print("1 - step 1 used to generate downloader script.")
    print("2 - step 2 used to estimate noise")
    sys.exit(-1)

file = sys.argv[1] if len(sys.argv)>=2 else "skorcz-obs.txt"

with open(file, "r+") as f:
    lines = f.readlines()
    for line in lines:
        l = line.strip().split(',')

        if sys.argv[2] == '1':
            print(f"curl -o {l[0]}.png {BASE_URL}{l[5]}")

        if sys.argv[2] == '2':
            print(f"python ../estimator.py {OPTIONS} --aos \"{l[1]}\" --los \"{l[2]}\" --tle1 \"{l[3]}\" --tle2 \"{l[4]}\" {l[0]}.png")
