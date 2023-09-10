import serial
import struct

import logging
logger = logging.getLogger(__name__)

def read_from_arduino(ser: serial.Serial, dev: str):
    """
    Reads data from the Arduino through a serial connection.

    Args:
        ser (serial.Serial): The serial connection to the Arduino.
        dev (str): The device type to read data from. Can be "led" or "temp".

    Returns:
        str or float: The data read from the Arduino. If the device is "led", it returns a string. If the device is "temp", it returns a float.

    Raises:
        Exception: If there is an error reading from the Arduino.

    """
    try:
        if ser.in_waiting > 0: 
            
            if dev == "led":
                #read the data from the arduino and put it in the data variable
                data = ser.read()
                # decode the data from the arduino and put it in the dataArduino variable
                data_arduino = data.decode()
                logger.info("Data from arduino: "+str(data_arduino))    
            if dev == "temp":
                #read the data from the arduino and put it in the data variable
                data = ser.readline()
                # decode the data from the arduino and put it in the dataArduino variable
                data_arduino = struct.unpack('<f', data[:4])[0]
                logger.info(f"Data from arduino: {data_arduino}")
        else:
            logger.error("No data in the buffer")
            data_arduino='error no data in the buffer'
    except Exception as e:
        logger.error(f"Error reading from arduino: {e}")
        data_arduino=f"error reading from arduino: {e}"
    finally:
        return data_arduino