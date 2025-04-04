# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials HID Keyboard example - Multi-key support"""
import time

import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# A simple neat keyboard demo in CircuitPython with multi-key support

# The pins we'll use, each will have an internal pullup
keypress_pins = [board.GP0, board.GP1]
key_pin_array = []
keys_pressed = [Keycode.RIGHT_BRACKET, Keycode.LEFT_BRACKET]
key_states = [False, False]  # Track the state of each key (pressed/released)

# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)

# Make all pin objects inputs with pullups
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pin_array.append(key_pin)

# For most CircuitPython boards:
led = digitalio.DigitalInOut(board.LED)
# For QT Py M0:
# led = digitalio.DigitalInOut(board.SCK)
led.direction = digitalio.Direction.OUTPUT

print("Waiting for key pin...")
led.value = False

while True:
    for i, key_pin in enumerate(key_pin_array):
        if not key_pin.value:  # Key is pressed
            if not key_states[i]:  # If it was not already pressed
                print(f"Key {keys_pressed[i]} pressed.")
                keyboard.press(keys_pressed[i])
                key_states[i] = True  # Update state to pressed
                led.value = True  # Turn on LED
        else:  # Key is released
            if key_states[i]:  # If it was previously pressed
                print(f"Key {keys_pressed[i]} released.")
                keyboard.release(keys_pressed[i])
                key_states[i] = False  # Update state to released

    # Turn off LED if no keys are pressed
    led.value = any(key_states)

    time.sleep(0.0001)
