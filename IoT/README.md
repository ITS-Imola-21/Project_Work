# Project-work ITS Imola 2021-23 - IoT - Overview

## Description

This the introduction to the IoT project which is divided into two main parts:

- [Arduino](Arduino/)
- [API](API/)

The [Arduino part](Arduino/README.md) has it's own documentation in it's directory, as well the [API part](API/README.md), this is just an introduction.

To help you understand it better, here are some flowcharts that provide additional context to the rest of the documentation and code.

## Table of Contents

- [Complete flowchart of the IoT project](#complete-flowchart-of-the-iot-project)
- [Arduino](#arduino)
- [Alexa-Arduino](#alexa-arduino)
- [Telemetry](#telemetry)
- [Credits](#credits)
- [License](#license)

## Complete flowchart of the IoT project

This comprehensive flowchart depicts the primary steps directly involved in the IoT section of the project.

Due to its complexity, it has been divided into three parts.

```mermaid
graph TB
    subgraph Arduino
        RGB{RGB Functions}
        S{Serial.}
        L[LED]
        T[Temperature Sensor]
        POT[Potentiometers]
        BTN[Button]

        BTN-.->|On/Off/Sequence|RGB
        POT-.->RGB
        RGB-.->L
        T-.->RGB

    end
    subgraph API
        F{FastAPI Server}
        TEL{Telemetry}
        
        SER{PySerial}
    end

    N([Ngrok Tunnel])
    A{{AWS Lambda}}
    W{{Website}}
    AL{{Alexa}}

    AL -.->|Temp?/On/Off| A
    -.->|Temp?/On/Off| N
    -.-> |Temp?/On/Off|F
    -->|Temp?/On/Off|SER
    -->|Temp?/On/Off|S 
    -->|Temp?|T
    -->|Temp|S
    S -->|On/Off|L
    -->|Feedback|S
    -->|Temp/Feedback|SER
    -->|Temp/Feedback|F
    ---->|Temp/Feedback|A
    -.->|Temp/Feedback|AL
    
    
    TEL -->|Temp?&On?/Off?| SER
    -->|Temp&Feedback|TEL
    -->|Temp&Feedback|W


```

## Arduino

The Arduino code has some inherent functionalities. The flowchart below displays them.
You can find more dettails in the [Arduino part](Arduino/README.md).

```mermaid
graph TB
    subgraph Arduino
        L[LED]
        T[Temperature Sensor]
        BTN[Button]

        subgraph Potentiometers
            POTR[Potentimeter RED]
            POTG[Potentimeter GREEN]
            POTB[Potentimeter BLUE]
        end
    
        subgraph RGBFunctions
            SEQ1{Sequence 1/On}
            SEQ2{Sequence 2}
            SEQ3{Sequence 3}
            OFF{Off}

        end

        BTN -->|On/Off/Sequence|RGBFunctions

        SEQ1 --->|On Rainbow|L

        SEQ2 <-.->|Temp|T
        SEQ2 -->|On Temp/Color|L

        SEQ3 -.->|Potentiometers?|Potentiometers
        POTR -.->|RED|SEQ3
        POTG -.->|GREEN|SEQ3
        POTB -.->|BLUE|SEQ3
        SEQ3 -->|On Potentiometers/Color|L

        OFF -->|Off|L
    end
```

## Alexa-Arduino

This flowchart primarily shows the functionality of the Alexa-Arduino, which is the main part of the whole project.
You can find more dettails in the [API part](API/README.md).

```mermaid
graph TB
    subgraph Arduino
        S{Serial.}
        L[LED]
        T[Temperature Sensor]
    end

    subgraph API
        F{FastAPI Server}
        SER{PySerial}
    end

    N([Ngrok Tunnel])
    A{{AWS Lambda}}
    AL{{Alexa}}

    AL -.->|Temp?/On/Off| A
    -.->|Temp?/On/Off| N
    -.-> |Temp?/On/Off|F
    -->|Temp?/On/Off|SER
    -->|Temp?/On/Off|S 
    -->|Temp?|T
    -->|Temp|S
    S -->|On/Off|L
    -->|Feedback|S
    -->|Temp/Feedback|SER
    -->|Temp/Feedback|F
    --->|Temp/Feedback|A
    -.->|Temp/Feedback|AL

```

## Telemetry

Here is a flowchart of the Telemetry part of the IoT part of the project.
You can find more dettails in the [API part](API/README.md).

```mermaid
graph TB
    subgraph Arduino
        S{Serial.}
        L[LED]
        T[Temperature Sensor]
    end

    subgraph API
        TEL{Telemetry}
        SER{PySerial}
    end

    W{{Website}}

    
    TEL -->|Temp?&On?/Off?| SER
    -->|Temp?&On?/Off?|S 
    -->|Temp?|T
    -->|Temp|S
    S -->|On?/Off?|L
    -->|Feedback|S
    -->|Temp&Feedback|SER
    -->|Temp&Feedback|TEL
    -->|Temp&Feedback|W

```

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