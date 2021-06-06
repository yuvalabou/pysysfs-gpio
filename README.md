Linux SysFS GPIO access via Python
==================================

This package offer Python classes to work with GPIO on Linux.

This work is based on [@derekstavis](https://github.com/derekstavis) amazing work, with minor changes made entirely for my own sake of learning experience.

## System Requirements

As this package relies on modern techniques provided by Linux kernel, so your kernel version should support at least EPoll and SysFS interfaces.

## How to use it

1. Install the package

```shell
pip install pysysfs-gpio
```

## Example

```python
# Import Twisted mainloop
from twisted.internet import reactor

# Import this package objects
from pysysfs.Controller import Controller
from pysysfs.const import OUTPUT, INPUT, RISING

# Refer to your chip GPIO numbers and set them this way - or referance your board from boards.py
controller = Controller()
controller.available_pins = [1, 2, 3, 4]

# Allocate a pin as Output signal
pin = controller.alloc_pin(1, OUTPUT)
pin.high()   # Sets pin to high logic level
pin.low()    # Sets pin to low logic level
pin.read()   # Reads pin logic level

# Allocate a pin as simple Input signal
pin = controller.alloc_pin(1, INPUT)
pin.read()   # Reads pin logic level

# Allocate a pin as level triggered Input signal
def pin_changed(number, state):
    print("Pin '%d' changed to %d state" % (number, state))

pin = controller.alloc_pin(1, INPUT, pin_changed, RISING)
pin.read()   # Reads pin logic level

```

3. Don't forget to start reactor loop!

```python
    reactor.run()
```

## LED blink example

```python
from time import sleep

from pysysfs.boards import NANOPI_NEO_3
from pysysfs.const import OUTPUT
from pysysfs.Controller import Controller
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

controller = Controller()
controller.available_pins = NANOPI_NEO_3

led = controller.alloc_pin(79, OUTPUT)


def blink():
    led.high()
    sleep(1)
    led.low()
    sleep(1)

# Main loop
lc = LoopingCall(blink)
lc.start(0.1)

reactor.run()

```
