#include "ByteBuf.h"

void ByteBuf::clear() {
  readerIndex = 0;
  writerIndex = 0;
}

int ByteBuf::size() {
  return writerIndex;
}

// Copies data into new object so buffer can be used again.
uint8_t* ByteBuf::makePacket() {
  uint16_t length = writerIndex;
  uint8_t data[length + 2];
  memcpy(&data[0], &length, 2);
  memcpy(&data[2], &byteBuff[0], length);
  return data;
}

/*
 * Writer functions
*/
void ByteBuf::write(void* data, uint8_t len) {
    memcpy(&byteBuff[writerIndex], data, len);
    writerIndex += len;
}

void ByteBuf::writeByte(uint8_t data) {
    write(&data, 1);
}

void ByteBuf::writeShort(uint16_t data) {
    write(&data, 2);
}

void ByteBuf::writeInt(uint32_t data) {
    write(&data, 4);
}

void ByteBuf::writeLong(uint64_t data) {
    write(&data, 8);
}

/*
 * Reader functions
*/
void ByteBuf::read(void* data, int len) {
    if (readerIndex + len > writerIndex) {
        return;
    }
    memcpy(data, &byteBuff[readerIndex], len);
    readerIndex += len;
}

uint8_t ByteBuf::readByte() {
    uint8_t result;
    read(&result, 1);
    return result;
}

uint16_t ByteBuf::readShort() {
    uint16_t result;
    read(&result, 2);
    return result;
}

uint32_t ByteBuf::readInt() {
    uint32_t result;
    read(&result, 4);
    return result;
}

uint64_t ByteBuf::readLong() {
    uint64_t result;
    read(&result, 8);
    return result;
}
