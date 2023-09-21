# -*- coding: utf-8 -*-

import json
import math
import random
import uuid
import logging
import datetime
import boto3
import requests
from zoneinfo import ZoneInfo
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

url_ngrok=""
token_database='xxxxxxxx'
url_database='http://pw2023.itsimola.it/insert.php'

def lambda_handler(request, context):
    
    try:
        global token_database
        global url_database
        global url_ngrok
        # Dump the request for logging - check the CloudWatch logs.
        if request is not None:
            print('lambda_handler request  -----')      # print in CloudWatch logs
            print(json.dumps(request))
        
        if context is not None:
            print('lambda_handler context  -----')      # print in CloudWatch logs
            print(context)
        
        # If the request contains a 'body' key, then it is a request for setting the ngrok url.
        if 'body' in request:
            json_body = json.loads(request['body'])
            if 'url' in json_body:
                # Store the ngrok url in the global variable.
                url_ngrok=json_body["url"]
                return send_response({'name':'Url received'})
            else:
                return send_response({'response':'Invalid request'})
        # If the request contains a 'directive' key, then it is a request from Alexa to control an endpoint.
        elif 'directive' in request:
            # Check the payload version.
            payload_version = request['directive']['header']['payloadVersion']
            if payload_version != '3':
                # Send an error response if the payload version is not supported.
                error_response = AlexaResponse(
                    namespace='Alexa',
                    name='ErrorResponse',
                    payload={'type': 'INTERNAL_ERROR', 'message': 'This skill only supports Smart Home API version 3'})
                return send_response(error_response.get())
        
            # Crack open the request to see the request.
            name = request['directive']['header']['name']
            namespace = request['directive']['header']['namespace']
        
            # Handle the incoming request from Alexa based on the namespace.
            
            if namespace == 'Alexa.Authorization':
                if name == 'AcceptGrant':
                    # Note: This example code accepts any grant request.
                    # In your implementation, invoke Login With Amazon with the grant code to get access and refresh tokens.
                    # Respond to AcceptGrant request from Alexa
                    grant_code = request['directive']['payload']['grant']['code']
                    grantee_token = request['directive']['payload']['grantee']['token']
                    auth_response = AlexaResponse(namespace='Alexa.Authorization', name='AcceptGrant.Response')
                    return send_response(auth_response.get())
        
            if namespace == 'Alexa.Discovery':
                if name == 'Discover':
                    # The request to discover the devices the skill controls.
                    discovery_response = AlexaResponse(namespace='Alexa.Discovery', name='Discover.Response')
                    # Create the response and add the capabilities.
                    capability_alexa = discovery_response.create_payload_endpoint_capability()
                    capability_alexa_powercontroller = discovery_response.create_payload_endpoint_capability(
                        interface='Alexa.PowerController',
                        supported=[{'name': 'powerState'}])
                    capability_alexa_powercontroller['properties']['retrievable']=True
                    capability_alexa_temperaturesensor = discovery_response.create_payload_endpoint_capability(
                        interface='Alexa.TemperatureSensor',
                        supported=[{'name': 'temperature'}])
                    capability_alexa_temperaturesensor['properties']['retrievable']=True
                    capability_alexa_endpointhealth = discovery_response.create_payload_endpoint_capability(
                        interface='Alexa.EndpointHealth',
                        supported=[{'name': 'connectivity'}])
                    # Add capabilities to the endpoint.
                    discovery_response.add_payload_endpoint(
                        friendly_name='Laptop',
                        endpoint_id='Lap1',
                        capabilities=[capability_alexa, capability_alexa_endpointhealth, capability_alexa_powercontroller])
                    # Send the discovery response back to Alexa.
                    return send_response(discovery_response.get())
        
            if namespace == 'Alexa.PowerController':
                if name == 'TurnOff':
                    # Prepare the JSON message to send to the IOT device to turn off the LED.
                    json_laptop = {"dev": "led","status":False}
                    print('json per il laptop --------')
                    print(json_laptop)
                    # Send the JSON message to the IOT device.
                    laptop_response = requests.post(url_ngrok+'/send', json=json_laptop)
                elif name == 'TurnOn':
                    # Prepare the JSON message to send to the IOT device to turn on the LED.
                    json_laptop = {"dev": "led","status":True}
                    print('json per il laptop --------')
                    print(json_laptop)
                    # Send the JSON message to the IOT device.
                    laptop_response = requests.post(url_ngrok+'/send', json=json_laptop)
                # Check if the response from the IOT device is valid.
                if ((not laptop_response) or (laptop_response == None)):
                    # If the response is not valid, send an error response back to Alexa.
                    unreachable_response = AlexaResponse(
                        namespace='Alexa',
                        name='ErrorResponse',
                        payload={'type': 'BRIDGE_UNREACHABLE', 'message': 'Unable to reach laptop.'})
                    return send_response(unreachable_response.get())
                # Parse the JSON response from the IOT device.
                json_laptop_response = json.loads(laptop_response.content)
                print('Response from laptop --------')
                print(json_laptop_response)
                value = ' '
                id_causa = '0'
                if json_laptop_response["done"]==('turned on' or 'already on'):
                    # If the LED is turned on or already on, set the response value and ID.
                    value=value.replace(' ','ON')
                    id_causa=id_causa.replace('0','2')
                elif json_laptop_response["done"]==('turned off' or 'already off'):
                    # If the LED is turned off or already off, set the response value and ID.
                    value=value.replace(' ','OFF')
                    id_causa=id_causa.replace('0','3')
                elif json_laptop_response["done"]=='error':
                    error_response = AlexaResponse(
                        namespace='Alexa',
                        name='ErrorResponse',
                        payload={'type': 'ENDPOINT_CONTROL_UNAVAILABLE', 'message': 'Arduino error'})
                    return send_response(error_response.get())
                power_response={
                      "event": {
                        "header": {
                          "namespace": "Alexa",
                          "name": "Response",
                          "messageId": str(uuid.uuid4()),
                          "correlationToken": request['directive']['header']['correlationToken'],
                          "payloadVersion": "3"
                        },
                        "endpoint": {
                          "scope": {
                            "type": "BearerToken",
                            "token": request['directive']['endpoint']['scope']['token']
                          },
                          "endpointId": "Lap1"
                        },
                        "payload": {}
                      },
                      "context": {
                            "properties": [
                              {
                                "namespace": "Alexa.PowerController",
                                "name": "powerState",
                                "value": value,
                                "timeOfSample": get_utc_timestamp(),
                                "uncertaintyInMilliseconds": 500
                              }
                            ]
                    }
                }
                print('json per il database --------')
                json_database={"email_amazon":"ITS.ProjectWork.2023@gmail.com","token":token_database,"id_causa":id_causa,"id_misura":'1',"data_time":datetime.now(tz=ZoneInfo("Europe/Berlin")).strftime('%Y-%m-%d %H-%M-%S'),"valore_effetto":value}
                print(json_database)
                database_response = requests.post(url_database, json=json_database)
                return send_response(power_response)
    
            if namespace == 'Alexa':
                if name == 'ReportState':
                    json_laptop = {"dev": "status"}
                    print('json per il laptop --------')
                    print(json_laptop)
                    laptop_response = requests.post(url_ngrok+'/read', json=json_laptop)
                    time = get_utc_timestamp()
                    if ((not laptop_response) or (laptop_response == None)):
                        unreachable_response = AlexaResponse(
                            namespace='Alexa',
                            name='ErrorResponse',
                            payload={'type': 'BRIDGE_UNREACHABLE', 'message': 'Unable to reach laptop.'})
                        return send_response(unreachable_response.get())
                    json_laptop_response = json.loads(laptop_response.content)
                    print('Response from laptop --------')
                    print(json_laptop_response)
                    if (json_laptop_response["connection"] == "open" and json_laptop_response["done"] == "ok" and json_laptop_response["status"] != "error"):
                        state_response = {
                            'event':{
                                'header': {
                                    'namespace':'Alexa',
                                    'name':'StateReport',
                                    'messageId': str(uuid.uuid4()),
                                    'correlationToken':request['directive']['header']['correlationToken'],
                                    'payloadVersion':'3'
                                },
                                'endpoint': {
                                    "scope": {
                                        "type": "BearerToken",
                                        "token":request['directive']['endpoint']['scope']['token']
                                    },
                                    "endpointId":"Lap1" 
                                },
                                'payload':{}
                            },
                            'context': {
                                "properties": [{
                                    "namespace": "Alexa.TemperatureSensor",
                                    "name": "temperature",
                                    "value": {
                                      "value": json_laptop_response["temp"],
                                      "scale": "CELSIUS"
                                    },
                                    "timeOfSample":time,
                                    "uncertaintyInMilliseconds": 1000
                                },
                                {
                                    "namespace": "Alexa.PowerController",
                                    "name": "powerState",
                                    "value": json_laptop_response["status"],
                                    "timeOfSample":time,
                                    "uncertaintyInMilliseconds": 1000
                                }]
                            }
                        }
                        print('json per il database --------')
                        json_database={"email_amazon":"ITS.ProjectWork.2023@gmail.com","token":token_database,"id_causa":'4',"id_misura":'2',"data_time":datetime.now(tz=ZoneInfo("Europe/Berlin")).strftime('%Y-%m-%d %H-%M-%S'),"valore_effetto":json_laptop_response["temp"]}
                        print(json_database)
                        database_response = requests.post(url_database, json=json_database)
                        return send_response(state_response)
                    else:
                        error_response = AlexaResponse(
                            namespace='Alexa',
                            name='ErrorResponse',
                            payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Arduino error'})
                        return send_response(error_response.get())
        else:
            invalid_response = {'response':'Invalid request'}
            return send_response(invalid_response)
    except Exception as e:
        print(f"No idea what happened: {e!r}") 
        lambda_error_response = AlexaResponse(
                    namespace='Alexa',
                    name='ErrorResponse',
                    payload={'type': 'INTERNAL_ERROR', 'message': 'Lambda function error'})
        return send_response(lambda_error_response.get())
        
    
# Send the response
def send_response(response):
    print('lambda_handler response -----')   #print in CloudWatch logs
    print(json.dumps(response))
    return response

# Datetime format for timeOfSample is ISO 8601, `YYYY-MM-DDThh:mm:ssZ`.
def get_utc_timestamp(seconds=None):
    return datetime.now(tz=ZoneInfo("Europe/Berlin")).isoformat()

class AlexaResponse:
    
    def __init__(self, **kwargs):
        # Initialize the context properties and payload endpoints lists.
        self.context_properties = []
        self.payload_endpoints = []
        
        # Set up the response structure with the given arguments.
        self.context = {}
        self.event = {
            'header': {
                'namespace': kwargs.get('namespace', 'namespace'),
                'name': kwargs.get('name', 'name'),
                'messageId': str(uuid.uuid4()),
                'payloadVersion': kwargs.get('payload_version', '3')
            },
            'endpoint': {
                "scope": {
                    "type": "BearerToken",
                    "token": kwargs.get('token', 'INVALID')
                },
                "endpointId": kwargs.get('endpoint_id', 'Lap1')
            },
            'payload': kwargs.get('payload', {})
        }
        # Set the correlation token if provided.
        if 'correlation_token' in kwargs:
            self.event['header']['correlation_token'] = kwargs.get('correlation_token', 'INVALID')
        # Set the cookie if provided.
        if 'cookie' in kwargs:
            self.event['endpoint']['cookie'] = kwargs.get('cookie', '{}')
        # Remove the endpoint property in an AcceptGrant or Discover request.
        if self.event['header']['name'] == 'AcceptGrant.Response' or self.event['header']['name'] == 'Discover.Response':
            self.event.pop('endpoint')

    def add_context_property(self, **kwargs):
        # Add a new context property to the list.
        self.context_properties.append(self.create_context_property(**kwargs))

    def add_cookie(self, key, value):
        # Add a new cookie to the endpoint property.
        if "cookies" in self is None:
            self.cookies = {}
        self.cookies[key] = value
        
    def add_payload_endpoint(self, **kwargs):
        # Add a new payload endpoint to the list.
        self.payload_endpoints.append(self.create_payload_endpoint(**kwargs))

    def create_context_property(self, **kwargs):
        # Create a new context property with the given arguments.
        return {
            'namespace': kwargs.get('namespace', 'Alexa.EndpointHealth'),
            'name': kwargs.get('name', 'connectivity'),
            'value': kwargs.get('value', {'value': 'ok'}),
            'timeOfSample': get_utc_timestamp(),
            'uncertaintyInMilliseconds': kwargs.get('uncertainty_in_milliseconds', 0)
        }
    def create_payload_endpoint(self, **kwargs):
        # Create a new payload endpoint with the given arguments.
        # All discovery responses must include the additionAttributes
        additionalAttributes = {
            'manufacturer': kwargs.get('manufacturer', 'xxxxxx'),
            'model': kwargs.get('model_name', 'xxxxxxxx'),
            'serialNumber': kwargs.get('serial_number', 'xxxxxxxxx'),
            'firmwareVersion': kwargs.get('firmware_version', 'xxxxxxx'),
            'softwareVersion': kwargs.get('software_version', 'xxxxxx'),
            'customIdentifier': kwargs.get('custom_identifier', 'xxxxxxx')
        }
        endpoint = {
            'capabilities': kwargs.get('capabilities', []),
            'description': kwargs.get('description', 'ProjectWork'),
            'displayCategories': kwargs.get('display_categories', ['OTHER']),
            'endpointId': kwargs.get('endpoint_id', 'Lap1'),
            'friendlyName': kwargs.get('friendly_name', 'Laptop'),
            'manufacturerName': kwargs.get('manufacturer_name', 'xxxxxx')
        }
        endpoint['additionalAttributes'] = kwargs.get('additionalAttributes', additionalAttributes)
        if 'cookie' in kwargs:
            endpoint['cookie'] = kwargs.get('cookie', {})
        return endpoint
    
    def create_payload_endpoint_capability(self, **kwargs):
        # Create a new payload endpoint capability with the given arguments.
        # All discovery responses must include the Alexa interface
        capability = {
            'type': kwargs.get('type', 'AlexaInterface'),
            'interface': kwargs.get('interface', 'Alexa'),
            'version': kwargs.get('version', '3')
        }
        supported = kwargs.get('supported', None)
        if supported:
            # If the 'supported' argument is provided, add the properties to the capability
            capability['properties'] = {}
            capability['properties']['supported'] = supported
            capability['properties']['proactivelyReported'] = kwargs.get('proactively_reported', False)
            capability['properties']['retrievable'] = kwargs.get('retrievable', False)
        return capability

    def get(self, remove_empty=True):
        # Get the response object, including context and event information
        response = {
            'context': self.context,
            'event': self.event
        }
        if len(self.context_properties) > 0:
            # If context properties exist, add them to the response
            response['context']['properties'] = self.context_properties
        if len(self.payload_endpoints) > 0:
            # If payload endpoints exist, add them to the response
            response['event']['payload']['endpoints'] = self.payload_endpoints
        if remove_empty:
            # If remove_empty is set to True, remove the 'context' key if it has no values
            if len(response['context']) < 1:
                response.pop('context')
        return response

    def set_payload(self, payload):
        # Set the event payload
        self.event['payload'] = payload

    def set_payload_endpoint(self, payload_endpoints):
        # Set the payload endpoint
        self.payload_endpoints = payload_endpoints

    def set_payload_endpoints(self, payload_endpoints):
        # If 'endpoints' does not exist in the event payload, add an empty list to it
        if 'endpoints' not in self.event['payload']:
            self.event['payload']['endpoints'] = []
        # Set the payload endpoints to the provided value
        self.event['payload']['endpoints'] = payload_endpoints
    
