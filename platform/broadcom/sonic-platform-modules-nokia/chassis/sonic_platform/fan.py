# Name: fan.py, version: 1.0
#
# Description: Module contains the definitions of FAN related APIs
# for Nokia IXR 7250 platform.
#
# Copyright (c) 2019, Nokia
# All rights reserved.
#

try:
    import time
    from sonic_platform_base.fan_base import FanBase
    from platform_ndk import nokia_common
    from platform_ndk import platform_ndk_pb2
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

NOKIA_MAX_IXR7250_FAN_SPEED = 9000  # Max RPMs per fan
NOKIA_MAX_IXR7250_TOLERANCE = 15


class Fan(FanBase):
    """Nokia IXR-7250 Platform-specific Fan class"""

    def __init__(self, fan_index, fantray_index, psu_fan, stub):
        self.max_fan_speed = NOKIA_MAX_IXR7250_FAN_SPEED
        self.is_psu_fan = psu_fan
        self.stub = stub
        self.fan_idx = fan_index
        self.is_cpm = 1
        if nokia_common.is_cpm() == 0:
            self.is_cpm = 0

        self.fantray_idx = 0
        if not self.is_psu_fan:
            self.fantray_idx = fantray_index

        self.partno = nokia_common.NOKIA_INVALID_STRING
        self.serialno = nokia_common.NOKIA_INVALID_STRING
        self.presence = False
        self.status = False
        self.direction = Fan.FAN_DIRECTION_EXHAUST
        self.timestamp = 0

    def _reset_fan_info(self):
        self.partno = nokia_common.NOKIA_INVALID_STRING
        self.serialno = nokia_common.NOKIA_INVALID_STRING
        self.presence = False
        self.status = False
        self.direction = Fan.FAN_DIRECTION_EXHAUST
        self.timestamp = 0

    def _get_fan_info(self):
        # Return the default value if it is not a CPM
        if self.is_cpm == 0:
            return

        current_time = time.time()
        if self.timestamp != 0 and (current_time - self.timestamp < 10):
            return

        channel, stub = nokia_common.channel_setup(nokia_common.NOKIA_GRPC_FAN_SERVICE)
        if not channel or not stub:
            self._reset_fan_info()
            return

        req_idx = platform_ndk_pb2.ReqFanTrayIndexPb(fantray_idx=self.fantray_idx)
        ret, response = nokia_common.try_grpc(stub.GetFanTrayInfo,
                                              platform_ndk_pb2.ReqFanTrayOpsPb(idx=req_idx))
        nokia_common.channel_shutdown(channel)

        if ret is False:
            self._reset_fan_info()
            return

        self.timestamp = current_time
        self.partno = response.fan_info.partno
        self.serialno = response.fan_info.serialno
        self.presence = response.fan_info.presence
        if response.fan_info.status == 'Online':
            self.status = True
        else:
            self.status = False

    def get_name(self):
        """
        Retrieves the fan name
        Returns:
            string: The name of the device
        """
        if not self.is_psu_fan:
            return "Fan{}".format(self.fan_idx)
        else:
            return "PSU{} Fan Missing"

    def get_model(self):
        """
        Retrieves the part number of the FAN
        Returns:
            string: Part number of FAN
        """
        self._get_fan_info()
        return self.partno

    def get_serial(self):
        """
        Retrieves the serial number of the FAN
        Returns:
            string: Serial number of FAN
        """
        self._get_fan_info()
        return self.serialno

    def get_presence(self):
        """
        Retrieves the presence of the FAN
        Returns:
            bool: True if fan is present, False if not
        """
        self._get_fan_info()
        return self.presence

    def get_status(self):
        """
        Retrieves the operational status of the FAN
        Returns:
            bool: True if FAN is operating properly, False if not
        """
        self._get_fan_info()
        return self.status

    def get_direction(self):
        """
        Retrieves the fan airflow direction
        Returns:
            A string, either FAN_DIRECTION_INTAKE or FAN_DIRECTION_EXHAUST
            depending on fan direction
        """
        self._get_fan_info()
        return self.direction

    def get_speed(self):
        """
        Retrieves the speed of fan
        Returns:
            int: percentage of the max fan speed
        """
        speed = 0
        if self.is_cpm == 0 or self.get_presence() is False:
            return speed

        channel, stub = nokia_common.channel_setup(nokia_common.NOKIA_GRPC_FAN_SERVICE)
        if not channel or not stub:
            return speed
        req_idx = platform_ndk_pb2.ReqFanTrayIndexPb(fantray_idx=self.fantray_idx)
        ret, response = nokia_common.try_grpc(stub.GetFanActualSpeed,
                                              platform_ndk_pb2.ReqFanTrayOpsPb(idx=req_idx))
        nokia_common.channel_shutdown(channel)

        if ret is False:
            return speed
        speed = response.fan_speed_actual.fantray_speed
        return speed

    def get_speed_tolerance(self):
        """
        Retrieves the speed tolerance of the fan
        Returns:
            An integer, the percentage of variance from target speed which is
        considered tolerable
        """
        tolerance = NOKIA_MAX_IXR7250_TOLERANCE

        channel, stub = nokia_common.channel_setup(nokia_common.NOKIA_GRPC_FAN_SERVICE)
        if not channel or not stub:
            return tolerance
        req_idx = platform_ndk_pb2.ReqFanTrayIndexPb(fantray_idx=self.fantray_idx)
        ret, response = nokia_common.try_grpc(stub.GetFanTolerance,
                                              platform_ndk_pb2.ReqFanTrayOpsPb(idx=req_idx))
        nokia_common.channel_shutdown(channel)

        if ret is False:
            return tolerance

        tolerance = response.fan_tolerance
        return tolerance

    def disable_fan_algorithm(self, disable):
        status = False
        if self.is_cpm == 0 or self.get_presence() is False:
            return status

        channel, stub = nokia_common.channel_setup(nokia_common.NOKIA_GRPC_FAN_SERVICE)
        if not channel or not stub:
            return status
        req_idx = platform_ndk_pb2.ReqFanTrayIndexPb(fantray_idx=self.fantray_idx)
        req_fan_algo = platform_ndk_pb2.SetFanTrayAlgorithmPb(fantray_algo_disable=disable)
        ret, response = nokia_common.try_grpc(stub.DisableFanAlgorithm,
                                              platform_ndk_pb2.ReqFanTrayOpsPb(idx=req_idx, fan_algo=req_fan_algo))
        nokia_common.channel_shutdown(channel)

        status = True
        return status

    def set_speed(self, speed):
        """
        Set fan speed to expected value
        Args:
            speed: An integer, the percentage of full fan speed to set fan to,
                   in the range 0 (off) to 100 (full speed)
        Returns:
            bool: True if set success, False if fail.
        """
        status = False
        if self.is_cpm == 0 or self.get_presence() is False:
            return status

        channel, stub = nokia_common.channel_setup(nokia_common.NOKIA_GRPC_FAN_SERVICE)
        if not channel or not stub:
            return status
        req_idx = platform_ndk_pb2.ReqFanTrayIndexPb(fantray_idx=self.fantray_idx)
        ret, response = nokia_common.try_grpc(stub.SetFanTargetSpeed,
                                              platform_ndk_pb2.ReqFanTrayOpsPb(idx=req_idx, fantray_speed=speed))
        nokia_common.channel_shutdown(channel)

        status = True
        return status

    def set_status_led(self, color):
        """
        Set led to expected color
        Args:
            color: A string representing the color with which to set the
                   fan module status LED
        Returns:
            bool: True if set success, False if fail.
        """
        status = False
        if self.is_cpm == 0 or self.get_presence() is False:
            return status

        channel, stub = nokia_common.channel_setup(nokia_common.NOKIA_GRPC_FAN_SERVICE)
        if not channel or not stub:
            return status
        req_idx = platform_ndk_pb2.ReqFanTrayIndexPb(fantray_idx=self.fantray_idx)
        led_info = nokia_common.led_color_to_info(color)
        ret, response = nokia_common.try_grpc(stub.SetFanLedStatus,
                                              platform_ndk_pb2.ReqFanTrayOpsPb(idx=req_idx, led_info=led_info))
        nokia_common.channel_shutdown(channel)

        status = True
        return status

    def get_status_led(self):
        """
        Gets the state of the Fan status LED

        Returns:
            A string, one of the predefined STATUS_LED_COLOR_* strings.
        """
        color = self.STATUS_LED_COLOR_OFF
        if self.is_cpm == 0 or self.get_presence() is False:
            return color

        channel, stub = nokia_common.channel_setup(nokia_common.NOKIA_GRPC_FAN_SERVICE)
        if not channel or not stub:
            return color
        req_idx = platform_ndk_pb2.ReqFanTrayIndexPb(fantray_idx=self.fantray_idx)
        ret, response = nokia_common.try_grpc(stub.GetFanLedStatus,
                                              platform_ndk_pb2.ReqFanTrayOpsPb(idx=req_idx))
        nokia_common.channel_shutdown(channel)

        if ret is False:
            return color

        color = nokia_common.led_info_to_color(response.led_info)
        return color

    def get_target_speed(self):
        """
        Retrieves the target (expected) speed of the fan
        Returns:
            An integer, the percentage of full fan speed, in the range 0 (off)
                 to 100 (full speed)
        """
        speed = 0
        if self.is_cpm == 0 or self.get_presence() is False:
            return speed

        channel, stub = nokia_common.channel_setup(nokia_common.NOKIA_GRPC_FAN_SERVICE)
        if not channel or not stub:
            return speed
        req_idx = platform_ndk_pb2.ReqFanTrayIndexPb(fantray_idx=self.fantray_idx)
        ret, response = nokia_common.try_grpc(stub.GetFanTargetSpeed,
                                              platform_ndk_pb2.ReqFanTrayOpsPb(idx=req_idx))
        nokia_common.channel_shutdown(channel)

        if ret is False:
            return speed

        speed = response.fan_speed_target.fantray_speed
        return speed

    def get_position_in_parent(self):
        """
        Retrieves 1-based relative physical position in parent device.
        Returns:
            integer: The 1-based relative physical position in parent device or
                     -1 if cannot determine the position
        """
        return -1

    def is_replaceable(self):
        """
        Indicate whether this device is replaceable.
        Returns:
            bool: True if it is replaceable.
        """
        return False
