##########################################################################################################################

# RoboCore MMA8452Q Library (MicroPython) (v1.0)

# Library to use the MMA8452Q accelerometer.

# Copyright 2023 RoboCore.
# Written by Luan.F (17/11/2023).
# Based on the Python library by RoboCore ( https://github.com/RoboCore/RoboCore_MMA8452Q_Python ).

# Notice: three (3) functions ("read_byte_data", "read_i2c_block_data", "write_byte_data") 
# from the "micropython-smbus" library ( https://github.com/gkluoe/micropython-smbus ), 
# created by @gkluoe, were incorporated. These functions were added to make registers easier to read.


# This file is part of the MMA8452Q library ("MMA8452Q-MicroPython-lib").

# "MMA8452Q-MicroPython-lib" is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# "MMA8452Q-MicroPython-lib" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with "MMA8452Q-MicroPython-lib". If not, see <https://www.gnu.org/licenses/>

##########################################################################################################################

# Necessary libraries
import time

# Constants

# MMA8452Q Register Map
MMA8452Q_STATUS = 0x00 # Data status Register
MMA8452Q_OUT_X_MSB = 0x01 # Output Value X MSB
MMA8452Q_OUT_X_LSB = 0x02 # Output Value X LSB
MMA8452Q_OUT_Y_MSB = 0x03 # Output Value Y MSB
MMA8452Q_OUT_Y_LSB = 0x04 # Output Value Y LSB
MMA8452Q_OUT_Z_MSB = 0x05 # Output Value Z MSB
MMA8452Q_OUT_Z_LSB = 0x06 # Output Value Z LSB
MMA8452Q_SYSMOD = 0x0B # System mode Register
MMA8452Q_INT_SOURCE = 0x0C # System Interrupt Status Register
MMA8452Q_WHO_AM_I = 0x0D # Device ID Register
MMA8452Q_XYZ_DATA_CFG = 0x0E # Data Configuration Register
MMA8452Q_CTRL_REG1 = 0x2A # Control Register 1
MMA8452Q_CTRL_REG2 = 0x2B # Control Register 2
MMA8452Q_CTRL_REG3 = 0x2C # Control Register 3
MMA8452Q_CTRL_REG4 = 0x2D # Control Register 4
MMA8452Q_CTRL_REG5 = 0x2E # Control Register 5
MMA8452Q_CFG_HPF_OUT = 0x10 # Output Data High-Pass Filtered
MMA8452Q_ASLP_RATE_50 = 0x00 # Sleep mode rate = 50Hz
MMA8452Q_ASLP_RATE_12_5 = 0x40 # Sleep mode rate = 12.5Hz
MMA8452Q_ASLP_RATE_6_25 = 0x80 # Sleep mode rate = 6.25Hz
MMA8452Q_ASLP_RATE_1_56 = 0xC0 # Sleep mode rate = 1.56Hz

# FastRead
MMA8452Q_FAST_READ_OFF = 0 # Enable fast read
MMA8452Q_FAST_READ_ON = 1 # Disable fast read

# Mode
MMA8452Q_MODE_NORMAL = 0x00 # Normal Mode
MMA8452Q_MODE_LNLP = 0x01 # Low Noise Low Power
MMA8452Q_MODE_HIGH_RES = 0x02 # High Resolution
MMA8452Q_MODE_LOW_POWER = 0x03 # Low Power

# ODR
MMA8452Q_ODR_800 = 0 # Output Data Rate = 800Hz
MMA8452Q_ODR_400 = 1 # Output Data Rate = 400Hz
MMA8452Q_ODR_200 = 2 # Output Data Rate = 200Hz
MMA8452Q_ODR_100 = 3 # Output Data Rate = 100Hz
MMA8452Q_ODR_50 = 4 # Output Data Rate = 50Hz
MMA8452Q_ODR_12 = 5 # Output Data Rate = 12.5Hz
MMA8452Q_ODR_6 = 6 # Output Data Rate = 6.25Hz
MMA8452Q_ODR_1 = 7 # Output Data Rate = 1.56Hz

# Scale
MMA8452Q_SCALE_2G = 2 # Full-Scale Range = 2g
MMA8452Q_SCALE_4G = 4 # Full-Scale Range = 4g
MMA8452Q_SCALE_8G = 8 # Full-Scale Range = 8g

# SYSMOD
MMA8452Q_SYSMOD_STANDBY = 0x00 # STANDBY
MMA8452Q_SYSMOD_WAKE = 0x01 # WAKE
MMA8452Q_SYSMOD_SLEEP = 0x02 # SLEEP

# Class
class MMA8452Q:
    """This class was created to facilitate the use of the MMA8452Q accelerometer"""

    def __init__(self, bus, address = 0x1D):
        """This method is the constructor of the class

        :param address [int]: the address of the device in the I2C bus
        """
        self.__bus = bus
        self.__address = address
        self.__fast_read = MMA8452Q_FAST_READ_OFF

    def active(self):
        """This method sets the Active mode

        Note: It is not possible to get confirmation of writing data directly
        """

        c = self.read_byte_data(
            self.__address, MMA8452Q_CTRL_REG1)

        self.write_byte_data(self.__address, MMA8452Q_CTRL_REG1, (c | 0x01))

    def available(self):
        """This method checks if new data is available

        return: 1 if a new set of data is avaible, 0 otherwise [int]
        """

        c = self.read_byte_data(
            self.__address, MMA8452Q_STATUS)
        c &= 0x08
        return (c >> 3)

    def getFastRead(self):
        """This method gets the read mode

        return: 1 if the mode is set to fast read, 0 otherwise [int]
        """

        c = self.read_byte_data(
            self.__address, MMA8452Q_CTRL_REG1)
        c &= 0x02
        c >>= 1

        return c

    def getHighPassOutput(self):
        """This method checks if the High-Pass Output is enabled

        return: 1 if the high-pass filter is on, 0 otherwise [int]
        """

        c = self.read_byte_data(
            self.__address, MMA8452Q_XYZ_DATA_CFG)
        c &= 0x10

        return (c >> 4)

    def getMode(self, sleep_mode):
        """This method gets the current Oversampling Mode

        :param sleep_mode [bool]: true for sleep mode

        return: the oversampling mode [int]
        """

        c = self.read_byte_data(
            self.__address, MMA8452Q_CTRL_REG2)
        if sleep_mode:
            c &= 0x18
            return (c >> 3)

        else:
            return (c & 0x03)

    def getODR(self):
        """This method gets the Output Data Rate

        return: the ODR [int]
        """

        c = self.read_byte_data(
            self.__address, MMA8452Q_CTRL_REG1)
        c &= 0x38

        return (c >> 3)

    def getScale(self):
        """This method gets the current Full Scale Range

        return: the scale [int]
        """

        c = self.read_byte_data(
            self.__address, MMA8452Q_XYZ_DATA_CFG)
        c &= 0x03

        return c

    def getState(self):
        """This method gets the current System Mode 

        return: the system mode [int]
        """
       
        c = self.read_byte_data(
            self.__address, MMA8452Q_SYSMOD)

        return c

    def init(self, scale=8, odr=1):
        """This method initializes the module

        :param scale [int]: the scale to configure
        :param odr [int]: the output data rate to configure

        return: 0 on invalid signature, 1 otherwise [int]
        """

        # check the device identification (should always be 0x2A)
        who_am_i = self.read_byte_data(
            self.__address, MMA8452Q_WHO_AM_I)

        if who_am_i != 0x2A:
            return 0

        self.standby() # must be in standby to change registers
        
        self.setScale(scale) # set up accelerometer scale
        self.setODR(odr) # set up output data rate

        self.active() # set to active to start reading

        return 1

    def read(self):
        """This method reads the acceleration data"""
        
        factor = 1.0 / self.__scale
        
        if self.__fast_read == MMA8452Q_FAST_READ_OFF:
            factor *= 2048.0  # 12 bits resolution

            # read the six (0 to 5) raw data records in the data array
            rawData = self.read_i2c_block_data(self.__address,  MMA8452Q_OUT_X_MSB, 6)

            self.raw_x = ((rawData[0] << 8) | rawData[1]) >> 4
            if self.raw_x > 2047:
                self.raw_x -= 4096

            self.raw_y = ((rawData[2] << 8) | rawData[3]) >> 4
            if self.raw_y > 2047:
                self.raw_y -= 4096

            self.raw_z = ((rawData[4] << 8) | rawData[5]) >> 4
            if self.raw_z > 2047:
                self.raw_z -= 4096

        else: 
            factor *= 128.0  # 8 bits resolution

            # read the three (0 to 2) raw data records in the data array
            rawData = self.read_i2c_block_data(self.__address,  MMA8452Q_OUT_X_MSB, 3)

            self.raw_x = (rawData[0] << 8) >> 8
            self.raw_y = (rawData[1] << 8) >> 8
            self.raw_z = (rawData[2] << 8) >> 8
    
        self.x = round(self.raw_x / factor, 2)
        self.y = round(self.raw_y / factor, 2)
        self.z = round(self.raw_z / factor, 2)


    def setFastRead(self, fs):
        """This method sets the read mode
        
        :param fs [int]: true to enable the fast read mode

        Note: It is not possible to get confirmation of writing data directly
        """

        # check if in standby mode
        if self.getState() != MMA8452Q_SYSMOD_STANDBY:
            return 0xFF
        
        ctrl = self.read_byte_data(
            self.__address, MMA8452Q_CTRL_REG1)

        if bool(fs):
            ctrl |= 0x02

        else:
            ctrl &= 0xFD
  
        self.write_byte_data(self.__address, MMA8452Q_CTRL_REG1, ctrl)

        self.__fast_read = fs

    def setHighPassOutput(self, set):
        """This method sets the High-Pass Output

        :param [bool]: true to enable the high-pass filter

        Note: It is not possible to get confirmation of writing data directly
        """
        
        # check if in standby mode
        if self.getState() != MMA8452Q_SYSMOD_STANDBY:
            return 0xFF
        
        cfg = self.read_byte_data(
            self.__address, MMA8452Q_XYZ_DATA_CFG)

        if bool(set):
            cfg |= 0x10
        else:
            cfg &= 0xEF

        self.write_byte_data(self.__address, MMA8452Q_XYZ_DATA_CFG, cfg)

    def setMode(self, mode, sleep):
        """This method sets the Oversampling Mode

        :param mode [int]: the oversampling mode to set
        :param sleep [bool]: true to select the sleep mode

        Note: It is not possible to get confirmation of writing data directly
        """

        # check if in standby mode
        if self.getState() != MMA8452Q_SYSMOD_STANDBY:
            return 0xFF

        toset = mode
        ctrl = self.read_byte_data(
            self.__address, MMA8452Q_CTRL_REG2)
        if(sleep):
            ctrl &= 0xE7  # mask out SMOD bits
            ctrl |= (toset << 3)

        else:
            ctrl &= 0xFC  # mask out MOD bits
            ctrl |= toset

        self.write_byte_data(self.__address, MMA8452Q_CTRL_REG2, ctrl)

    def setODR(self, odr, sleep = False):
        """This method sets the Outuput Data Rate

        :param odr [int]: the output data rate to set
        :param sleep [bool]: true to select the sleep mode

        Note: It is not possible to get confirmation of writing data directly
        """

        # check if in standby mode
        if self.getState() != MMA8452Q_SYSMOD_STANDBY:
            return 0xFF

        toset = odr
        ctrl = self.read_byte_data(
            self.__address, MMA8452Q_CTRL_REG1)
        if(sleep):
            toset &= 0xFF # mask out ASLP data rate bits
            ctrl &= 0x3F
            ctrl |= (toset << 6)

        else:
            ctrl &= 0xC7 # mask out data rate bits
            ctrl |= (toset << 3)
        
        self.write_byte_data(self.__address, MMA8452Q_CTRL_REG1, ctrl)

    def setScale(self, fsr):
        """This method sets the Full Scale Range

        :param fsr [int]: the full scale range to set

        Note: It is not possible to get confirmation of writing data directly
        """

        # check if in standby mode
        if self.getState() != MMA8452Q_SYSMOD_STANDBY:
            return 0xFF
        
        cfg = self.read_byte_data(
            self.__address, MMA8452Q_XYZ_DATA_CFG)
        cfg &= 0xFC
        cfg |= (fsr >> 2)
        self.write_byte_data(self.__address, MMA8452Q_XYZ_DATA_CFG, cfg)
        
        self.__scale = fsr

    def standby(self):
        """This method sets the Standby mode

        Note: It is not possible to get confirmation of writing data directly
        """
        
        c = self.read_byte_data(
            self.__address, MMA8452Q_CTRL_REG1)
        self.write_byte_data(self.__address, MMA8452Q_CTRL_REG1, (c & 0xFE))
    
    # micropython-smbus library function
    def read_byte_data(self, addr, register):
        """ Read a single byte from register of device at addr
            Returns a single byte """

        return self.__bus.readfrom_mem(addr, register, 1)[0]
    
    # micropython-smbus library function
    def read_i2c_block_data(self, addr, register, length):
        """ Read a block of length from register of device at addr
            Returns a bytes object filled with whatever was read """
        return self.__bus.readfrom_mem(addr, register, length)
    
    # micropython-smbus library function
    def write_byte_data(self, addr, register, data):
        """ Write a single byte from buffer `data` to register of device at addr
            Returns None """

        # writeto_mem() expects something it can treat as a buffer
        if isinstance(data, int):
            data = bytes([data])
        
        return self.__bus.writeto_mem(int(addr), int(register), data)



# DEBUG #
# this condition will only be True if the file is executed directly
if __name__ == "__main__":
    from time import sleep
    from machine import Pin, I2C

    i2c = I2C(scl=Pin(22), sda=Pin(21))

    accel = MMA8452Q(i2c, 0x1D)
    accel.init() # initialize the accelerometer with default parameters (8G and 400 Hz)
    
    #print(accelerometer.getFastRead())
    
    while True:
        accel.read()
        print(f'| X : {accel.x} ({accel.raw_x}) ', end=" ")
        print(f'| Y : {accel.y} ({accel.raw_y}) ', end=" ")
        print(f'| Z : {accel.z} ({accel.raw_z}) ')
        sleep(0.25)