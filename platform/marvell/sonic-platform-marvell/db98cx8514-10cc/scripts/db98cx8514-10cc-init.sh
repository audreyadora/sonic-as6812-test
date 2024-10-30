#!/bin/bash
# Platform init script for db98cx8514-10cc 
db98cx8514-10cc_profile()
{
    MAC_ADDR=$(ip link show eth0 | grep ether | awk '{print $2}')
    find /usr/share/sonic/device/*db98cx8514_10cc* -name profile.ini | xargs sed -i "s/switchMacAddress=.*/switchMacAddress=$MAC_ADDR/g"
    echo "db98cx8514-10cc: Updating switch mac address ${MAC_ADDR}"
}

# - Main entry
db98cx8514-10cc_profile

# LOGIC to enumerate SFP eeprom devices - send 0x50 to kernel i2c driver - initialize devices
echo optoe2 0x50 > /sys/bus/i2c/devices/i2c-2/new_device

# Disable BIOS ACPI interrupt
echo disable > /sys/firmware/acpi/interrupts/gpe01

exit 0
