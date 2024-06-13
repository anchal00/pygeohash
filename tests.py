import random
import unittest

from geo_hash import GeoHash


class GeoHashingTests(unittest.TestCase):

    def setUp(self) -> None:
        self.geo_hash_object = GeoHash()

    def test_geohash_lat_long(self):
        coordinates_geohash_map = {
            # (long, lat) -> Expected hash
            (31.327222, 76.894893): "utwm2y7c1nvz",
            (-13.8940, -7.8031): "7ww5eg6xwkdx",
            (85.7689, 28.1213): "tuuzzxr42nr0",
            (-35.1739, 62.9859): "g5nyrd5pkwz0",
            (74.0968, 23.6638): "tshww5gess49",
            (145.2002, -46.7680): "ppxmbn5s9uum",
        }
        for coords, expected_geohash in coordinates_geohash_map.items():
            long, lat = coords
            PRECISION = random.randint(1, 12)
            self.assertEqual(
                self.geo_hash_object.get_geohash(long, lat, PRECISION),
                expected_geohash[:PRECISION]
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
