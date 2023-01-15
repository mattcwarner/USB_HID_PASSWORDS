import aesio
from binascii import hexlify
import circuitpython_csv as csv
import os
import secrets
import struct
import sys


def load_bytes(path, path_csv='/sd/passwords.csv'):
    v1_fmt_str = '15sx20sx50s'
    nul = b'\x00'
    try:
        with open(path, mode='rb') as f:
            data = f.read()
    except OSError:
        print(f"No such file: {path}")
        print(f"Trying to create from {path_csv}")
        encrypt(read_csv(path_csv), path)
        print(f'securely removing {path_csv}')
        secure_delete(path_csv)
        with open(path, mode='rb') as f:
            data = f.read()
        print(f'success, {path} created, {path_csv} deleted')
    password_dictionary = {}
    unit_size = struct.calcsize(v1_fmt_str)
    # print(f'size of data: {len(data)}, size of unit: {unit_size}.')
    for index, _ in enumerate(range(0, len(data), unit_size)):
        fields = struct.unpack_from(v1_fmt_str, data, offset=unit_size*index)
        x = []
        for y in fields:
            x.append(y.rstrip(nul))
        password_dictionary[index] = {'e':x[0].decode(), 'u':x[1].decode(), 'p':x[2]}
    return password_dictionary

def decrypt_bytes(byte_arr):
    encoding = 'utf-8'
    key = bytes(secrets.master_password, encoding)
    outp = bytearray(len(byte_arr))
    decipher = aesio.AES(key, aesio.MODE_CTR)
    decipher.decrypt_into(byte_arr, outp)
    return outp.decode()

def read_csv(path):
    data = {}
    try:
        with open(path, "r") as f:
            for line in csv.DictReader(f):
                data[line["Title"]] = line["Username"], line["Password"]
    except OSError:
        print("No passwords.csv file on sd card")
        # at the moment this wont unmount the sd card
        # return 1
        sys.exit(1)
    return data

def encrypt(data, path):
    v1_fmt_str = '15sx20sx50s'
    encoding = 'utf-8'
    key = bytes(secrets.master_password, encoding)
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

def secure_delete(path, passes=3):
    with open(path, "ba+") as delfile:
        length = delfile.tell()
    with open(path, "br+") as delfile:
        for i in range(passes):
            delfile.seek(0)
            delfile.write(os.urandom(length))
    os.remove(path)


if __name__ == "__main__":
    main()

# Write your code here :-)
