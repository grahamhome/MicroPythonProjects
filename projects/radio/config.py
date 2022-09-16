# config.py Configuration file for radio_fast.py
# This contains the user defined configuration
# (C) Copyright Peter Hinch 2017
# Released under the MIT licence

# Modified by Graham Home 2022
import ustruct
from radio.msg import RadioConfig, msg

# Choose a channel (or accept default 99)
# RadioConfig.channel = 99
testbox_config = RadioConfig(spi_no=0, csn_pin=5, ce_pin=12)  # My testbox
v1_config = RadioConfig(spi_no=0, csn_pin=5, ce_pin=3)  # Pico explorer
v2_config = RadioConfig(spi_no=1, csn_pin=5, ce_pin=3)  # Pico on breadboard
master_config = v1_config
slave_config = v2_config

# For both messages need to alter fmt, instance variables, pack() and unpack() methods, to suit application.
# Both messages must pack to the same length otherwise an assertion failure will occur at runtime.
class FromMaster(msg):
    fmt = "iii"

    def __init__(self):
        super().__init__(FromMaster, ToMaster)
        self.i0 = 0
        self.i1 = 0
        self.i2 = 0

    def pack(self):
        ustruct.pack_into(self.fmt, self.buf, 0, self.i0, self.i1, self.i2)
        return self.buf

    def unpack(self):
        self.i0, self.i1, self.i2 = ustruct.unpack(self.fmt, self.buf)
        return self


class ToMaster(msg):
    fmt = "iii"

    def __init__(self):
        super().__init__(FromMaster, ToMaster)
        self.i0 = 0
        self.i1 = 0
        self.i2 = 0

    def pack(self):
        ustruct.pack_into(self.fmt, self.buf, 0, self.i0, self.i1, self.i2)
        return self.buf

    def unpack(self):
        self.i0, self.i1, self.i2 = ustruct.unpack(self.fmt, self.buf)
        return self
