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

    // Set indexes
    void setWriterIndex(uint16_t index);
    void setReaderIndex(uint16_t index);
    
    // Write
    void write(void* data, uint8_t len);
    void writeByte(uint8_t data);
    void writeShort(int16_t data);
    void writeUShort(uint16_t data);
    void writeInt(int32_t data);
    void writeUInt(uint32_t data);
    void writeLong(int64_t data);
    void writeULong(uint64_t data);

    // Read
    void read(void* dest, int len);
    uint8_t readByte();
    int16_t readShort();
    uint16_t readUShort();
    int32_t readInt();
    uint32_t readUInt();
    int64_t readLong();
    uint64_t readULong();
  private:
    uint8_t byteBuff[256];
    uint16_t readerIndex = 0, writerIndex = 0;
    uint16_t recvLength = -1;
};
#endif
