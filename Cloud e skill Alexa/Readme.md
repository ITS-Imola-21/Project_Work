# Lambda Function for Alexa-Laptop Communication

This Lambda function facilitates communication between Alexa's servers and your laptop. It requires a layer because the 'requests' library is no longer supported by Amazon. Your PC is exposed via ngrok to overcome NAT issues. Alexa's servers perceive the laptop as a device capable of turning itself on and off ([Alexa Power Controller](https://developer.amazon.com/en-US/docs/alexa/device-apis/alexa-powercontroller.html)) and measuring temperature ([Alexa Temperature Sensor](https://developer.amazon.com/en-US/docs/alexa/device-apis/alexa-temperaturesensor.html)). It's important to note that Alexa's servers are unaware of the Arduino Uno connected to the laptop.

## Functionality

- The Lambda function logs all activities in AWS CloudWatch.
- Basic error handling is implemented.
- Communication with Alexa's servers is achieved using POST requests.
- The core components of this Lambda function include:
  - `lambda_handler` function, which is executed each time the Lambda function wakes up.
  - `AlexaResponse` class, defining the structure of the JSON data sent to Alexa's servers.
- If all operations are successful, data is also sent to the website's database.

## Contributors

This project was developed by:
- Federico Ghiselli
- Enrico Terzi
- Alessandro Gianstefani
- Mattia Tulipani

