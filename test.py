from base64 import b64decode
from colored import Fore, Back, Style

HIDE = Fore.black
RESET = Style.reset
EMP = Back.yellow


def print_bytes(data: bytes | bytearray):
    for c in data:
        if c == 0:
            print(HIDE + f"{c:x}".zfill(2) + RESET, end=" ")
        else:
            print(EMP + f"{c:x}".zfill(2) + RESET, end=" ")
    print()


def print_sharecode_data(sharecode: str):
    print_bytes(b64decode(sharecode))


print_sharecode_data("AAAAADEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")