from base64 import b64decode, b64encode
from enum import Enum
from typing import Iterable, Literal, SupportsIndex


class Character(int, Enum):
    ganyu = 0x01
    diona = 0x02
    kaeya = 0x03
    chongyun = 0x04
    kamisato_ayaka = 0x05
    eula = 0x06
    shenhe = 0x07
    qiqi = 0x08
    barbara = 0x09
    xingqiu = 0x0A
    mona = 0x0B
    tartaglia = 0x0C
    sangonnomiya_kokomi = 0x0D
    kamisato_ayato = 0x0E
    candace = 0x0F
    nilou = 0x10
    diluc = 0x11
    xiangling = 0x12
    bennett = 0x13
    amber = 0x14
    yoimiya = 0x15
    klee = 0x16
    hu_tao = 0x17
    yanfei = 0x18
    dehya = 0x19
    fischl = 0x1A
    razor = 0x1B
    keqing = 0x1C
    cyno = 0x1D
    beidou = 0x1E
    kujou_sara = 0x1F
    raiden_syogun = 0x20


tuple_int51 = tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]


class hexarray():
    def __init__(self, data: bytes | None) -> None:
        self.__data: list[int] = []
        if data is not None:
            for c in data:
                self.__data.append(c >> 4)
                self.__data.append(c & 0b00001111)
    
    @staticmethod
    def __slice_check(key: slice):
        if key.step is not None:
            raise KeyError("key.step must be None")
        elif key.start > key.stop:
            raise KeyError("key.start < key.stop")
    
    def __getitem__(self, key: int | slice):
        if isinstance(key, slice):
            self.__slice_check(key)
            data: int = 0
            for i in range(key.start, key.stop):
                data <<= 4
                data |= self.__data[i]
            return data
        else:
            return self.__data[key]
    
    def __setitem__(self, key: int | slice, value: int):
        if isinstance(key, slice):
            self.__slice_check(key)
            data: int = value
            for i in range(key.start, key.stop)[::-1]:
                self.__data[i] = data & 0b1111
                data >>= 4
        else:
            if not 0 <= value < 16:
                raise ValueError("0 <= value < 16")
            self.__data[key] = value

    def append(self, value: int):
        if not 0 <= value < 16:
            raise ValueError("0 <= value < 16")
        self.__data.append(value)
    
    def __iter__(self):
        yield from self.__data


class Deck(hexarray):
    @staticmethod
    def _swapped_index(i: int):
        return 50 if i == 50 else i * 2 if i < 25 else i * 2 - 49
    
    def __init__(self, data: str | bytes | None = None) -> None:
        if data is None:
            data = bytearray((0,) * 51)
        elif isinstance(data, str):
            data = b64decode(data)
            swapped = bytearray()
            for i in range(51):
                swapped.append(data[self._swapped_index(i)])
            data = swapped
        
        super().__init__(data)
    
    def print_data(self):
        for i, c in enumerate(self):
            if i % 2 == 0:
                print(end=" ")
            if c == 0:
                print(f"\x1b[30m{c:x}\x1b[0m", end="")
            else:
                print(f"\x1b[43m{c:x}\x1b[0m", end="")
        print()
    
    def encode(self):
        barr = bytearray(51)
        for i in range(51):
            barr[self._swapped_index(i)] = self[i * 2] << 4 | self[i * 2 + 1]
        return b64encode(barr)

    def set_char(self, char: int, pos: Literal[0, 1, 2]):
        i = pos * 3 + 1
        self[i:i + 2] = char


deck1  = Deck("AAAAAAAAAAAAAHkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
deck1.print_data()
# deck1.set_char(Character.raiden_syogun, 0)
# deck1.print_data()
# print(deck1.encode())