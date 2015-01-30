#!/usr/bin/env python3
#-*- coding: utf-8 -*-


sign = lambda x: -1 if x<0 else 1
cmp = lambda a, b: (a > b) - (a < b)
cmpr = lambda left_room, right_room: True if (right_room<<2) & 0b0100 == left_room & 0b0100 else False
cmpt = lambda top_room, bottom_room: True if (top_room<<2) & 0b1000 == bottom_room & 0b1000 else False
ncmpr = lambda left_room, right_room: cmp((right_room<<2) & 0b0100, left_room & 0b0100)
ncmpt = lambda top_room, bottom_room: cmp((top_room<<2) & 0b1000, bottom_room & 0b1000)

# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))


def dxy(num):
    dx = (-1*(num&0b0001), 0, (num>>2)&0b0001, 0)
    dy = (0, (num>>1)&0b0001, 0, -1*((num>>3)&0b0001))
    return [(dx[i], dy[i]) for i in range(4) if not(dx[i]==dy[i])]

def check_integrity(m):
    checked = set()
    fifo = [(0, 0),]
    while not(len(fifo)==0):
        cur_y, cur_x = fifo.pop()
        d = dxy(m[cur_y][cur_x])
        for i in d:
            if not(((cur_y+i[1], cur_x+i[0])) in checked or ((cur_y+i[1], cur_x+i[0])) in fifo):
                fifo.append((cur_y+i[1], cur_x+i[0]))
        checked.add(tuple((cur_y, cur_x)))
    return set([(y, x) for y in range(len(m)) for x in range(len(m[0]))]) - checked
        

