#!/usr/bin/env python3.9

import argparse
import sys

from geo_hash import GeoHash

arg_parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description="A simple Python Based Geohashing codec 🌎",
    add_help=True,
    epilog="Made for fun 🙂"
)
arg_parser.add_argument(
    "-e",
    metavar=("Longitude", "Latitude"),
    required=False,
    nargs=2,
    type=float,
    help="Encodes given Longitude and Latitude to a Geohash with provided precision (default precision is 12)",
)

arg_parser.add_argument(
    "-p",
    metavar="precision",
    required=False,
    type=int,
    choices=range(1, 13),
    help="Precision value (Integer between 1-12) for encoding Longitude and Latitude to a Geohash.",
)

arg_parser.add_argument(
    "-d",
    metavar="geohash",
    required=False,
    type=str,
    help="Decodes given Geohash to Longitude and Latitude",
)


name_space = arg_parser.parse_args()

geo_hash_object = GeoHash()

if name_space.e:
    precision = name_space.p
    print(geo_hash_object.get_geohash(*name_space.e, precision))
elif name_space.d:
    print(geo_hash_object.get_coordinates(name_space.d))
else:
    arg_parser.print_help()
