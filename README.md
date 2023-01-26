# USB_HID_PASSWORDS
#### Video Demo: https://youtu.be/lXtYAOPhjNA
#### Description:
Plug the manager into one of your devices with a USB-C cable, choose the password you want to enter on the manager and select the password field on the device. Hit the input button and watch as your impossible to remember password is magically typed for you!

First iteration hardware is a seeed xiao rp2040 board, oled screen, sd card reader and 4 push buttons

#### The first iteration of the password manager involves:
  Taking an unencrypted .csv file including passwords and usernames as available from your professional password manager
  Running the encryption script to generate an encrypted binary file from the csv and a master key.
  Secure deletion of the plaintext csv
  storage of encryted passwords on a micro-sd and master key on the rp2040 internal memory 
  main.py/code.py runs when the device is plugged into a device
    firstly it allows selection of a password on the oled using push button A to cycle through entries
    push button B causes decryption of corresponding password and entry into selected field on device
  
  
#### Current structure:
####    lib/
      secrets.py has a bytestring of 16 or 32 bytes which is the key for the encryption.
      helpers.py has all the helper funtions for encryption, decryption and deletion.
####    / 
      code.py has the main script.
####    /sd/
      passwords.csv file must be added before first use preferably exported directly from your password manager.
      encrypted.bin will automatically be created on first use if passwords.csv is found on your sd card.
