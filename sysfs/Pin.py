"""Pin represtation."""

import logging

from const import (
    ACTIVE_LOW_MODES,
    SYSFS_GPIO_ACTIVE_LOW_PATH,
    SYSFS_GPIO_DIRECTION_PATH,
    SYSFS_GPIO_EDGE_PATH,
    SYSFS_GPIO_VALUE_HIGH,
    SYSFS_GPIO_VALUE_LOW,
    SYSFS_GPIO_VALUE_PATH,
)

Logger = logging.getLogger("sysfs.gpio")
Logger.addHandler(logging.StreamHandler())
Logger.setLevel(logging.DEBUG)


class Pin(object):
    """Represent a pin in SysFS."""

    def __init__(
        self, number: int, direction: int, callback=None, edge=None, active_low=0
    ) -> None:
        """
        @type  callback: callable
        @param callback: Method be called when pin changes state
        @type  edge: int
        @param edge:
            The edge transition that triggers callback, enumerated by C{Edge}
        @type active_low: int
        @param active_low:
            Indicator of whether this pin uses inverted logic for HIGH-LOW transitions.
        """
        self._number = number
        self._direction = direction
        self._callback = callback
        self._active_low = active_low

        self._fd = open(self._sysfs_gpio_value_path(), "r+")

        if callback and not edge:
            raise Exception("You must supply a edge to trigger callback on")

        with open(self._sysfs_gpio_direction_path(), "w") as fsdir:
            fsdir.write(direction)

        if edge:
            with open(self._sysfs_gpio_edge_path(), "w") as fsedge:
                fsedge.write(edge)

        if active_low:
            if active_low not in ACTIVE_LOW_MODES:
                raise Exception(
                    "You must supply a value for active_low which is either 0 or 1."
                )
            with open(self._sysfs_gpio_active_low_path(), "w") as fsactive_low:
                fsactive_low.write(str(active_low))

    @property
    def callback(self):
        """Gets this pin callback."""
        return self._callback

    @callback.setter
    def callback(self, value):
        """Sets this pin callback."""
        self._callback = value

    @property
    def direction(self):
        """Pin direction."""
        return self._direction

    @property
    def number(self) -> int:
        """Pin number."""
        return self._number

    @property
    def active_low(self):
        """Active low."""
        return self._active_low

    def set(self):
        """Set pin to HIGH logic setLevel."""
        self._fd.write(SYSFS_GPIO_VALUE_HIGH)
        self._fd.seek(0)

    def reset(self):
        """Set pin to LOW logic setLevel."""
        self._fd.write(SYSFS_GPIO_VALUE_LOW)
        self._fd.seek(0)

    def read(self) -> int:
        """Read pin value."""
        val = self._fd.read()
        self._fd.seek(0)
        return int(val)

    def fileno(self) -> int:
        """Get the file descriptor associated with this pin."""
        return self._fd.fileno()

    def changed(self, state):
        if callable(self._callback):
            self._callback(self.number, state)

    def _sysfs_gpio_value_path(self) -> str:
        """Get the file that represent the value of this pin."""
        return SYSFS_GPIO_VALUE_PATH % self.number

    def _sysfs_gpio_direction_path(self) -> str:
        """Get the file that represent the direction of this pin."""
        return SYSFS_GPIO_DIRECTION_PATH % self.number

    def _sysfs_gpio_edge_path(self) -> str:
        """Get the file that represent the edge that will trigger an interrupt."""
        return SYSFS_GPIO_EDGE_PATH % self.number

    def _sysfs_gpio_active_low_path(self) -> str:
        """Get the file that represents the active_low setting for this pin."""
        return SYSFS_GPIO_ACTIVE_LOW_PATH % self.number
