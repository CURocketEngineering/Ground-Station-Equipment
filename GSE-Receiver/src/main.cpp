#include <Arduino.h>
#include <SoftwareSerial.h>

SoftwareSerial XBee(D1, D0);

const int BUFFER_SIZE = 5;
char buffer[BUFFER_SIZE]; // Buffer to store incoming characters
int bufferIndex = 0;      // Current index in the buffer
int i = 0; 

void check_purge(char* buf);
void check_fuel(char* buf);

void setup() {
  XBee.begin(9600);
  Serial.begin(9600);
}

void loop() {
  i++;
  
  // Forward data from Serial to XBee
  if (Serial.available()) { 
    XBee.write(Serial.read());
  }
  

  // Read data from XBee and process it
  if (XBee.available()) {
    // Serial.println("Data received from XBee:");
    char receivedChar = XBee.read();

    // Echo received data to Serial
    Serial.write(receivedChar);

    // If the char is a newline, reset the buffer
    if (receivedChar == '\n') {
      bufferIndex = 0;
      return;
    }

    // Add character to buffer and check for commands
    buffer[bufferIndex++] = receivedChar;

    // If buffer is full, check for commands and reset buffer index
    if (bufferIndex >= BUFFER_SIZE) {
      check_purge(buffer);
      check_fuel(buffer);
      bufferIndex = 0;  // Reset the buffer for the next command
    }
  }
}

// Function to check if the buffer contains "purge"
void check_purge(char* buf) {
  if (strncmp(buf, "purge", BUFFER_SIZE) == 0) {
    Serial.println("Purge command detected!");
    // Add any additional action here for the "purge" command
  }
}

// Function to check if the buffer contains "fuel"
void check_fuel(char* buf) {
  if (strncmp(buf, "fuel_", BUFFER_SIZE - 1) == 0) { // "fuel" is 4 chars, no null needed
    Serial.println("Fuel command detected!");
    // Add any additional action here for the "fuel" command
  }
}
