Linux SysFS GPIO access via Python
==================================

This package offer Python classes to work with GPIO on Linux.

## System Requirements

As this package relies on modern techniques provided by Linux kernel, so your kernel version should support at least EPoll and SysFS interfaces.

## Package Requirements

This package is based on Twisted main loop.
To build the package you will also need setuptools.

## How to use it

1. Clone this repository

```shell
    git clone https://github.com/yuvalabou/pysysfs-gpio
```

2. Inside it, issue:

```shell
    python3 setup.py install
```

3. On your code:

```python

    # Import Twisted mainloop
    from twisted.internet import reactor

    # Import this package objects
    from sysfs import Controller
    from sysfs.const import OUTPUT, INPUT, RISING

    # Refer to your chip GPIO numbers and set them this way - or referance your board from boards.py
    Controller.available_pins = [1, 2, 3, 4]

    # Allocate a pin as Output signal
    pin = Controller.alloc_pin(1, OUTPUT)
    pin.high()   # Sets pin to high logic level
    pin.low() # Sets pin to low logic level
    pin.read()  # Reads pin logic level

    # Allocate a pin as simple Input signal
    pin = Controller.alloc_pin(1, INPUT)
    pin.read()  # Reads pin logic level

    # Allocate a pin as level triggered Input signal
    def pin_changed(number, state):
        print("Pin '%d' changed to %d state" % (number, state))

    pin = Controller.alloc_pin(1, INPUT, pin_changed, RISING)
    pin.read()  # Reads pin logic level

```

4. Don't forget to start reactor loop!

```python
    reactor.run()
```


## Contributing

If you think that there's work that can be done to make this module better
(and that's the only certainty), fork this repo, make some changes and create
a pull request. I will be glad to accept it! :)
