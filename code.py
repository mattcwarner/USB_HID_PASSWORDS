import adafruit_displayio_ssd1306
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import adafruit_sdcard
import aesio
from binascii import hexlify
import board
import busio
import circuitpython_csv as csv
from decrypter import load_bytes, decrypt_bytes
import digitalio
import displayio
# import encrypter
import os
import secrets
import storage
import struct
import sys
import terminalio
import time
import usb_hid

path_encrypted = '/sd/encrypted.bin'
v1_fmt_str = '15sx20sx50s'
encoding = 'utf-8'
key = bytes(secrets.master_password, encoding)
nul = b'\x00'


def main():
    vfs = mount_sd()
    # if not os.is_file(path_encrypted):
        # encrypter(path_encrypted, path_csv)
        # if not os.is_file(path_csv): raise OSError('error message')

    display = display_config()
    splash = draw_display(display)
    keyb = hid_config()
    change = btn_config('A')
    paste = btn_config('B')
    data = load_bytes(path_encrypted)
    current_entry = 0
    while True:
        if not change.value:
            if current_entry == len(data) - 1:
                current_entry = 0
            else:
                current_entry += 1
            write_line(data[current_entry]['e'], 1, splash)
            write_line(data[current_entry]['u'], 2, splash)
            write_line("*"*len(data[current_entry]['p']), 3, splash)
            time.sleep(0.5)
        else:
            pass
        if not paste.value:
            print("printing selected password", data[current_entry])
            d = decrypt_bytes(data[current_entry]['p'])
            keyb.write(d)
            time.sleep(0.5)
        else:
            pass
    storage.umount(vfs)


def mount_sd():
    # Connect to the card and mount the filesystem.
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs = digitalio.DigitalInOut(board.D7)
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    return vfs

def display_config():
    displayio.release_displays()
    i2c = busio.I2C (scl=board.SCL, sda=board.SDA)
    display_bus = displayio.I2CDisplay (i2c, device_address = 0x3C) # The address of my Board
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
    return display

def draw_display(display):
    splash = displayio.Group() # no max_size needed
    display.show(splash)
    write_line("Passwords", 0, splash, init=1)
    write_line("btn-A to cycle", 1, splash, init=1)
    write_line("btn-B to insert", 2, splash, init=1)
    write_line("passwords here", 3, splash, init=1)
    return splash

def write_line(text, line, splash, init=0):
    lines = {0:(40,7), 1:(2,20), 2:(2,38), 3:(2,53),}
    x, y = lines[line]
    lab = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=x, y=y)
    if init:
        splash.append(lab)
    else:
        splash[line] = lab # splash[-2] = label

def btn_config(button):
    BUTTONS = {'A': board.D0, 'B': board.D1,}
    button_object = digitalio.DigitalInOut(BUTTONS[button])
    button_object.switch_to_input(pull=digitalio.Pull.UP)
    return button_object

def hid_config():
    keyboard = Keyboard(usb_hid.devices)
    return KeyboardLayoutUS(keyboard)

if __name__ =="__main__":
    main()
