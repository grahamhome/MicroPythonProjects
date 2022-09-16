# Generic Tests for radio-fast module.
# Modify config.py to provide master_config and slave_config for your hardware.
import radio.radio_fast as radio_fast
from radio.config import master_config, slave_config, FromMaster, ToMaster
from utime import sleep_ms


def test_master():
    m = radio_fast.Master(master_config)
    send_msg = FromMaster()
    with open("master_log.txt", "w") as log:
        while True:
            result = m.exchange(send_msg)
            if result is not None:
                log.write(f"{result.i0}\n")
            else:
                log.write("Timeout\n")
            send_msg.i0 += 1
            sleep_ms(1000)


def test_slave():
    s = radio_fast.Slave(slave_config)
    send_msg = ToMaster()
    with open("slave_log.txt", "w") as log:
        while True:
            result = s.exchange(send_msg)  # Wait for master
            if result is not None:
                log.write(f"{result.i0}\n")
            else:
                print("Timeout\n")
            send_msg.i0 += 1
