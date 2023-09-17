# Project-work ITS Imola 2021-23 - IoT - API

## Description

This is the part of the project that runs all the code needed to control the Arduino and the API that interacts with it and communicate with the AWS lambda function (connected to Alexa) and the Project website.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the server without Ngrok](#running-the-server-without-ngrok)
  - [Running the server with Ngrok](#running-the-server-with-ngrok)
- [Credits](#credits)
- [License](#license)

## Requirements

The auto recognition of the serial port is tested only on Windows and Linux.
If you have macOS you need to edit the code in **connect_serial.py** in the function **find_arduino()**.

This software is written in Python and uses [FastAPI](https://fastapi.tiangolo.com/) with [uvicorn](https://www.uvicorn.org/), [pySerial](https://pythonhosted.org/pyserial/) and [pyngrok](https://pyngrok.readthedocs.io/en/latest/index.html). 
To install the required packages, follow the instructions in the *README.md* file located in the **Python_Environments** folder and use the **requirements.txt** file.

In order to use this script, you need to create a `secret-config.json` file in the same folder as the `main.py` file. The `secret-config.json` file should have the following structure:

```json
{
    "nduration": "<number>",
    "websiteAPI":"https://<>",
    "lambdaEndpoint":"https://<>",
    "email_amazon":"<email>",
    "token":"<token>"
}
```

Here's an explanation of each key in the secret-config.json file:

- `nduration`: This is a number that specifies the refresh timing (in seconds) of the temperature data sent to the website. For example, if you set nduration to 60, the script will send temperature data to the website every 60 seconds.
- `websiteAPI`: This is the URL where the website exposes the API that will receive the temperature data. Replace the <> with the actual API URL.
- `lambdaEndpoint`: This is the URL of the endpoint where the AWS Lambda function is exposed. Replace the <> with the actual Lambda endpoint URL.
- `email_amazon`: This is the email address used as an identifier by the website API to authenticate access. Replace \<email> with your actual email address that will be matched with the emails in the website database.
- `token`: This is the token used as an identifier by the website API to authenticate access. Replace \<token> with your actual token that will be matched with the tokens in the website database.
  
Make sure to replace the placeholders with the actual values needed for your specific use case.
  
## Installation

1. To use this project, first ensure you have the required dependencies installed as described in the [Requirements](#requirements) section.

2. Clone the repository to your local machine.

## Usage

To run the server, use uvicorn. You can use uvicorn with the default settings or personalize it. You can also use Ngrok to create a tunnel and expose the server to the internet.

### Running the server without Ngrok

Open the command prompt, `cd` to this directory, and type the following:

- to start the server with live update:

```bash
(<env_name>)uvicorn main:app --reload
```

The default ip is <http://127.0.0.1:8000> so you can go there and you will receive the status of the serial conenction.

If you want to test it you can go to <http://127.0.0.1:8000/docs> and use the interactive documentation provided by uvicorn.

- To run the server without live update and with different ip and/or port:

```bash
(<env_name>)uvicorn main:app --host <IP> --port <PORT>
```

### Running the server with Ngrok

- First you need to create a free account on <https://ngrok.com>

- If you don't have ngrok already installed on your system then initialize uvicorn with ngrok, it will install all the required software in the right place:

**Important: Make sure you are in your virtual enviroment!**

- Using Command Prompt:

```bash
C:\>(<env_name>)set USE_NGROK=True
C:\>(<env_name>)uvicorn main:app --reload
```

- Using Powershell:

```powershell
(<env_name>)PS C:\>$env:USE_NGROK="True"
(<env_name>)PS C:\>uvicorn main:app --reload
```

- Using Linux terminal:

```bash
(<env_name>)$ export USE_NGROK=True
(<env_name>)$ uvicorn main:app --reload
```

- After you are sure the server is running, **stop it** and add the authtoken using this command that you find on your [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken):

```bash
ngrok config add-authtoken <YOUR TOKEN>
```

In this way you can use Ngrok without the need to start it manually every time and the tunnel will be forwarded to the AWS lambda function automatically.

## Credits

- [Matteo Kevin Gardi](https://github.com/MaKeG0)
- [Alessandro Boschetti](https://github.com/alessandroboschetti)

## License

MIT License

Copyright (c) 2023 Matteo Kevin Gardi, Alessandro Boschetti

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
