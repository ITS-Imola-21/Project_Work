import requests
import serial
import time
import json
from read_arduino import read_from_arduino

import logging
logger = logging.getLogger(__name__)

def send_temp(ser: serial.Serial, website_api: str, email_amazon: str, token: str):
    """
    Sends temperature data from Arduino to a website API.

    Args:
        ser (serial.Serial): The serial object connected to the Arduino.
        website_api (str): The URL of the website API.

    Returns:
        None

    Raises:
        Exception: If there is an error in the send_temp.py script.

    """
    try:
        if ser is not None:
            if not ser.is_open:
                ser.open()
                print("reopening the serial")
                
            #send the command to read the temperature
            ser.write(b'T')
            time.sleep(1)
            logger.info("Reading temperature from arduino for scheduled task")
            #read the data from the arduino using the read_from_arduino function
            temperature=read_from_arduino(ser,"temp")
            humidity=read_from_arduino(ser,"temp")
            heat_index=read_from_arduino(ser,"temp")
            
            status_led=read_from_arduino(ser,"led")
            if status_led=="H":
                status_led="On"
            elif status_led=="L":
                status_led="Off"
            else:
                status_led="error"
            t = time.localtime()
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
            
            #send the data to the server using the API
            logger.info("Sending temperature to the server for scheduled task")
            payload = {"email_amazon":email_amazon,
                       "token":token,
                       "id_causa":1,
                       "id_misura":2,
                       "log":f"Sent temperature to website, led {status_led}",
                       "data_time":current_time,
                       "valore_effetto": temperature}
            temperature_communication = requests.post(website_api, json=payload)
            
            payload = {"email_amazon":email_amazon,
                       "token":token,
                       "id_causa":1,
                       "id_misura":4,
                       "log":f"Sent humidity to website, led {status_led}",
                       "data_time":current_time,
                       "valore_effetto": humidity}
            humidity_communication= requests.post(website_api, json=payload)
            
            payload = {"email_amazon":email_amazon,
                       "token":token,
                       "id_causa":1,
                       "id_misura":3,
                       "log":f"Sent heatindex to website, led {status_led}",
                       "data_time":current_time,
                       "valore_effetto": heat_index}
            heat_index_communication= requests.post(website_api, json=payload)
            
            print(f"Sent temperature to {temperature_communication.url} temperature: {temperature}")
            print(temperature_communication.text)
            print(f"Sent humidity to {humidity_communication.url} humidity: {humidity}")
            print(humidity_communication.text)
            print(f"Sent heatIndex to {heat_index_communication.url} heatIndex: {heat_index}")
            print(heat_index_communication.text)
            

            #this is for debug
            #print ("Temperature: ", temperature, "Humidity: ", humidity,    "Heat Index: ", heatIndex, "Timestamp: ",  current_time)
            
        else:
            print("Serial Port Not Found when sending temperature to the server")
            logger.error("Serial Port Not Found when sending temperature to the server")
    except Exception as e:
        logger.error(f"Error in send_temp.py: {e}")