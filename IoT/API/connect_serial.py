import serial
#https://pyserial.readthedocs.io/en/latest/tools.html#module-serial.tools.list_ports
import serial.tools.list_ports 
import time
import os

import logging
logger = logging.getLogger(__name__)

#using this code you can find the port of the arduino in Windows
#https://github.com/WaveShapePlay/ArduinoPyserialComConnect
def find_arduino()->str|None:
    """
    Finds the Arduino port from the list of found ports depending on the operating system.
    
    Parameters:
        ports_found (list): A list of ports found by the system.
    
    Returns:
        str: The Arduino port if found, or None if no Arduino port is found.
    """
    try:
        ports_found=serial.tools.list_ports.comports()
        if len(ports_found) == 0:
            logger.error("No ports found len=0")
            print("No ports found len=0")
            return None
        #checking if the operating system is windows
        if os.name == 'nt':
            for port in ports_found:
                if r'Arduino' in str(port):
                    # it needs to split the string to get the port as it will -
                    # be something like this: COM3 - Arduino and we need only the COM3
                    comm_port = str(port).split(' ')[0]
                    print(comm_port)
                    logger.info(f"Found Arduino on port: {comm_port}")
                    return comm_port
        elif os.name == 'posix':
            #in case the operating system is not windows
            for port in ports_found:
                if r'ttyACM' in port.name or r'Arduino' in port.manufacturer:
                    print(f"{port.device}")
                    logger.info(f"Found Arduino on port: {port.device}")
                    return str(port.device)                
        logger.error(f"No Arduino port found {ports_found}")
        print(f"No Arduino port found {ports_found}")
        return None
   
    except Exception as e:
        logger.error("Error finding Arduino port: "+str(e))
        print("Error finding Arduino port: "+str(e))


def connect_to_arduino()->serial.Serial|None:
    """
    Connects to an Arduino device using the specified Arduino port.

    Args:
        arduino_port (str): The port to connect to the Arduino. Defaults to the result of `find_arduino(get_ports())`.

    Returns:
        serial.Serial or str: The serial connection to the Arduino if successful, otherwise 'None'.
    """
    arduino_port = find_arduino()
    #this is for debug
    if arduino_port is not None:
        try :
            #this is the serial port that will be used to connect to the arduino
            #the baudrate is the speed of the serial port and
            print("Opening the serial port at startup")
            logger.info("Opening the serial port at startup")
            ser=serial.Serial(arduino_port , 9600, timeout = 1)
            #sleep for 2 seconds to let the arduino enter in the serial mode
            time.sleep(2)
        except serial.SerialException as e :
            #this is for debug
            if 'Access is denied' in str(e):
                print(f"Arduino port is in use at startup {e}")
                logger.critical(f"Arduino port is in use at startup {e}")
            else:
                print(f"Arduino not found at startup {e}")
                logger.critical(f"Arduino not found at startup {e}")
            return None
        except Exception as e:
            #this is for debug
            print(f"Error opening the serial port at startup {e}")
            logger.critical(f"Error opening the serial port at startup {e}")
            return None
        else :
            #this is the return of the function if everything is ok
            logger.info("Arduino connected at startup")
            return ser
    else:
        # in case the arduino is not found return None
        logger.critical("Arduino not found at startup")
        return arduino_port