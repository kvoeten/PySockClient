#include "byteBuf.h"

ByteBuf* inPacket = new ByteBuf();
ByteBuf* outPacket = new ByteBuf();

int front = A0;
int back = A1;
int left = A2;
int right = A3;

void setup() {
  Serial.begin(9600);
}

void loop() {
  outPacket->writeInt(analogRead(front));
  outPacket->writeInt(analogRead(back));
  outPacket->writeInt(analogRead(left));
  outPacket->writeInt(analogRead(right));
  
}

void sendPacket() {
   Serial.write(outPacket->makePacket(), outPacket->size() + 2);
   outPacket->clear();
}
