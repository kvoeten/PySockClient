
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <SoftwareSerial.h>
#include "ByteBuf.h"

ByteBuf inPacket;
ByteBuf outPacket;
int recvLen = -1;

SoftwareSerial BTserial(7, 6); // RX | TX

#define TYPE 0x02
#define UID 0x02
#define PROGRAMMING_MODE false
#define NAME "AT+NAMESimly RS-01 0001"
#define PIN "AT+PIN1234"

// Rotary Encoder Inputs
#define CLK 2
#define DT 3
#define SW 4

// Motor outputs
#define IN1 7
#define IN2 8
#define EN1 9

// State assignable by simulation
int desiredCount = 0;

// Rotary encoder status tracker
int counter = 0;
int currentStateCLK;
int lastStateCLK;
String currentDir ="";
unsigned long lastButtonPress = 0;

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotorL = AFMS.getMotor(1);

void sendPacket() {
  // Free memory for header + packet
  uint16_t length = outPacket.size();
  uint8_t* data = (uint8_t*) malloc(length + 2);

  // Copy header + packet into new memory
  memcpy(&data[0], &length, 2);
  memcpy(&data[2], outPacket.buffer(), length);

  // Write and flush to ensure packet was sent
  BTserial.write(data, length + 2);
  BTserial.flush();

  // Also write to USB connection for non-BT
  Serial.write(data, length + 2);
  Serial.flush();

  // Reset buffer and free memory
  outPacket.clear();
  free(data);
}

void setup() {
  Serial.begin(9600);
  BTserial.begin(9600);
  delay(1000);

  // Set encoder pins as inputs
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  pinMode(SW, INPUT_PULLUP);
  lastStateCLK = digitalRead(CLK);

  // Set motor pins as outputs
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(EN1, OUTPUT);

  desiredCount = 5;
  motorRun(true);

  AFMS.begin();  // create with the default frequency 1.6KHz
}

void motorRun(bool right) {
  analogWrite(EN1, 255);  // Max Speed    
  digitalWrite(IN1, right ? HIGH : LOW);
  digitalWrite(IN2, right ? LOW : HIGH);
}

void loop() {
  #if PROGRAMMING_MODE
  // Read & Write AT Commands
  if (BTserial.available()) Serial.write(BTserial.read());
  if (Serial.available()) BTserial.write(Serial.read());
#else
  checkPacket();
  handleRotator();
  delay(1);
#endif
}

/*
 * Reads serial, might have to rewrite to have individual decoder state
 */
void checkPacket() {
  if (recvLen == -1) {
    // Check if either Serial interface has a packet available
    if (Serial.available() >= 2) {
      Serial.readBytes(inPacket.buffer(), 2);
    } else if (BTserial.available() >= 2) {
      BTserial.readBytes(inPacket.buffer(), 2);
    } else {
      // Return if no data available
      return;
    }
    
    // Read the length and clear inpacket 
    recvLen = inPacket.readUShort();
    inPacket.clear();
  }
  
  if (recvLen != -1) {
    // Check if data is available 
    if (Serial.available() >= recvLen) {
      Serial.readBytes(inPacket.buffer(), recvLen);
    } else if (BTserial.available() >= recvLen) {
      BTserial.readBytes(inPacket.buffer(), recvLen);
    } else {
      // Return if neither serial ports has (the) packet data
      return;
    }
    
    // Handle the packet
    inPacket.setWriterIndex(recvLen);
    handlePacket();

    // Clear inPacket/ encoder state
    inPacket.clear();
    recvLen = -1;
  }
}

void handlePacket() {
  desiredCount = inPacket.readInt();
  counter = 0;
  if (desiredCount > 0) {
    myMotorL->setSpeed(255);
    myMotorL->run(RELEASE);
    myMotorL->run(FORWARD);
  } else if (desiredCount < 0) {
    myMotorL->setSpeed(255);
    myMotorL->run(RELEASE);
    myMotorL->run(BACKWARD);
  }
}

void stopMotor() {
  analogWrite(EN1, 0);
  myMotorL->setSpeed(0);
  myMotorL->run(RELEASE);
}

void handleRotator() {
  currentStateCLK = digitalRead(CLK);

  // If state changes, send notification to unreal
  if (currentStateCLK != lastStateCLK  && currentStateCLK == 1){
    outPacket.writeUShort(TYPE);
    outPacket.writeUShort(UID);

    if (digitalRead(DT) != currentStateCLK) {
      // Clockwise
      outPacket.writeInt(1);
      if (desiredCount != 0) {
        counter++;
      }
    } else {
      // Counterclockwise
      outPacket.writeInt(-1);
      if (desiredCount != 0) {
        counter--;
      }
    }
    // Send off update to server
    sendPacket();
  }

  // Check if desired count has been reached
  if ( (desiredCount > 0 && counter >= desiredCount) 
  || (desiredCount < 0 && counter <= desiredCount)){
    delay(20); // ensure previous data has been sent    
    desiredCount = 0, counter = 0;
    // Send status packet (0 means no dial change)
    outPacket.writeShort(TYPE);
    outPacket.writeShort(UID);
    outPacket.writeInt(0);
    sendPacket();
    stopMotor();
  }

  // Remember last CLK state
  lastStateCLK = currentStateCLK;

  // Read the button state
  int btnState = digitalRead(SW);
  if (btnState == LOW) {
    if (millis() - lastButtonPress > 50) {
      // DoNothing atm
    }
    lastButtonPress = millis();
  }
}
