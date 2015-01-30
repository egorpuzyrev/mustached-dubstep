#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint as rnd
from random import choice
from copy import deepcopy

from my_functions import *
from consts import Const
from rooms import *
from crafting import *


class Player(object):
    def __init__(self,  map_obj, pos_x=0, pos_y=0):
        self.glob_x = pos_x
        self.glob_y = pos_y
        self.room_x = 0
        self.room_y = 0
        self.combatmode = 0
        self.collected_details = 0
        self.map_obj = map_obj


        self.stats = {'health': 30,
                      'agility': 30,
                      'strength': 20,
                      }

        self.inventory = {'flashlight': 2, 'cutting torch': 2, 'hammer': 2, 'hand': 50}
        


    def move_inside_room(self, direction):
        dx = -(ncmpr(direction, 1) + ncmpr(4, direction))
        dy = ncmpt(direction, 8) + ncmpt(2, direction)
        self.prev_room_x = self.room_x
        self.prev_room_y = self.room_y
        self.room_x += dx
        self.room_y += dy


    def move_to_room(self, direction):
        dx = -(ncmpr(direction, 1) + ncmpr(4, direction))
        dy = ncmpt(direction, 8) + ncmpt(2, direction)
        if not(dx == 0) or not(dy == 0):
            self.prev_glob_x = self.glob_x
            self.prev_glob_y = self.glob_y
            self.glob_x += dx
            self.glob_y += dy
        
        self.new_turn()
        

    def next_turn(self):
        self.inventory['cutting torch'] = 2
        self.inventory['flashlight'] = 2
        self.inventory['hand'] = 50
        if self.stats['health']>1:
            self.stats['health'] -= 1
        if self.stats['agility']>1:
            self.stats['agility'] -= 1
        if self.stats['strength']>1:
            self.stats['strength'] -= 1






class Map(object):

    def __init__(self, size_x, size_y, expandable=[-1,]):
        self.X = size_x
        self.Y = size_y
        self.bitmap = ''
        self._exp = expandable

        self.__generate_map(size_x, size_y)
        self.close_borders()
        self.__fix_all()

    def __generate_map(self, size_x, size_y):
        self.m = [[rnd(1,15) for i in range(size_x)] for j in range(size_y)]

        for i in range(1, size_y-1):
            for j in range(1, size_x-1):
                x = self.m[i][j]
                while (ncmpr(self.m[i][j-1], x) and ncmpt(self.m[i-1][j], x)):
                    x =rnd(1, 15)
                self.m[i][j] = x


    def __fix_cell(self, row=-1, column=-1):
        if not(row==-1 or column==-1):

            if not(column-1>=0):
                if ncmpr(self.m[row][column-1], self.m[row][column]):
                    self.m[row][column-1] |= 0b0100
                    self.m[row][column] |= 0b0001
            else:
                self.m[row][colimn] &= 0b1110
            
            if not(column+1<self.X):
                if ncmpr(self.m[row][column], self.m[row][column+1]):
                    self.m[row][column] |= 0b0100
                    self.m[row][colimn+1] |= 0b0001
            else:
                self.m[row-1][column] &= 0b1011
            
            if not(row-1>=0):
                if ncmpt(self.m[row-1][column], self.m[row][column]):
                    self.m[row-1][column] |= 0b0010
                    self.m[row][column] |= 0b1000
            else:
                self.m[row][column] &= 0b0111
            
            if not(row+1<self.Y):
                if ncmpt(self.m[row][column], self.m[row+1][column]):
                    self.m[row+1][column] |= 0b1000
                    self.m[row][column] |= 0b0010
            else:
                self.m[row][column] &= 0b0010


    def __fix_all(self):
        self.__fix_area(rows=range(self.Y), cols=range(self.X))

    fix_all = __fix_all

    def __fix_area(self, rows=[-1,], cols=[-1,]):
        if not(-1 in rows) and not(-1 in cols):
        
            for i in [k for k in rows if k<self.Y-1]:
                for j in range(self.X):
                    if ncmpt(self.m[i][j], self.m[i+1][j]):
                        self.m[i+1][j] |= 0b1000
                        self.m[i][j] |= 0b0010

            for i in [k for k in rows if k<self.Y]:
                for j in range(self.X-1):
                    if ncmpr(self.m[i][j], self.m[i][j+1]):
                        self.m[i][j+1] |= 0b0001
                        self.m[i][j] |= 0b0100

            for j in [k for k in cols if k<self.X-1]:
                for i in range(self.Y):
                    if ncmpr(self.m[i][j], self.m[i][j+1]):
                        self.m[i][j+1] |= 0b0001
                        self.m[i][j] |= 0b0100

            for j in [k for k in cols if k<self.X]:
                for i in range(self.Y-1):
                    if ncmpt(self.m[i][j], self.m[i+1][j]):
                        self.m[i+1][j] |= 0b1000
                        self.m[i][j] |= 0b0010


    def close_borders(self, force=0):
        if force or not(Const.W in self._exp):
            for i in range(self.Y):
                if ncmpr(0, self.m[i][0]):
                    self.m[i][0] &= 0b1110

        if force or not(Const.E in self._exp):
            for i in range(self.Y):
                if ncmpr(self.m[i][-1], 0):
                    self.m[i][-1] &= 0b1011

        if force or not(Const.N in self._exp):
            for i in range(self.X):
                if ncmpt(0, self.m[0][i]):
                    self.m[0][i] &= 0b0111

        if force or not(Const.S in self._exp):
            for i in range(self.X):
                if ncmpt(self.m[-1][i], 0):
                    self.m[-1][i] &= 0b1101



    def rebuild_bitmap(self):
        b = ''
        for i in range(self.Y):
            for j in range(3):
                for k in range(self.X):
                    b += ''.join(rooms_maps_str3[self.m[i][k]][j*3:j*3+3])
                b += '\n'

        bitmap = list(map(list, b.split('\n')))[:-1]

        for j in range(len(bitmap)):
            for i in range((len(bitmap[j])-1)//3, 0, -1):
                del(bitmap[j][i*3])

        for i in range((len(bitmap)-1)//3, 0, -1):
            del(bitmap[i*3])

        self.bitmap = [list(map(int, bitmap[i])) for i in range(len(bitmap))]



    def rebuild_modm_bitmap(self):
        b = ''
        for i in range(self.Y):
            for j in range(3):
                for k in range(self.X):
                    b += ''.join(rooms_maps_str3[self.modm[i][k]][j*3:j*3+3])
                b += '\n'

        bitmap = list(map(list, b.split('\n')))[:-1]

        for j in range(len(bitmap)):
            for i in range((len(bitmap[j])-1)//3, 0, -1):
                del(bitmap[j][i*3])

        for i in range((len(bitmap)-1)//3, 0, -1):
            del(bitmap[i*3])

        self.modm_bitmap = [list(map(int, bitmap[i])) for i in range(len(bitmap))]


    def expand(self, side=-1, count=1, sides=[]):
        rows = []
        cols = []
        if (Const.N in sides) or (side == Const.N) and (Const.N in self._exp):
            self.Y += count
            for i in range(count):
                self.m.insert(0, [rnd(1, 15) for i in range(self.X)])
            rows.extend(range(0, count+1))

        if (Const.S in sides) or (side == Const.S) and (Const.S in self._exp):
            self.Y += count
            for i in range(count):
                self.m.append([rnd(1, 15) for i in range(self.X)])
            rows.extend(range(self.Y-count-1, self.Y))

        if (Const.W in sides) or (side == Const.W) and (Const.W in self._exp):
            self.X += count
            for i in range(count):
                for i in range(self.Y):
                    self.m[i].insert(0, rnd(1, 15))
            cols.extend(range(0, count+1))

        if (Const.E in sides) or (side == Const.E) and (Const.E in self._exp):
            self.X += count
            for i in range(count):
                for i in range(self.Y):
                    self.m[i].append(rnd(1, 15))
            cols.extend(range(self.X-count-1, self.X))

        self.__fix_area(cols=cols, rows=rows)
        self.close_borders()


    def __str__(self):
        m1 = ''
        for i in range(self.Y):
            for j in range(7):
                m1 += ''.join([rooms_list[self.m[i][k]][j+1] for k in range(self.X)]) + '\n'
        return m1





class Goods(object):
    def __init__(self, map_obj, N=0):
        self.map_obj = map_obj
        self.N = N
        self.goods_map = [[0 for i in range(self.map_obj.X)] for j in range(self.map_obj.Y)]
        for i in range(self.N):
            x = rnd(0, self.map_obj.X-1)
            y = rnd(0, self.map_obj.Y-1)
            while self.goods_map[y][x]:
                x = rnd(0, self.map_obj.X-1)
                y = rnd(0, self.map_obj.Y-1)

            self.goods_map[y][x] = {'item': choice(Items.map_items_list),
                                    'coords': (rnd(0, 4), rnd(0, 4))
                                    }
        for i in range(4):
            x = rnd(0, self.map_obj.X-1)
            y = rnd(0, self.map_obj.Y-1)

            while self.goods_map[y][x]:
                x = rnd(0, self.map_obj.X-1)
                y = rnd(0, self.map_obj.Y-1)
            self.goods_map[y][x] = {'item': 'detail'+str(i+1),
                                    'coords': (rnd(0, 4), rnd(0, 4))
                                    }
        x = rnd(0, self.map_obj.X-1)
        y = rnd(0, self.map_obj.Y-1)
        while self.goods_map[y][x]:
            x = rnd(0, self.map_obj.X-1)
            y = rnd(0, self.map_obj.Y-1)
        self.goods_map[y][x] = {'item': 'reactor',
                                'coords': (1, 1)
                                }


class Monsters(object):
    
    monsters_list = ('bird', 'komar', 'kvadrat', 'turtle', 'zombie')
    
    def __init__(self, map_obj, player_obj, N=0):

        self.player_obj = player_obj
        self.map_obj = map_obj
        self.N = N
        self.monsters_map = [[0 for i in range(self.map_obj.X)] for j in range(self.map_obj.Y)]
        for i in range(self.N):
            x = rnd(0, self.map_obj.X-1)
            y = rnd(0, self.map_obj.Y-1)

            while self.monsters_map[y][x]:
                x = rnd(0, self.map_obj.X-1)
                y = rnd(0, self.map_obj.Y-1)

            self.monsters_map[y][x] = {'health' : rnd(15, 30),
                                       'agility' : rnd(15, 30),
                                       'strength' : rnd(15, 30),
                                       'sawplayer' : 0,
                                       'monster' : choice(self.monsters_list),
                                       'coords' : (rnd(0, 4), rnd(0, 4)),
                                       'id': 0
                                       }

    def move(self, x1, y1, dx=0, dy=0):
        self.monsters_map[y1][x1], self.monsters_map[y1+dy][x1+dx] = self.monsters_map[y1+dy][x1+dx], self.monsters_map[y1][x1]

    def next_turn(self, obj):
        X = self.map_obj.X
        Y = self.map_obj.Y
        
        x = self.player_obj.glob_x
        y = self.player_obj.glob_y
        
        for i in range(Y):
            for j in range(X):
                if self.monsters_map[i][j] and self.monsters_map[i][j]['sawplayer'] and not(x==j and y==i):
                    dx = 0
                    dy = 0
                    if rnd(0,1):
                        dy = (y - i)/abs(y - i)
                    else:
                        dx = (x - j)/abs(x - j)
                    self.move(j, i, dx, dy)
                    obj.Canvas1.coords(self.monsters_map[i][j]['id'], (j+dx)*180+self.monsters_map[i][j]['coords'][0]*30+15, (i+dy)*180+self.monsters_map[i][j]['coords'][1]*30+30)



