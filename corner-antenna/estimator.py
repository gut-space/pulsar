# Based on Analog-noise-estimator-cli by Sławek Figiel
# original: https://github.com/gut-space/analog-noise-estimator-cli
#
# Changes: Tomek Mrugalski


from matplotlib.pyplot import imread, imsave
import numpy as np

import cv2
import os
import sys
import argparse
import logging

from datetime import datetime, timedelta, timezone
from dateutil import parser as dateparser
from dateutil import tz

from analog_noise_estimator.rating import gaussian_rating as rating
from analog_noise_estimator.estimation import np_fftconvolve, estimate_in_boxes, estimate_noise
from analog_noise_estimator import laplacians
from analog_noise_estimator import metrics
from orbit_predictor.sources import get_predictor_from_tle_lines
from orbit_predictor.locations import Location

import passes

logging.basicConfig(stream=sys.stdout, format="%(levelname)s: %(message)s", level=logging.DEBUG)


def coords(lat: float, lon: float, alt: float = None ) -> str:
    """Turn longitude, latitude into a printable string."""
    txt = "%2.4f%s" % (abs(lat), "N" if lat>0 else "S")
    txt += " %2.4f%s" % (abs(lon), "E" if lon>0 else "W")
    if alt:
        txt += " %2.0fm" % alt
    return txt

def get_timestamp_str(timestamp: datetime, timezone: tz.tz) -> str:
    return f"{timestamp.astimezone(timezone)} {timestamp.astimezone(timezone).tzname()}"

def aggregate_noise(noise_table):
    """this function takes the noise_table (that contains entries for each box) and aggregates
    values for each row. The values are averaged. Returned structure is a dictionary."""

    row_noise = {}
    print("---------BEGIN noise-----")
    row = 0
    sum = 0.0
    elems = 0
    for n in noise_table:
        if n['row'] == row:
            sum += n['noise']
            elems += 1
        else:
            # Divide by 2, because we want to move from lines (2 per second) to seconds
            row_noise[row/2] = sum / elems
            row = n['row']
            sum = 0.0
            elems = 0

    return row_noise

def draw_noise(I, stats, box, metric="sigma"):
    '''
    Draw noise on image. Show division into boxes. Green circuit of box means
    low noise, red circuit means high noise. Requires original image @I,
    noise statistics @stats and @box size used to calculation.
    Sigma noise may be used directly @metric=sigma or may be rated using
    normal distribution based rank when @metric=gauss (or something else).

    Display OpenCV window.
    '''
    for stat in sorted(stats, key=lambda s: s['noise']):
        start = (stat['col'], stat['row'])
        end = tuple([min(d + box, s) for d, s in zip(start, reversed(I.shape[:2]))])
        center = tuple([int(d + box / 2) for d in start])
        noise = stat['noise']

        if metric == "sigma":
            val = noise
            max_ = 40
            text = "%.0f" % (val,)
        else:
            rate = rating(noise)
            val = rate
            max_ = 1
            text = "%.1f" % (rate,)
        color = (0, 255 * (max_ - val) / max_, 255 * (val / max_))

        cv2.rectangle(I, start, end, color, 2)
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.25
        font_thickness = 1
        cv2.putText(I, text, center, font_face, font_scale, (0, 128, 255), font_thickness)

    return I

def show_image(img, title):
    cv2.imshow(title, img)
    while cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) > 0:
        key = cv2.waitKey(50)
        if key == 27: # ESC
            cv2.destroyAllWindows()
            break


def write_noise_row(noise_csv_filename: str, noise_rows: str):
    out = open(noise_csv_filename, "w+")
    out.write("#time since AOS [s], average noise")
    for n in noise_rows.keys():
        out.write(f"{n},{noise_rows[n]:.3f}\n")
    out.close()
    print(f"Noise in CSV format written to {noise_csv_filename}")

def print_pos(positions: list):
    """Prints the positions list. Useful for debugging."""
    print(f"---positions has {len(positions)} entries")
    for x in positions:
        print(f"utc={x[0]}, local={x[0].astimezone()}: az={x[1]:3.1f}, el={x[2]:03.1f}")


def filter_positions(pos, aos, los):
    out = []
    for x in pos:
        if x[0] <= aos:
            continue
        if x[0] >= los:
            continue
        out.append(x)
    return out

def aggregate_pos_noise(pos, noise):
    # Ok, we have 2 lists here. positions describe timestamp, alt, az position of the sat.
    # The noise has timedelta since beginning, and noise value.
    out = []
    beg = pos[0][0]
    print("---BEFORE--------")
    index = 0
    print("#timestamp, az, el, delta[s], noise")
    for p in pos:
        delta = int((p[0] - beg).total_seconds())
        row = [p[0], p[1], p[2], delta, noise[delta]]
        out.append(row)
        index = index + 1
    print("---AFTER--------")
    return out

def write_aggregate_pos_noise(noise_csv_filename, agg):
    out = open(noise_csv_filename, "w+")
    out.write("# timestamp, az [deg], el[deg], delta [s], average noise\n")
    for n in agg:
        out.write(f"{n[0]},{n[1]:.3f},{n[2]:.3f},{n[3]},{n[4]:.3f}\n")
        pass
    out.close()
    print(f"Noise in CSV format written to {noise_csv_filename}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Path to image file")
    parser.add_argument("-l", "--laplacian", choices=['3', '5', '7'], default='3', help="Laplacian")
    parser.add_argument("-c", "--conv", help="Convulsion function", choices=['numpy', 'scipy'], default='numpy')
    parser.add_argument("-m", "--metric", help="Metric to plot", choices=["sigma", "gauss"], default="sigma")
    parser.add_argument("-n", "--noise", help="Noise plot", default=False, action="store_true")
    parser.add_argument("-r", "--rating", help="Plot rating", default=False, action="store_true")
    parser.add_argument("-b", "--box", default=30, type=int, help="Box size")

    parser.add_argument('--tle1', type=str, help="First line of the orbital data in TLE format")
    parser.add_argument('--tle2', type=str, help="Second line of the orbital data in TLE format")
    parser.add_argument("--lat", type=float, required=True,
        help="Specify the latitude of the observer in degrees, positive is northern hemisphere"
             " (e.g. 53.3 represents 53.3N for Gdansk)")
    parser.add_argument("--lon", type=float, required=True,
        help="Specify the longitude of the observer in degrees, positive is easter hemisphere "
             "(e.g. 18.5 represents 18.5E for Gdansk)")
    parser.add_argument("--alt", default=0, type=int, required=False,
        help="Observer's altitude, in meters above sea level")
    parser.add_argument("--aos", type=str,
        help="Specify the AOS timestamp, in UTC.")
    parser.add_argument("--los", type=str,
        help="Specify the LOS timestamp, in UTC.")

    args = parser.parse_args()


    # --- Orbital mechanics part --------------------

    if not args.tle1 or not args.tle2:
        print("tle1 and tle2 parameters are mandatory")
        sys.exit(-1)

    aos = dateparser.parse(args.aos)
    los = dateparser.parse(args.los)

    # If TLE is specified explicitly, we don't need to load any databases, just use
    # the TLE as is.
    tle_lines = (args.tle1, args.tle2)
    pred = get_predictor_from_tle_lines(tle_lines)
    zone = timezone.utc

    loc = Location('Observer', args.lat, args.lon, args.alt)

    pass_ = pred.get_next_pass(loc, when_utc=aos)


    positions = passes.get_pass(pred, loc, aos, los, passes.PassAlgo.TIME_TICKS, 15)

    positions2 = filter_positions(positions, aos, los)

    # def log_details(loc: Location, args: argparse.Namespace, when: datetime, pass_,
    #             zone: tz.tz):
    """Print the details of parameters used. Mostly for developer's convenience."""
    logging.info("Observer loc. : %s", coords(loc.latitude_deg, loc.longitude_deg))
    logging.info("AOS           : %s", get_timestamp_str(aos, zone))
    logging.info("LOS           : %s", get_timestamp_str(los, zone))
    logging.info("AOS (pred)    : %s", get_timestamp_str(pass_.aos, zone))
    logging.info("LOS (pred)    : %s", get_timestamp_str(pass_.los, zone))
    logging.info("Max elevation : %.1f deg at %s", pass_.max_elevation_deg,
        str(pass_.max_elevation_date.astimezone(zone)))
    logging.info("Duration(pred): %s", timedelta(seconds=pass_.duration_s).total_seconds())
    logging.info("Duration      : %s", (los - aos).total_seconds())






    # --- Image processing part ----------------------

    Ls = {
        '3': laplacians.L3,
        '5': laplacians.L5,
        '7': laplacians.L7
    }
    L = Ls[args.laplacian]

    if args.conv == 'numpy':
        conv2d = np_fftconvolve
    else:
        from scipy.signal import convolve2d
        conv2d = convolve2d

    path = args.path

    noise_img_filename = os.path.splitext(path)[0] + '-noise' + os.path.splitext(path)[1]
    noise_csv_filename = os.path.splitext(path)[0] + '.csv'

    print(f"IMG file = {noise_img_filename}")
    print(f"CSV file = {noise_csv_filename}")

    # Global recognition
    img = imread(path)

    img_gray = img

    if len(img.shape) == 3:
        # Magic happens here. If the image is read as RGBA, then it's really a 3D array
        # (each pixel is an 4 element array of values for each channel).
        # Since the alpha channel is always 1.0, we need to use offset sum, which starts
        # with a value of -1.0. The values are in 0.0..1.0 range, so need to convert to
        # 0..255 range and then divide by 3, because we summed 3 channels (RGB).
        tmp = img.sum(axis=2, initial=-1.0)*255/3

        # The values are almost fine, except some sums are almost correct (e.g. 43.99995).
        # To address those, we'll be adding 0.5 to each value, which will then be trucnated.
        img_gray = np.array(tmp+0.5, dtype=np.uint8)

    # Analog noise estimator requires image in range 0-255. If the image is loaded as
    # floating-point array (range 0.0-1.0), then the samples are scaled to 0.0-255.0 range.
    if img_gray.max() <= 1.0 and np.issubdtype(img_gray.dtype, np.floating):
       img_gray = img_gray * 255

    sigma = estimate_noise(img_gray, L, conv2d)

    # Local recognition
    box = args.box
    noise_stats = estimate_in_boxes(img_gray, L, conv2d, box)
    noises = [s['noise'] for s in noise_stats]

    noise_rows = aggregate_noise(noise_stats)

    agg = aggregate_pos_noise(positions2, noise_rows)

    #write_noise_row(noise_csv_filename, noise_rows)
    write_aggregate_pos_noise(noise_csv_filename, agg)

    # Some metrics
    # Sigma - Gauss distribution parameter for describe 'size' ('area') of the noise)
    # Global value of sigma for whole image:
    print("Global sigma:", sigma)
    # Average of sigma in separate boxes
    print("Average local sigma:", metrics.average_sigma(noises))
    # Average of sigma in separate boxes, but sigma is cliped to 30.
    print("Average local sigma clip:", metrics.average_sigma_clip(noises, 30))
    # Rating calculated on global sigma
    print("Global rating:", rating(sigma))
    # Rating with constant threshold. 0 for sigma < 10, 0.5 for sigma < 20 otherwise 1.
    print("Constant metric:", metrics.constant_ranges_rating(noises))
    # Rating with linear value for sigma between 10 and 20.
    print("Linear metric:", metrics.linear_middle_range_rating(noises))
    # Rating based on normal distribution for sigma between 10 and 20.
    print("Gauss metric:", metrics.gauss_middle_range_rating(noises))

    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img_noise = draw_noise(img, noise_stats, box, args.metric)
    cv2.imwrite(noise_img_filename, img_noise)
    print(f"File with noise marked written to {noise_img_filename}")

    # Show the noise plot, if requested
    if args.noise:
        show_image(img_noise, "")

    # Plot rating
    if args.rating:
        from matplotlib import pyplot as plt
        arr = range(0, 25)
        val = [rating(v) for v in arr]
        plt.plot(arr, val, 'r')
        plt.xticks(arr)
        plt.xlabel("Sigma")
        plt.ylabel("Rate")
        plt.title("Noise rating for gaussian sigma")
        plt.show()
