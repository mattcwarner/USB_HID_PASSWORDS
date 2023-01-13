import pyaes
import secrets
import struct

encrypted_passwords_path = 'test.bin'
fmt_str = '15sx20sx50s'
fmt = '10s'
encoding = 'utf-8'
key = bytes(secrets.master_password, encoding)

def load_bytes():
    with open(encrypted_passwords_path, 'rb') as f:
        data = f.read()
        eps = struct.iter_unpack(fmt, data)
        # take first item of tuple and remove trailing nul 
        return [x[0].rstrip(b'\x00') for x in eps]

def decrypyt_bytes(byte_arr):
    decipher = pyaes.AESModeOfOperationCTR(key)
    return decipher.decrypt(byte_arr).decode()


for p in load_bytes():
    password = decrypyt_bytes(p)
    print(password)
