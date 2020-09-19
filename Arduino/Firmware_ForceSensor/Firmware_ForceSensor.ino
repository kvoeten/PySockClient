#include <SoftwareSerial.h>
#include "ByteBuf.h"

ByteBuf inPacket;
ByteBuf outPacket;

SoftwareSerial BTserial(2, 3); // RX | TX

#define TYPE 0x01
#define UID 0x01
#define PROGRAMMING_MODE false
#define NAME "AT+NAMESimly FS-01 0001"
#define PIN "AT+PIN1234"
#define pin_front A0
#define pin_back A1
#define pin_left A2
#define pin_right A3

int front = 0, back = 0;
int left = 0, right = 0;

void setup() {
  Serial.begin(9600);
  BTserial.begin(9600);
  delay(1000);
}

void loop() {
#if PROGRAMMING_MODE
  // Read & Write AT Commands
  if (BTserial.available()) Serial.write(BTserial.read());
  if (Serial.available()) BTserial.write(Serial.read());
#else
  // Read sensor values
  front = analogRead(pin_front);
  back = analogRead(pin_back);
  left = analogRead(pin_left);
  right = analogRead(pin_right);

  // Write to serial ports
  outPacket.writeShort(TYPE);
  outPacket.writeShort(UID);
  outPacket.writeInt(front);
  outPacket.writeInt(back);
  outPacket.writeInt(left);
  outPacket.writeInt(right);
  sendPacket();
  delay(100);
#endif
}

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
