#those are the libraries that are used to access the system
import os
import sys

#this is the library that will be used to create the API and the exceptions handlers
from fastapi import FastAPI, HTTPException, Depends
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

#this is the library that will be used to validate the data and to create the models
from pydantic import BaseModel,validator,BaseSettings

#this is the library that will be used to manage time
import time
#this is the library that will be used to log
import logging

#this library is used to create a scheduler that will execute a function every X time
from apscheduler.schedulers.background import BackgroundScheduler

#this library is used to import the variables from the json file
import json

    
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s[%(name)s] %(message)s',
                    filename='logging.log')

'''
The secret-config.json file must be in the same folder of the main.py file and it must have this structure:
{
    "nduration": <number>,
    "websiteAPI":"https://<>",
    "lambdaEndpoint":"https://<>",
    "email_amazon":"<email>",
    "token":"<token>"
}

here we define the variables importing the json file
'''
try:
    with open('secrets-config.json', 'r') as file:
        config = json.load(file)
        
    #this variable will be used to set the duration of the scheduler
    nduration = config['nduration']
    if nduration is None and type(nduration) is not int:
        print("nduration is not set, setting it to 60")
        logging.warning("nduration is not set, setting it to 60")
        nduration = 60
        
    #this is the API that will be used to send the data to the server
    websiteAPI =config['websiteAPI']
    if websiteAPI is None or "http" not in websiteAPI:
        logging.critical("websiteAPI is not set, exiting")
        exit("websiteAPI is not set, exiting")
        
    #this is endpoint of the lambda function that will be used to communicate with the alexa skill
    lambdaEndpoint = config['lambdaEndpoint']
    if lambdaEndpoint is None or "http" not in lambdaEndpoint:
        logging.critical("lambdaEndpoint is not set, exiting")
        exit("lambdaEndpoint is not set, exiting")
        
    #this is the email that will be used to send the data to the server
    email_amazon = config['email_amazon']
    if email_amazon is None or "@" not in email_amazon:
        logging.critical("email_amazon is not set, exiting")
        exit("email_amazon is not set, exiting")
        
    #this is the token that will be used to send the data to the server
    token = config['token']
    if token is None:
        logging.critical("token is not set, exiting")
        exit("token is not set, exiting")
        
except Exception as e:
    logging.critical(f"Error reading secret-config.json: {e}")
    exit("Error reading secret-config.json, exiting...")
  

#if you want to use templates read this https://fastapi.tiangolo.com/advanced/templates/#templates

#this is the function that will be used to send the data to the server
from send_temp import send_temp
#this is the function that will be used to connect to the arduino
from connect_serial import connect_to_arduino
#this is the function that will be used to read the data from the arduino
from read_arduino import read_from_arduino


#this is the global variable that will be used to connect to the arduino
ser=connect_to_arduino()

class Settings(BaseSettings):
    # ... The rest of our FastAPI settings

    BASE_URL = "http://localhost:8000"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"

settings = Settings()

def init_webhooks(base_url):
    """
    Initializes webhooks by updating the inbound traffic via APIs to use the public-facing ngrok URL.

    Args:
        base_url (str): The base URL to update the inbound traffic.

    Returns:
        None
    """
    pass

message_error_validation='Error validating the data received'
class Control(BaseModel):
    try:
        dev: str
        #the on off
        status: bool #https://docs.pydantic.dev/usage/types/#booleans
        
        @validator('dev')
        def dev_must_be(cls,v):
            """
            Validates the 'dev' parameter for the 'dev_must_be' function.

            Parameters:
                v (str): The value of the 'dev' parameter.

            Returns:
                str: The validated value of the 'dev' parameter.

            Raises:
                ValueError: If the 'dev' parameter is not equal to 'led'.

            Note:
                This function is a validator for the 'dev' parameter. It checks if the value of 'dev' is equal to 'led'. If the value is not 'led', a ValueError is raised. Otherwise, the value is returned.
            """
            #here we can add more devices
            if v != 'led':
                logging.warning ('dev must be led received: ' + v)
                raise ValueError('dev must be led')
            return v
        
    except Exception as e:
        logging.warning(f"{message_error_validation}: {e}")
        print(f"{message_error_validation}: {e}")
        
class ControlRead(BaseModel):
    try:
        dev: str
        
        @validator('dev')
        def dev_must_be(cls,v):
            """
            A function comment for the dev_must_be function.

            Parameters:
                cls (type): The class that the method is bound to.
                v (Any): The input value.

            Returns:
                Any: The input value if it is equal to 'status'.

            Raises:
                ValueError: If the input value is not equal to 'status'.
            """
            #here we can add more devices
            if v != 'status':
                logging.warning ('dev must be status, received: ' + v)
                raise ValueError('dev must be status')
            return v
        
    except Exception as e:
        logging.warning(f"{message_error_validation}: {e}")
        print(f"{message_error_validation}: {e}")

#this function is called when we need a current time
def get_timestamp():
    t = time.localtime()
    current_time = time.strftime("%d-%m-%Y %H:%M:%S", t)
    return current_time
       
#this is the main app    
try :
    app = FastAPI()
except Exception as e:
    logging.error(f"Error creating the app: {e}")
    print(f"Error creating the app: {e}")

#in case we activate Ngrok with pyngrok this will manage all the setup
if settings.USE_NGROK:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok, conf
    import requests
    conf.get_default().monitor_thread = False
    
    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000
    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    logging.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))
    # Update any base URLs or webhooks to use the public ngrok URL
    settings.BASE_URL = public_url
    init_webhooks(public_url)
    print ("ngrok tunnel " + public_url)
    
    #this is the payload that will be sent to the lambda function to connect to the alexa skill
    payload = {"url": public_url}
    l = requests.post(lambdaEndpoint, json=payload)
    logging.info ("Lambda response: " + str(l.status_code) + " " + str(l.text))
    
async def log_request(request: Request):
    """
    Logs the details of a request.

    Parameters:
        request (Request): The request object containing information about the request.

    Returns:
        None
    """
    #to log the body of the request we need to read it first and then log it
    body = await request.body() 
    logging.info(f"Request: {request.method} {request.url} Body: {body}")

@app.exception_handler(StarletteHTTPException)
async def log_http_exception_handler(request, exc):
    """
    Exception handler for Starlette HTTP exceptions.

    Args:
        request: The incoming request object.
        exc: The Starlette HTTP exception that occurred.

    Returns:
        The result of the `http_exception_handler` for the given request and exception.

    Raises:
        None.
    """
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.warning(f"HTTPException: {exc_str} ")
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    Exception handler for `RequestValidationError`.

    Args:
        request: The request object.
        exc: The exception object.

    Returns:
        The result of `request_validation_exception_handler`.

    Raises:
        None.
    """
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.warning(f"RequestValidationError: {exc_str})")
    return await request_validation_exception_handler(request, exc)
    
@app.on_event('startup')
async def init_data():
    """
	Initializes the data on application startup.
 
	This function is registered as an event handler for the 'startup' event in the FastAPI application. 
    It initializes the global variables 'ser', 'nduration', and 'websiteAPI'. 
    Next, it checks if the serial port is open. If it is open, it prints a message indicating that the serial port is open. 
    It then creates a scheduler using the BackgroundScheduler class from the apscheduler library. 
    The scheduler is used to periodically call the 'send_temp' function with the serial port and 'websiteAPI' as arguments. 
    The interval between calls is specified by the 'nduration' variable. 
    Finally, the scheduler is started and a message is printed indicating that the scheduler has started.
    
	Parameters:	None
 
	Returns: None
	"""
    global ser, nduration, websiteAPI, email_amazon, token
    try:
        #this is for debug and it checks if the serial port is open
        if ser is not None:
            if ser.is_open:
                print("Serial port is open")
                #this is the scheduler that will be used to send the data to the server
                scheduler = BackgroundScheduler()
                #every X seconds the function sendTemp will be called passing the serial port as an argument
                scheduler.add_job(send_temp , 'interval', seconds=nduration, args=[ser,websiteAPI,email_amazon,token])
                scheduler.start()
                print(f"Scheduler started every {nduration} seconds")
            else:
                print(f"Serial port is not open {ser}")
                logging.error(f"Serial port is not open {ser}")
        else:
            print(f"Serial port is None {ser}")
            logging.error(f"Serial port is None {ser}")
        
    except Exception as e:
        logging.error(f"Error creating the scheduler: {e}")
        print(f"Error creating the scheduler: {e}")

#this is the main page that will be used to check if the serial port is open
@app.get('/')
async def index() :
    global ser
    serial_port = "Serial Port"
    if ser is not None:
        if ser.is_open:
            return {serial_port : "Open"}
        else:
            return {serial_port : "Closed"}
    else:
        return {serial_port : "Not Found"}

@app.post('/send')
async def read_trigger(trigger_control: Control, request: Request, logger: None = Depends(log_request)):
    """
    Handles the '/send' endpoint of the API. Reads the trigger control data and performs actions based on the device and status. Sends the control data to the server if required.

    Parameters:
    - trigger_control (Control): The control data received from the client.
    - request (Request): The incoming HTTP request object.
    - logger (None, optional): The logger object for logging the request. Defaults to None.

    Returns:
    - read_control (dict): The control data after performing actions based on the trigger_control.

    Raises:
    - Exception: If there is an error in the read_trigger function.

    Notes:
    - This function assumes the global variables ser and websiteAPI are defined and accessible.
    - If ser is not None, the function will open the serial connection if it's closed, read the data from the trigger_control, perform actions based on the device and status, and return the control data.
    - If ser is None, the function will log an error and return a dictionary indicating that the serial port was not found.
    - If there is an exception during execution, the function will log the error and return None.

    """
    global ser
    #general contols
    try:
        if ser is not None:
            if not ser.is_open:
                ser.open()
                print("reopening the serial")
            if ser.is_open:   
                #get the data from the model
                read_control  ={
                    "dev": trigger_control.dev,
                    "done": "no",
                    "arduinoRead": "no data"
                }
                #if the device is the led
                if read_control['dev'] == "led":
                    read_control['status']=trigger_control.status
                    
                    #turn on the led
                    if read_control['status'] == True:
                        #send the command to turn on the led
                        ser.write(b'O')
                        #read the status of the led from the arduino
                        time.sleep(1)
                        read_control['arduinoRead']=read_from_arduino(ser,read_control['dev'])
                        
                        #if the led is on and was off before
                        if read_control['arduinoRead']=="H":
                            read_control['done']="turned on"
                        #if the led is on and was on before
                        elif read_control['arduinoRead']=="A":
                            read_control['done']="already on"
                        else :
                            read_control['done']="error"
                                
                    #if the status is off
                    if read_control['status'] == False:
                        #send the command to turn off the led
                        ser.write(b'F')
                        #read the status of the led from the arduino
                        time.sleep(1)
                        read_control['arduinoRead']=read_from_arduino(ser,read_control['dev'])
                        
                        #if the led is off and was on before
                        if read_control['arduinoRead']=="L":
                            read_control['done']="turned off"
                        #if the led is off and was off before
                        elif read_control['arduinoRead']=="D":
                            read_control['done']="already off"
                        else:
                            read_control['done']="error"
                                
                    #optional, send the data to the server
                    #payload = {'device': read_control['dev'], 'status': read_control['status'], 'done': read_control['done'], 'arduinoRead': read_control['arduinoRead'], 'timestamp': get_timestamp()}
                    #r = requests.get(websiteAPI, params=payload)
                    
                logging.info("Sent message "+str(read_control))   
                return read_control
            else:
                logging.error("Serial port is not open")
                return {"Serial Port": "Not Open"}
        else:
            logging.error("Serial port not found")
            return {"Serial Port": "Not Found"}
    except Exception as e:
        print("Error in the read_trigger function "+str(e))
        logging.error("Error in the read_trigger function "+ str(e))
        print(str(read_control))
        logging.error("Read_control :"+str(read_control))

@app.post('/read')
async def read_status(status_control: ControlRead, request: Request, logger: None = Depends(log_request)):
    """
    Handles the '/read' endpoint of the API. Reads the status control data and performs actions based on the device and status. Returns the status control data.

    Parameters:
    - status_control (ControlRead): The control data received from the client.
    - request (Request): The incoming HTTP request object.
    - logger (None, optional): The logger object for logging the request. Defaults to None.

    Returns:
    - read_control (dict): The control data after performing actions based on the status_control.

    Raises:
    - Exception: If there is an error in the read_status function.

    Notes:
    - This function assumes the global variable ser is defined and accessible.
    - If ser is not None, the function will open the serial connection if it's closed, read the temperature, humidity, heat index, and status of the LED from the Arduino, and return the control data.
    - If ser is None, the function will log an error and return a dictionary indicating that the serial port was not found.
    - If there is an exception during execution, the function will log the error and return None.

    """
    global ser
    try:
        read_control  ={
            "dev": status_control.dev,
        }
        #if the dev is the status we send the status of the led, temperature and serial conneciton
        if read_control['dev'] == "status":
            if ser is not None:
                if not ser.is_open:
                    read_control['connection']="closed"
                    print("reopening the serial")  
                    ser.open()
                if ser.is_open:
                    read_control['connection']="open"
                    
                    #this part will be used to read the temperature, humidity, heat index and status of the led
                    ser.write(b'T')
                    time.sleep(1)
                    #read the temperature from the arduino
                    read_control['temp']=round(float(read_from_arduino(ser,"temp")),2)
                    #read the humidity from the arduino
                    read_control['humidity']=round(float(read_from_arduino(ser,"temp")),2)
                    #read the heat index from the arduino
                    read_control['heatIndex']=round(float(read_from_arduino(ser,"temp")),2)
                    #read the status of the led from the arduino
                    read_control['arduinoRead']=read_from_arduino(ser,"led")
                    if read_control['arduinoRead']=="H":
                        read_control['status']="On"
                    elif (read_control['arduinoRead']=="L"):
                        read_control['status']="Off"
                    else:
                        read_control['status']="error"
                    #if there is an error in the reading of the temperature, humidity, heat index or status of the led
                    if 'error' in str(read_control['temp']) or 'error' in str(read_control['humidity']) or 'error' in str(read_control['heatIndex']) or 'error' in read_control['status']:
                        read_control['done']="error"
                        logging.error("Error reading the temperature, humidity, heat index or status of the led")
                    else :
                        read_control['done']="ok"    
                    
                logging.info("Sent message "+str(read_control))   
                return read_control                  
            else:
                logging.error("Serial port not found")
                read_control['connection']="not found"
                return read_control
    except Exception as e:
        print("Error in the read_status function "+str(e))
        print(str(read_control))
        logging.error("Error in the read_status function "+str(e))
        logging.error("Read_control :"+str(read_control))