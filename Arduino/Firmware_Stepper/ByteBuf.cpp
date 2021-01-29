/*
*   Bytebuf.h - Library for reading/writing a bytebuffer Created by Kaz Voeten, September 15, 2020.
*   Copyright (C) 2020 Eindhoven University of Technology
*
*   This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "ByteBuf.h"

void ByteBuf::clear() {
  readerIndex = 0;
  writerIndex = 0;
}

uint16_t ByteBuf::size() {
  return writerIndex;
}

uint8_t* ByteBuf::buffer() {
  return &byteBuff[0];
}

void ByteBuf::setWriterIndex(uint16_t index) {
  writerIndex = index;
}

void ByteBuf::setReaderIndex(uint16_t index) {
  readerIndex = index;
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

void ByteBuf::writeShort(int16_t data) {
    write(&data, 2);
}

void ByteBuf::writeUShort(uint16_t data) {
    write(&data, 2);
}

void ByteBuf::writeInt(int32_t data) {
    write(&data, 4);
}

void ByteBuf::writeUInt(uint32_t data) {
    write(&data, 4);
}

void ByteBuf::writeLong(int64_t data) {
    write(&data, 8);
}

void ByteBuf::writeULong(uint64_t data) {
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

int16_t ByteBuf::readShort() {
    int16_t result;
    read(&result, 2);
    return result;
}

uint16_t ByteBuf::readUShort() {
    uint16_t result;
    read(&result, 2);
    return result;
}

int32_t ByteBuf::readInt() {
    int32_t result;
    read(&result, 4);
    return result;
}

uint32_t ByteBuf::readUInt() {
    uint32_t result;
    read(&result, 4);
    return result;
}

int64_t ByteBuf::readLong() {
    int64_t result;
    read(&result, 8);
    return result;
}

uint64_t ByteBuf::readULong() {
    uint64_t result;
    read(&result, 8);
    return result;
}
