import adafruit_sdcard
import aesio
from binascii import hexlify
import board
import busio
import circuitpython_csv as csv
import digitalio
import os
import secrets
import storage
import struct
import sys

path_from = 'test.bin'
v1_fmt_str = '15sx20sx50s'
key = bytes(secrets.master_password, 'utf-8')
encoding = 'utf-8'
nul = b'\x00'


def main():
    # Connect to the card and mount the filesystem.
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs = digitalio.DigitalInOut(board.D7)
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    data = load_bytes(path_from)
    print(data)
    for name in data:
        print(name, data[name]['p'], decrypyt_bytes(data[name]['p']))
    storage.umount(vfs)



def load_bytes(path):
    with open(path, mode='rb') as f:
        data = f.read()
        password_dictionary = {}
        unit_size = struct.calcsize(v1_fmt_str)
        print(f'size of data: {len(data)}, size of unit: {unit_size}.')
        for index, _ in enumerate(range(0, len(data), unit_size)):
            fields = struct.unpack_from(v1_fmt_str, data, offset=unit_size*index)
            x = []
            for y in fields:
                x.append(y.rstrip(nul))
            password_dictionary[x[0].decode()] = {'u':x[1].decode(), 'p':x[2]}
        return password_dictionary

def decrypyt_bytes(byte_arr):
    outp = bytearray(len(byte_arr))
    decipher = aesio.AES(key, aesio.MODE_CTR)
    return outp.decode()


if __name__ == "__main__":
    main()

