# More details on the sysfs entries

## Drivers

The kernel drivers in this repository are mostly running on a 4.19 kernel.
They should be backward compatible to 4.9 and potentially compatible with
higher kernel version like 5.10.

### scd-hwmon

The `scd-hwmon` is a central kernel module on Arista devices and gets loaded on
all platforms.

When this driver is loaded, the various gpios and resets are exposed on the sysfs.
They can be set and unset by writing into the sysfs file.
The meaning of `0` or `1` should be deduced based on the name of the sysfs entry.

```
cd /sys/module/scd/drivers/pci:scd/<pciAddr>/
# put the switch chip in reset
echo 1 > switch_chip_reset
```

## Components

This section describes how to interact with the various components exposed by
the kernel drivers.
In order to see them, the platform must be successfully initialized.

The following sections describe how to manually interact with the components.
Examples shown may differ across platforms but the logic stays the same.

### LEDs

LED objects can be found under `/sys/class/leds`.The brightness field is used to
toggle between off and different colors.
The brightness to LED color mapping is as follows (0 maps to off for all LEDs):

```
status, fan_status, psu1, psu2:
  0 => off
  1 => green
  2 => red

beacon:
  1+ => blue

qsfp:
  1 => green
  2 => amber

fan:
  1 => green
  2 => red
  3 => amber
```

Given that this repository is primarily aimed at running on SONiC, an
implementation of the `led_control` plugin is available under
`arista.utils.sonic_leds`. It requires access to the `port_config.ini` file to
translate from `interface name` to `front panel port`.

### Fans

Fans are exposed under `/sys/class/hwmon/*` and respect the
[sysfs-interface](https://www.kernel.org/doc/Documentation/hwmon/sysfs-interface)
guidelines.

This repository provides the kernel modules to handle the fans.

### Temperature sensors

Temperature sensors are exposed under `/sys/class/hwmon/*` and also respect
the [sysfs-interface](https://www.kernel.org/doc/Documentation/hwmon/sysfs-interface).

They are all managed by linux standard modules like `lm73` and `max6658`.

### Power supplies

Power supplies and power controllers can be managed by the kernel's
generic `pmbus` module. Assuming the pmbus module was compiled into the
kernel.

Some power supplies may need kernel patches against the `pmbus` driver.

### System EEPROM

The system eeprom contains platform specific information like the `SKU`, the
`serial number` and the `base mac address`.

The location of the eeprom that contains this information vary from one product to
another. The most reliable way to get this information is to run `arista syseeprom`

The library implements the SONiC eeprom plugin under `arista.utils.sonic_eeprom`.

### Transceivers - QSFPs / SFPs

Currently only platforms with QSFP+, SFP+, OSFP and QSFP-DD ports are supported.
All transceivers provide 2 kinds of information.

#### Pins

The first piece of information is obtained from the transceiver physical pins.
 - OSFP: present, reset, low power mode, interrupt, module select
 - QSFP: present, reset, low power mode, interrupt, module select
 - SFP: present, rxlos, txfault, txdisable

These knobs are accessible under `/sys/module/scd/drivers/pci:scd/.../`
The name of the entries follow this naming `<type><id>_<pin>`
For example `qsfp2_reset` or `sfp66_txdisable`.

See [this section](#scd-hwmon) on how to use them.

#### Eeproms

The second piece of information provided by a transceiver is the content of its
`eeprom`. It is accessible via `SMBus` at the fixed address `0x50`. Some
transceivers also exist at other `SMBus` addresses like `0x51` and `0x56`.

On linux, an unoffical module called `optoe` manages such devices.
This library implements the spfutil plugin for SONiC to manage xcvrs.

Before being read, the QSFP+, OSFP and QSFP-DD modules must be taken out of reset and
have their module select signals asserted. This can be done through the GPIO
interface. The library does it at boot time.

### QSFP - SFP multiplexing

On the `DCS-7050QX-32S`, the first QSFP port and the 4 SFP ports are multiplexed.
To choose between one or the other, write into the sysfs file located under
`/sys/modules/scd/drivers/pci:scd/.../mux_sfp_qsfp`

### GPIOs and resets

Most of the GPIOs of the system are exposed by the `scd-hwmon` driver.
They should be available under `/sys/module/scd/drivers/pci:scd/.../`.
