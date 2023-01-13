# USB_HID_PASSWORDS
A project exploring the use of the rp2040 microcontroller as a password manager.

First iteration hardware is a seeed xiao rp2040 board, oled screen, sd card reader and 2 push buttons

The first iteration of the password manager involves:
  Taking an unencrypted .csv file including passwords and usernames as available from your professional password manager
  Running the encryption script to generate an encrypted binary file from the csv and a master key.
  Secure deletion of the plaintext csv
  storage of encryted passwords on a micro-sd and master key on the rp2040 internal memory 
  main.py/code.py runs when the device is plugged into a device
    firstly it allows selection of a password on the oled using push button A to cycle through entries
    push button B causes decryption of corresponding password and entry into selected field on device
  
