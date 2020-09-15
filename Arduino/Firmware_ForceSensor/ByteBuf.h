/*
  Bytebuf.h - Library for reading/writing a bytebuffer.
  Created by Kaz Voeten, September 15, 2020.
*/
#ifndef Bytebuf_h
#define Bytebuf_h

#include "Arduino.h"

class ByteBuf {
  public:
    void clear();
    uint16_t size();
    uint8_t* buffer();
    
    // Write
    void write(void* data, uint8_t len);
    void writeByte(uint8_t data);
    void writeShort(uint16_t data);
    void writeInt(uint32_t data);
    void writeLong(uint64_t data);

    // Read
    void read(void* dest, int len);
    uint8_t readByte();
    uint16_t readShort();
    uint32_t readInt();
    uint64_t readLong();
  private:
    uint8_t byteBuff[1024];
    uint16_t readerIndex = 0, writerIndex = 0;
    uint16_t recvLength = -1;
};
#endif
