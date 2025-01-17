"""Pin represtation."""

import logging
from typing import Callable

from .const import (
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
        self,
        number: int,
        direction: str,
        callback: Callable = None,
        interrupt_edge: str = None,
        active_low: bool = False,
    ) -> None:
        """
        @param callback: Method to be called when a pin changes state
        @param interrpt_egde: The edge transition that triggers callback
        """
        self._number = number
        self._direction = direction
        self._callback = callback
        self._active_low = active_low

        self._fd = open(self._sysfs_gpio_value_path(), "r+")

        if callback and not interrupt_edge:
            raise Exception("You must supply an interrupt edge to trigger callback on")

        with open(self._sysfs_gpio_direction_path(), "w") as fs_dir:
            fs_dir.write(direction)

        if interrupt_edge:
            with open(self._sysfs_gpio_edge_path(), "w") as fs_edge:
                fs_edge.write(interrupt_edge)

        if active_low:
            if active_low not in ACTIVE_LOW_MODES:
                raise Exception(
                    "You must supply a value for active_low which is either True or False."
                )
            with open(self._sysfs_gpio_active_low_path(), "w") as fs_active_low:
                fs_active_low.write(str(int(active_low)))

    @property
    def callback(self):
        """Gets this pin callback."""
        return self._callback

    @callback.setter
    def callback(self, value) -> None:
        """Sets this pin callback."""
        self._callback = value

    @property
    def direction(self) -> str:
        """Pin direction."""
        return self._direction

    @property
    def number(self) -> int:
        """Pin number."""
        return self._number

    @property
    def active_low(self) -> bool:
        """Active low."""
        return self._active_low

    def high(self) -> None:
        """Set pin to HIGH."""
        self._fd.write(SYSFS_GPIO_VALUE_HIGH)
        self._fd.seek(0)

    def low(self) -> None:
        """Set pin to LOW."""
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

    def changed(self, state) -> None:
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
