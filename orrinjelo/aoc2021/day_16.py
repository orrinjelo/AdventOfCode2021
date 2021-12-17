from orrinjelo.utils.decorators import timeit
import numpy as np
import sys

def hex_to_bin(s):
    lut = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
    }
    b = ''
    for c in s.strip():
        b += lut[c]

    return b

VERBOSE = False

# Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
# Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
# Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
# Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
# Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
# Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
# Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.

class Packet():
    @staticmethod
    def parse(s, i=0):
        version = int(s[i:i+3], 2)
        type_id = int(s[i+3:i+6], 2)
        return Packet.packetType[type_id](s, version, type_id, i)

    def version_sum(self):
        vs = self.version
        for sub in self.sub_packets:
            vs += sub.version_sum()

        return vs

class LiteralValuePacket(Packet):
    def __init__(self, s, version, type_id=4, start_bit=0, consume_word=False, indent=0):
        self.version = version
        if VERBOSE: print(f'VER: {self.version}')
        self.start_bit = start_bit
        self.type_id = type_id
        if VERBOSE: print(f'TID: {self.type_id}')

        stop = False
        bit = start_bit + 6
        num = ''
        while not stop:
            b = s[bit]
            num += s[bit+1:bit+5]
            if VERBOSE: print(f'STP: {b}')
            if VERBOSE: print(f'VAL: {num} ({int(num, 2)})')
            if b == '0':
                stop = True
            bit += 5
        
        if consume_word:
            while bit % 4 != 0:
                bit += 1

        self.end_bit = bit

        self.value = int(num, 2)

        self.sub_packets = []
        self.length = self.end_bit - self.start_bit
        self.size = self.length

        # if VERBOSE: print(f'LVPacket: {self}')

    def __str__(self):
        return f'Version: {self.version}\nStart bit: {self.start_bit}\nType ID: {self.type_id}\n' \
                f'End bit: {self.end_bit}\nValue: {self.value}\nLength: {self.length}'

class OperatorPacket(Packet):
    def __init__(self, s, version, type_id, start_bit=0, indent=0):
        self.version = version
        if VERBOSE: print(f'VER: {self.version}')
        self.type_id = type_id
        if VERBOSE: print(f'TID: {self.type_id}')
        self.start_bit = start_bit

        bit = start_bit + 6

        self.length_id = int(s[bit])
        if VERBOSE: print(f'LID: {self.length_id}')
        bit += 1
        if self.length_id == 0:
            self.length = int(s[bit:bit+15],2) # 15 bits
        elif self.length_id == 1:
            self.length = int(s[bit:bit+11],2) # 11 bits
        if VERBOSE: print(f'LEN: {self.length}')

        self.estimated_size = self.length + 6 + (15 if self.length_id == 0 else 11)
        self.sub_packets = []
        
        bit = bit + (15 if self.length_id == 0 else 11)
        tot_len = 0
        while tot_len < self.length:
            # print(self.start_bit, self.length, tot_len, self.estimated_size, bit)
            if self.length_id == 0:
                if bit-self.start_bit >= self.estimated_size:
                    break

            self.sub_packets.append(Packet.parse(s, bit))
            bit = self.sub_packets[-1].end_bit
            if self.length_id == 0:
                tot_len += self.sub_packets[-1].size
            else:
                tot_len += 1

        self.end_bit = bit
        self.size = self.end_bit - self.start_bit

        self.value = 0

        # if VERBOSE: print(f'\nOPacket: \n{self}')

    def __str__(self):
        return f'Version: {self.version}\nStart bit: {self.start_bit}\nType ID: {self.type_id}\n' \
                f'End bit: {self.end_bit}\nLength ID: {self.length_id}\nLength: {self.length}\n'


class SumPacket(OperatorPacket):
    def __init__(self, s, version, type_id, start_bit=0, indent=0):
        super().__init__(s, version, type_id, start_bit, indent)

        self.value = sum([x.value for x in self.sub_packets])
        if VERBOSE: print(f'VAL: {self.value}')

class ProductPacket(OperatorPacket):
    def __init__(self, s, version, type_id, start_bit=0, indent=0):
        super().__init__(s, version, type_id, start_bit, indent)

        self.value = 1
        for x in self.sub_packets:
            self.value *= x.value
        if VERBOSE: print(f'VAL: {self.value}')

class MinPacket(OperatorPacket):
    def __init__(self, s, version, type_id, start_bit=0, indent=0):
        super().__init__(s, version, type_id, start_bit, indent)

        self.value = min([x.value for x in self.sub_packets])
        if VERBOSE: print(f'VAL: {self.value}')

class MaxPacket(OperatorPacket):
    def __init__(self, s, version, type_id, start_bit=0, indent=0):
        super().__init__(s, version, type_id, start_bit, indent)

        self.value = max([x.value for x in self.sub_packets])
        if VERBOSE: print(f'VAL: {self.value}')

class GtPacket(OperatorPacket):
    def __init__(self, s, version, type_id, start_bit=0, indent=0):
        super().__init__(s, version, type_id, start_bit, indent)

        self.value = 1 if self.sub_packets[0].value > self.sub_packets[1].value else 0
        if VERBOSE: print(f'VAL: {self.value}')

class LtPacket(OperatorPacket):
    def __init__(self, s, version, type_id, start_bit=0, indent=0):
        super().__init__(s, version, type_id, start_bit, indent)

        self.value = 1 if self.sub_packets[0].value < self.sub_packets[1].value else 0
        if VERBOSE: print(f'VAL: {self.value}')

class EqualPacket(OperatorPacket):
    def __init__(self, s, version, type_id, start_bit=0, indent=0):
        super().__init__(s, version, type_id, start_bit, indent)

        self.value = 1 if self.sub_packets[0].value == self.sub_packets[1].value else 0
        if VERBOSE: print(f'VAL: {self.value}')

Packet.packetType = {
    0: SumPacket,
    1: ProductPacket,
    2: MinPacket,
    3: MaxPacket,
    4: LiteralValuePacket,
    5: GtPacket,
    6: LtPacket,
    7: EqualPacket
}

@timeit("Day 14 Part 1")
def part1(input_str, use_rust=False):
    if VERBOSE: print(f'Input: {input_str}')
    s = hex_to_bin(input_str[0] if type(input_str) == list else input_str)
    if VERBOSE: print(f'Input: {s}')
    p = Packet.parse(s)

    return p.version_sum()

@timeit("Day 14 Part 2")
def part2(input_str, use_rust=False):
    s = hex_to_bin(input_str[0] if type(input_str) == list else input_str)
    p = Packet.parse(s)
    return p.value




# = Test ================================================

inputlist1 = [
]

def test_part1():
    s = hex_to_bin('D2FE28')
    p = Packet.parse(s)

    assert p.version == 6
    assert p.type_id == 4
    assert p.value == 2021


    s = hex_to_bin('38006F45291200')
    p = Packet.parse(s)
 
    assert p.version == 1
    assert p.type_id == 6
    assert p.length_id == 0
    assert p.length == 27
    assert len(p.sub_packets) == 2
    assert p.sub_packets[0].value == 10
    assert p.sub_packets[1].value == 20


    s = hex_to_bin('EE00D40C823060')
    p = Packet.parse(s)

    assert p.version == 7
    assert p.type_id == 3
    assert p.length_id == 1
    assert p.length == 3
    assert p.sub_packets[0].value == 1
    assert p.sub_packets[1].value == 2
    assert p.sub_packets[2].value == 3


    assert part1('8A004A801A8002F478') == 16
    assert part1('620080001611562C8802118E34') == 12
    assert part1('C0015000016115A2E0802F182340') == 23
    assert part1('A0016C880162017C3686B18A3D4780') == 31

def test_part2():
    assert part2('C200B40A82') == 3

import pygame
import sys
from pygame import gfxdraw


def plot(input_str):
    pass