from math import ceil
from typing import List


class GeoHash:
    def __init__(self) -> None:
        self.__base32_lookup_table = {
            0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6",
            7: "7", 8: "8", 9: "9", 10: "b", 11: "c", 12: "d",
            13: "e", 14: "f", 15: "g", 16: "h", 17: "j", 18: "k",
            19: "m", 20: "n", 21: "p", 22: "q", 23: "r", 24: "s",
            25: "t", 26: "u", 27: "v", 28: "w", 29: "x", 30: "y",
            31: "z",
        }
        self.__inverted_base32_lookup_table = {
            value: key for key, value in self.__base32_lookup_table.items()
        }

    def __to_base_32(self, binary_str: str) -> str:
        chunked_str = [
            binary_str[i:i+5] for i in range(0, len(binary_str), 5)
        ]

        return "".join(
            [
                self.__base32_lookup_table[int(chunk, base=2)] for chunk in chunked_str 
                                                               if len(chunk) == 5
            ]
        )

    def __encode_to_binary(self, number: float, bit_len: int, _range: List[float]) -> str:
        bin_string_list = []
        for _ in range(bit_len):
            if number < _range[1]:
                bin_string_list.append("0")
                _range[2] = _range[1] 
            else:
                bin_string_list.append("1")
                _range[0] = _range[1]
            _range[1] = (_range[0] + _range[2]) / 2
        return "".join(bin_string_list)

    def __longitude_to_binary(self, longitude: float, bit_len: int) -> str:
        _range = [-180, 0, 180]  # [low, mid, high]
        return self.__encode_to_binary(longitude, bit_len, _range)

    def __latitude_to_binary(self, latitude: float, bit_len: int) -> str:
        _range = [-90, 0, 90]  # [low, mid, high]
        return self.__encode_to_binary(latitude, bit_len, _range)

    def get_geohash(self, longitude: float, latitude: float, precision: int) -> str:
        # TODO: Validate lat, long
        total_bits = precision * 5
        longitude_bin: str = self.__longitude_to_binary(longitude, ceil(total_bits / 2))
        latitude_bin: str = self.__latitude_to_binary(latitude, ceil(total_bits / 2))

        interleaved_binary_str = "".join("".join(entry) for entry in list(zip(longitude_bin, latitude_bin)))
        return self.__to_base_32(interleaved_binary_str)

    def get_coordinates(self, geohash) -> tuple[float, float]:
        decoded_base32: List[int] = [self.__inverted_base32_lookup_table[char] for char in geohash]
        binary_str: str = "".join([bin(number).replace("0b", "").zfill(5) for number in decoded_base32])
        longitude_bin: str = "".join([char for index, char in enumerate(binary_str) if index % 2 == 0])
        latitude_bin: str = "".join([char for index, char in enumerate(binary_str) if index % 2 == 1])

        return self.__binary_to_longitude(longitude_bin), self.__binary_to_latitude(latitude_bin)
    
    def __binary_to_latitude(self, binary_stream: str) -> float:
        _range = [-90, 0, 90]
        return self.__decode_from_binary(binary_stream, _range)

    def __binary_to_longitude(self, binary_stream: str) -> float:
        _range = [-180, 0, 180]
        return self.__decode_from_binary(binary_stream, _range)

    def __decode_from_binary(self, binary_stream: str, _range: List[float]) -> float:
        for digit in binary_stream:
            if digit == "1":
                _range[0] = _range[1]
            else:
                _range[2] = _range[1]
            _range[1] = (_range[0] + _range[2]) / 2
        return _range[1]
