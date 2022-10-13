import machine
from projects.radio.test_radio import test_slave, test_master

from components import LED


def main():
    with LED(pin_number=25) as work_light:
        machine_id = "".join(hex(b)[2:] for b in machine.unique_id())
        if machine_id == "e66118604b824c25":
            work_light.update_flash_per_sec(2)
            work_light.on()
            test_master()
        elif machine_id == "e660c0d1c7869836":
            work_light.on()
            test_slave()
