#!/bin/bash

# Platform init script for rd98dx35xx 
rd98dx35xx_profile()
{
    MAC_ADDR=$(ip link show eth0 | grep ether | awk '{print $2}')
    find /usr/share/sonic/device/*rd98DX35xx* -name profile.ini | xargs sed -i "s/switchMacAddress=.*/switchMacAddress=$MAC_ADDR/g"
    echo "rd98dx35xx: Updating switch mac address ${MAC_ADDR}"
}

# - Main entry
rd98dx35xx_profile

# - Main entry
# LOGIC to enumerate SFP eeprom devices - send 0x50 to kernel i2c driver - initialize devices
echo eeprom 0x50 > /sys/bus/i2c/devices/i2c-2/new_device

# Disable BIOS ACPI interrupt
echo disable > /sys/firmware/acpi/interrupts/gpe01

exit 0
