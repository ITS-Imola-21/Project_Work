//those are the pins that the RGB led is connected to:
#define BLUE 3
#define GREEN 5
#define RED 6
// fading time between colors in milliseconds:
#define delayTime 15 

//this is the pin that the button is connected to:
#define button 2

//those are the pins that the potentiometers are connected to:
#define potRed A0
#define potGreen A1
#define potBlue A2

//this is the library for the DHT11 sensor:
#include "DHT.h"
//this is the pin that the DHT11 sensor is connected to:
#define DHTPIN 13
//this is the type of the DHT11 sensor:
#define DHTTYPE DHT11
//this is the setup for the DHT11 sensor:
DHT dht(DHTPIN, DHTTYPE);


//those are the commands that the python script will send to the arduino:
#define turnOn 'O'
#define turnOff 'F'
#define readTemp 'T'
//those are the commands that the arduino will send to the python script:
#define turnedOn "H"
#define turnedOff "L"
#define alreadyOn "A"
#define alreadyOff "D"


// define variables used by the RGB in the different functions
int redValue = 0;
int greenValue = 0;
int blueValue = 0;

int potRedValue = 0;
int potGreenValue = 0;
int potBlueValue = 0;

int tempRedValue = 0;
int tempGreenValue = 0;
int tempBlueValue = 0;

// this variable is used to define the sequence of the RGB led
int sequence = 0;

// this variable is used to define the state of the button
volatile bool toggle = 0;

// those variables are used to avoid the delay and keep the program running
unsigned long startMillis;
unsigned long currentMillis;


void setup()
{
    Serial.begin(9600);
     // we set the button to input with internal pullup
     // so that it is high when not pressed and not needed to use a resistor
    pinMode(button, INPUT_PULLUP);

    //set led pins to output
    pinMode(RED, OUTPUT); 
    pinMode(GREEN, OUTPUT);
    pinMode(BLUE, OUTPUT);
    //set pins to LOW so that the led is off
    digitalWrite(RED, redValue);
    digitalWrite(GREEN, greenValue);
    digitalWrite(BLUE, blueValue);
    //set potentiomenters pins to input
    pinMode(potRed, INPUT); 
    pinMode(potGreen, INPUT);
    pinMode(potBlue, INPUT);
    //set the button interrupt
    attachInterrupt(digitalPinToInterrupt(button), press, FALLING);
    //initial start time
    startMillis = millis();
    //initialize DHT11 sensor
    dht.begin();
}


// main loop
void loop()
{
    // we check if the button is pressed and toggle the state of the led
    if (toggle == 1){
        // we check the sequence of the RGB led and call the corresponding function, in this case sequence 0
        if (sequence==0){
            sequence=1;//setting sequence to 1 so that the next time it will run the next sequence
            //we call the function that turn on the led with the color changing in loop
            RGB();
        }
        else{
            // we check the sequence of the RGB led and call the corresponding function, in this case sequence 1
            if (sequence==1){
                //this will ensure that the led will turn on in tempRGB() even if we start is early
                if (currentMillis - startMillis < 60000){
                    startMillis=0;
                }
                sequence=2;//setting sequence to 2 so that the next time it will run the next sequence
                //we call the function that turn on the led with the color depending on the temperature sensor
                tempRGB();
            }
            else{
                // we check the sequence of the RGB led and call the corresponding function, in this case sequence 2
                if (sequence==2){
                    //this will check that the potentiometers are more than 5 so that the led will be turned on in potRGB()
                    potRedValue = analogRead(potRed);
                    potGreenValue = analogRead(potGreen);
                    potBlueValue = analogRead(potBlue);
                    if(potRedValue < 5 && potGreenValue < 5 && potBlueValue < 5){
                        //if the potentiometers are less than 5 we will go back to sequence 0
                        sequence=1;
                        RGB();
                    }
                    else{
                        //if the potentiometers are more than 5 we will go to sequence 2
                        sequence=0;//setting sequence to 0 so that the next time it will run the first sequence
                        //we call the function that turn on the led with the color depending on the potentiometers
                        potRGB();
                    }
                }
            }
        }
            
    }
    else{
        // if the toggle is off we turn off the led
        digitalWrite(RED, LOW);
        digitalWrite(GREEN, LOW);
        digitalWrite(BLUE, LOW);
        // we check if there is data available on the serial port
        if (Serial.available() > 0) {
            // we call the function that will receive the data
            receive_serial();
        }
    }
    
}
// this function is called when there is data available on the serial port
void receive_serial(){
    while(Serial.available()>0)
    {
        // we read the data from the serial port and store it in the variable inByte
        int inByte = Serial.read();
        switch(inByte){
            // we check if the data is a command to turn on the led
            case turnOn:
                if (toggle==0){
                    // if the led is off we turn it on
                    toggle = 1;
                    sequence = 0;
                    // we send a response to the python script to confirm that the led is turned on
                    Serial.write(turnedOn);
                }
                else{
                    // if the led is already on we send a response to the python script to inform that the led is already on
                    Serial.write(alreadyOn);
                }
                break;
            // we check if the data is a command to turn off the led
            case turnOff:
                // if the led is on we turn it off
                if (toggle==1){
                    toggle = 0;
                    Serial.write(turnedOff);
                }
                else{
                    // we send a response to the python script to confirm that the led is turned off
                    Serial.write(alreadyOff);
                }
                break;
            // we check if the data is a command to read the temperature
            case readTemp:
                // we read the temperature and send it to the python script deviding each read by a delimiter character
                float t = dht.readTemperature();
                float h = dht.readHumidity();  
                float hic = dht.computeHeatIndex(t, h, false);                      
                sendFloat(t);
                Serial.write('\n'); //send delimiter character
                sendFloat(h);
                Serial.write('\n'); //send delimiter character
                sendFloat(hic);
                Serial.write('\n'); //send delimiter character
                if (toggle==1){
                    // if the led is on we send a response to the python script to inform that the led is on
                    Serial.write(turnedOn);
                }
                else{
                    // if the led is off we send a response to the python script to inform that the led is off
                    Serial.write(turnedOff);
                }
                break;
        }
        // we wait a bit to avoid reading the same data multiple times
        delay(50);
    }
}

// this function is called to send a float number to the serial port
void sendFloat(float x){
    byte *bx = (byte*)&x; //convert float into four bytes
    for(int i=0;i<4;i++){
        Serial.write(bx[i]); //sends each byte
    }
}

// this function is the first sequence of the RGB led and it will change the color of the led in loop
void RGB(){
    // we check if the button is pressed and toggle the state of the led
    while (toggle==1 && sequence == 1){
        //we start with red on and green and blue off
        redValue = 255; // choose a value between 1 and 255 to change the color.
        greenValue = 0;
        blueValue = 0;
        
        // every change of color we check if the button is pressed and if we are in the right sequence
        while (greenValue < 255 && toggle == 1 && sequence == 1)// fades out red bring green full when i=255
        {
            // we check if there is data available on the serial port
            if (Serial.available() > 0) {
                receive_serial();
            }
            currentMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started)
            if (currentMillis - startMillis >= delayTime)
            {
                // we change the value of the red and green led to fade out the red and fade in the green
                redValue -= 1;
                greenValue += 1;
                analogWrite(RED, redValue);
                analogWrite(GREEN, greenValue);
                startMillis = currentMillis;
            }
        }
        // this will set the value of the red led to 0 and the value of the green led to 255
        redValue = 0;
        greenValue = 255;
        blueValue = 0;
        // every change of color we check if the button is pressed and if we are in the right sequence
        while(blueValue < 255 && toggle == 1 && sequence == 1) // fades out green bring blue full when i=255
        {   
            // we check if there is data available on the serial port
            if (Serial.available() > 0) {
                receive_serial();
            }
            currentMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started)
            if (currentMillis - startMillis >= delayTime)
            {
                // we change the value of the green and blue led to fade out the green and fade in the blue
                greenValue -= 1;
                blueValue += 1;
                analogWrite(GREEN, greenValue);
                analogWrite(BLUE, blueValue);
                startMillis = currentMillis;
            }
        }
        // this will set the value of the green led to 0 and the value of the blue led to 255
        redValue = 0;
        greenValue = 0;
        blueValue = 255;
        // every change of color we check if the button is pressed and if we are in the right sequence
        while(redValue < 255 && toggle == 1 && sequence == 1) // fades out blue bring red full when i=255
        {   
            // we check if there is data available on the serial port
            if (Serial.available() > 0) {
                receive_serial();
            }
            currentMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started)
            if (currentMillis - startMillis >= delayTime)
            {
                // we change the value of the blue and red led to fade out the blue and fade in the red
                blueValue -= 1;
                redValue += 1;
                analogWrite(BLUE, blueValue);
                analogWrite(RED, redValue);
                startMillis = currentMillis;
            }
        }
    }
}

// this function is the second sequence of the RGB led and it will change the color of the led based on the temperature
void tempRGB()
{
    // we check if the button is pressed and toggle the state of the led and if we are in the right sequence
    while(toggle == 1 && sequence == 2){
        // we check if there is data available on the serial port
        if (Serial.available() > 0) {
            receive_serial();
        }
        // manipulation of the value of the millis to ensure that the led is turned on even if it starts very soon
        if (currentMillis<60000){
          currentMillis=60020;
          startMillis=0;
        }
        else{
          currentMillis = millis();//get the current "time" (actually the number of milliseconds since the program started)
        }
        //every minute we read the temperature and change the color of the led based on the temperature
        if (currentMillis - startMillis >= 60000){
            // we read the temperature and change the color of the led
            float t = dht.readTemperature();
            float h = dht.readHumidity();  
            float hicf = dht.computeHeatIndex(t, h, false);
            int hic=int(round(hicf));
            // depending on the temperature we define the color of the led in this way:
            // if the temperature is below 0 the led will be blue
            if(hic<0){
                tempRedValue = 0;
                tempGreenValue = 0;
                tempBlueValue = 255;
            }
            // if the temperature is above 30 the led will be red
            else if(hic>30){
                tempRedValue = 255;
                tempGreenValue = 0;
                tempBlueValue = 0;
            }
            // if the temperature is 15 the led will be green
            else {
                // if the temperature is between 0 and 15 the led will be from blue to green
                if (hic<15){
                    tempGreenValue=map(hic,0,15,0,255);
                    tempBlueValue = map(hic,0,15,255,0);
                    tempRedValue=0;
                }
                else{
                // if the temperature is between 15 and 30 the led will be from green to red
                    tempGreenValue=map(hic,15,30,255,0);
                    tempRedValue=map(hic,15,30,0,255);
                    tempBlueValue=0;
                }
            }
            // we change the value of the led
            analogWrite(RED, tempRedValue);
            analogWrite(GREEN, tempGreenValue);
            analogWrite(BLUE, tempBlueValue);
            startMillis = currentMillis;
        }
        delay(50);
    }
}

// this function is the third sequence of the RGB led and it will change the color of the led based on the potentiometer
void potRGB(){
    // we check if the button is pressed and toggle the state of the led and if we are in the right sequence
    while(toggle == 1 && sequence == 0)
    {
        // we check if there is data available on the serial port
        if (Serial.available() > 0) {
            receive_serial();
        }
        // we read the value of the potentiometer and change the color of the led based on the value
        // the value is devided by 10 because the analog read is from 0 to 1023 and the analog write is from 0 to 255
        // this makes the led change color more smoothly
        potRedValue = analogRead(potRed)/10;
        potRedValue = map(potRedValue,0,102,0,255); //map the value of the potentiometer to the value of the led

        potGreenValue = analogRead(potGreen)/10;
        potGreenValue = map(potGreenValue,0,102,0,255);

        potBlueValue = analogRead(potBlue)/10;
        potBlueValue = map(potBlueValue,0,102,0,255);
        // we change the value of the led
        analogWrite(RED, potRedValue);
        analogWrite(GREEN, potGreenValue);
        analogWrite(BLUE, potBlueValue);

    }
}

// this function is the called when the button is pressed and it will toggle the state of the led
void press()
{
    //those variables are used to avoid the button to be pressed multiple times, it's a debouncing system
    static unsigned long last_interrupt_time = 0;
     unsigned long interrupt_time = millis();
    if ((interrupt_time - last_interrupt_time) > 200) {
        // we toggle the state of the led, from on to off and viceversa
        toggle=!toggle;
    }
    last_interrupt_time = interrupt_time;
}