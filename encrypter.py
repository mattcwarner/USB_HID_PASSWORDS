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

path_from = 'passwords.csv'
path_to = '/sd/encrypted.bin'
v1_fmt_str = '15sx20sx50s'
encoding = 'utf-8'
key = bytes(secrets.master_password, encoding)



def main():
    # Connect to the card and mount the filesystem.
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs = digitalio.DigitalInOut(board.D7)
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    encrypt(read_csv(path_from), path_to)
    storage.umount(vfs)

def read_csv(path):
    data = {}
    with open(path, "r") as f:
        for line in csv.DictReader(f):
            data[line["Title"]] = line["Username"], line["Password"]
    return data

def encrypt(data, path):
    with open(path, 'wb') as f:
        for entry in data:
            username, password = data[entry]
            entry = bytes(entry, encoding)
            username = bytes(username, encoding)
            password = bytes(password, encoding)
            encrypted = bytearray(len(password))
            cipher = aesio.AES(key, aesio.MODE_CTR)
            cipher.encrypt_into(password, encrypted)
            hexlify(encrypted)
            stream = struct.pack(v1_fmt_str, entry, username, encrypted)
            f.write(bytes(stream))
            print(stream)

if __name__ == "__main__":
    main()
