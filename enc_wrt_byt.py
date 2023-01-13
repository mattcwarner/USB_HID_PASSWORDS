import pyaes
import secrets
import csv
import struct

passwords_path = 'passwords.csv'
encrypted_passwords_path = 'test.bin'
fmt_str = '15sx20sx50s'
fmt = '10s'
encoding = 'utf-8'
key = bytes(secrets.master_password, encoding)

def get_passwords(passwords_path):
    container = {}
    with open(passwords_path, "r") as f:
        for line in csv.DictReader(f):
            container[line["Title"]] = line["Username"], line["Password"]
    return container

def encrypt_passwords(password_dict):
    with open(encrypted_passwords_path, 'wb') as f:
        for entry in password_dict:
            username, password = password_dict[entry]
            entry = bytes(entry, encoding)
            username = bytes(username, encoding)
            cipher = pyaes.AESModeOfOperationCTR(key) # ECB - 16 bytes, CBC - multiples of 16, CTR - no restriction
            encrypted_password = cipher.encrypt(password)
            data = struct.pack(fmt, encrypted_password)
            f.write(data)


d = get_passwords(passwords_path)
encrypt_passwords(d)