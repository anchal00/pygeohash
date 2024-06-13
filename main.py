from geo_hash import GeoHash

long, lat = 31.327222120016813, 76.89489296637475
hash = GeoHash().get_geohash(long, lat, precision=12)

print(f"Geohash for longitude {long} and latitude {long} is `{hash}")

decoded_long, decode_lat = GeoHash().get_coordinates(hash)
print(
    f"Decoded GeoHash `{hash}`,"
    f"longitude is {decoded_long} and latitude is {decode_lat}"
)
