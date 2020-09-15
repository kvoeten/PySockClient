#include "ByteBuf.h"

ByteBuf inPacket;
ByteBuf outPacket;

#define pin_front A0
#define pin_back A1
#define pin_left A2
#define pin_right A3
#define HUMAN true

int front = 0, back = 0;
int left = 0, right = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  front = analogRead(pin_front);
  back = analogRead(pin_back);
  left = analogRead(pin_left);
  right = analogRead(pin_right);
#if HUMAN
  Serial.print("Sensor values: L(");
  Serial.print(left);
  Serial.print("), R(");
  Serial.print(right);
  Serial.print(")");
  Serial.println("");
  delay(1000);
#else
  outPacket.writeInt(front);
  outPacket.writeInt(back);
  outPacket.writeInt(left);
  outPacket.writeInt(right);
  sendPacket();
  delay(10);
#endif
}

void sendPacket() {
  // Free memory for header + packet
  uint16_t length = outPacket.size();
  uint8_t* data = (uint8_t*) malloc(length + 2);

  // Copy header + packet into new memory
  memcpy(&data, &length, 2);
  memcpy(&data[2], outPacket.buffer(), length);

  // Write and flush to ensure packet was sent
  Serial.write(data, outPacket.size() + 2);
  Serial.flush();

  // Release memory and reset buffer
  free(data);
  outPacket.clear();
}
