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
import os
import secrets
import storage
import struct
import sys
import terminalio
import time
import usb_hid

path_from = '/sd/encrypted.bin'
v1_fmt_str = '15sx20sx50s'
encoding = 'utf-8'
key = bytes(secrets.master_password, encoding)
nul = b'\x00'


def main():
    vfs = mount_sd()
    display = display_config()
    splash = draw_display(display)
    keyb = hid_config()
    change = btn_config('A')
    paste = btn_config('B')
    data = load_bytes(path_from)
    current_entry = 0
    while True:
        if not change.value:
            if current_entry == len(data) - 1:
                current_entry = 0
            else:
                current_entry += 1
            text = data[current_entry]['e']
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=32, y=25)
            splash[-1] = text_area
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

    color_bitmap = displayio.Bitmap(128, 64, 1) # Full screen white
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF  # White

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(118, 54, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
    splash.append(inner_sprite)
    # Draw a label
    text = "Passwords"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=15)
    splash.append(text_area)

    text = "btn-A to cycle"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=32, y=25)
    splash.append(text_area)
    return splash

def btn_config(button):
    BUTTONS = {'A': board.D0, 'B': board.D1,}
    button_object = digitalio.DigitalInOut(BUTTONS[button])
    button_object.switch_to_input(pull=digitalio.Pull.UP)
    return button_object

def hid_config():
    # Set up device as hid keyboard
    keyboard = Keyboard(usb_hid.devices)
    return KeyboardLayoutUS(keyboard)

if __name__ =="__main__":
    main()
