#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint as rnd
from random import choice
from copy import deepcopy

from my_functions import *
from consts import Const
from rooms import *
# ~ from crafting import *


class Player(object):
    def __init__(self,  map_obj, pos_x=0, pos_y=0):
        self.glob_x = pos_x
        self.glob_y = pos_y
        self.room_x = 0
        self.room_y = 0
        self.combatmode = 0
        self.collected_details = 0
        self.map_obj = map_obj

        self.stats = {'health': 300000000,
                      'agility': 30,
                      'strength': 20,
                      }

        self.inventory = {'flashlight': 2,
                          'cutting torch': 2,
                          'hammer': 2,
                          'hand': 50
                          }


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

    """
    def rebuild_pathmap(self):
        self.path_map = [[0 for j in range(self.X)] for i in range(self.Y)]

        checked = set()
        cur_deep = 1

        fifo = [(0, 0), (-1, -1)]

        #~ while not(len(checked)==self.X*self.Y)):
        for k in range(self.X*self.Y):
            #~ while not(len(fifo)==0):
            while not(fifo and fifo[0]==(-1, -1)):
                cur_y, cur_x = fifo.pop(0)
                #~ if cur_y==cur_x==-1:
                    #~ cur_deep += 1
                d = dxy(self.m[cur_y][cur_x])
                for i in d:
                    if not((cur_y+i[1], cur_x+i[0]) in checked or (cur_y+i[1], cur_x+i[0]) in fifo):
                        self.path_map[cur_y+i[1]][cur_x+i[0]] += cur_deep
                        fifo.append((cur_y+i[1], cur_x+i[0]))
                checked.add(tuple((cur_y, cur_x)))
            fifo.append((-1, -1))
            cur_deep+=1
            if fifo and fifo[0]==(-1, -1):
                fifo.pop(0)

        for i in range(self.Y):
            # ~ for j in range(self.X):
            print(self.path_map[i])

        print("PATH_MAP BUILDED")

        # ~ return set([(y, x) for y in range(len(m)) for x in range(len(m[0]))]) - checked
    """


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
                                       'tk_id': 0
                                       }

    def move(self, x1, y1, dx=0, dy=0):
        self.monsters_map[y1][x1], self.monsters_map[y1+dy][x1+dx] = self.monsters_map[y1+dy][x1+dx], self.monsters_map[y1][x1]
        # ~ self.monsters_map[y1+dy][x1+dx].append(self.monsters_map[y1][x1].pop(n))

    def multipathfind(self, x2, y2, coords_list):
        print("MULTIPATHFINDING")
        path_map = [[0 for j in range(self.map_obj.X)] for i in range(self.map_obj.Y)]

        checked = set()
        cur_deep = 1

        fifo = [(y2, x2), (-1, -1)]

        while not(all([i in checked for i in coords_list]) and (y2, x2) in checked):
            while not(fifo and fifo[0]==(-1, -1)):
                cur_y, cur_x = fifo.pop(0)

                d = dxy(self.map_obj.m[cur_y][cur_x])
                for i in d:
                    if not((cur_y+i[1], cur_x+i[0]) in checked or (cur_y+i[1], cur_x+i[0]) in fifo):
                        path_map[cur_y+i[1]][cur_x+i[0]] += cur_deep
                        fifo.append((cur_y+i[1], cur_x+i[0]))
                checked.add(tuple((cur_y, cur_x)))
            fifo.append((-1, -1))
            cur_deep+=1
            if fifo and fifo[0]==(-1, -1):
                fifo.pop(0)
            

        sum_dxy = {}
        for k in coords_list:
            sum_dx = 0
            sum_dy = 0
            cur_x = k[1]
            cur_y = k[0]

            for i in range(Const.MONSTERS_SPEED):
                for j in dxy(self.map_obj.modm[cur_y][cur_x]):
                    if 0 < path_map[cur_y+j[1]][cur_x+j[0]] < path_map[cur_y][cur_x]:
                        if not self.monsters_map[cur_y+j[1]][cur_x+j[0]]:
                            # ~ path.append((cur_y+j[1], cur_x+j[0]))
                            cur_y += j[1]
                            cur_x += j[0]
                        else:
                            break
            sum_dx = cur_x - k[1]
            sum_dy = cur_y - k[0]
            sum_dxy[k] = (sum_dy, sum_dx)
            # ~ print("SUM_DXY: ", sum_dxy)
        print("MULTIPATHFOUND")
        return sum_dxy


    def walk(self, x1, y1, x2, y2):
        # ~ integrity = check_integrity(self.map_obj.modm, x0=x2, y0=y2)
# ~
        # ~ if not((y1, x1) in integrity):
        path_map = [[0 for j in range(self.map_obj.X)] for i in range(self.map_obj.Y)]

        checked = set()
        cur_deep = 1

        fifo = [(y2, x2), (-1, -1)]

        while not((y1, x1) in checked and (y2, x2) in checked):
            while not(fifo and fifo[0]==(-1, -1)):
                cur_y, cur_x = fifo.pop(0)

                d = dxy(self.map_obj.m[cur_y][cur_x])
                for i in d:
                    if not((cur_y+i[1], cur_x+i[0]) in checked or (cur_y+i[1], cur_x+i[0]) in fifo):
                        path_map[cur_y+i[1]][cur_x+i[0]] += cur_deep
                        fifo.append((cur_y+i[1], cur_x+i[0]))
                checked.add(tuple((cur_y, cur_x)))
            fifo.append((-1, -1))
            cur_deep+=1
            if fifo and fifo[0]==(-1, -1):
                fifo.pop(0)

        # ~ path = []

        sum_dx = 0
        sum_dy = 0
        cur_x = x1
        cur_y = y1

        for i in range(Const.MONSTERS_SPEED):
            for j in dxy(self.map_obj.modm[cur_y][cur_x]):
                if path_map[cur_y+j[1]][cur_x+j[0]] <= path_map[cur_y+j[1]][cur_x+j[0]] < path_map[cur_y][cur_x]:
                    # ~ path.append((cur_y+j[1], cur_x+j[0]))
                    cur_y += j[1]
                    cur_x += j[0]
        sum_dx = cur_x - x1
        sum_dy = cur_y - y1

        return sum_dx, sum_dy


    def next_turn(self, obj):
        print("MONSTERS NEXT TURN")
        X = self.map_obj.X
        Y = self.map_obj.Y

        x = self.player_obj.glob_x
        y = self.player_obj.glob_y
        print("MONSTERS WALKING")
        integrity = check_integrity(self.map_obj.modm, x0=x, y0=y)
        # ~ monsters_sawpalayer = [self.monsters_map[i][j] if not(self.monsters_map[i][j]==0) and self.monsters_map[i][j]['sawplayer'] and not(x==j and y==i) for i in range(Y) for j in range(X)]
        monsters_sawplayer = []
        for i in range(Y):
            for j in range(X):
                if not(self.monsters_map[i][j]==0) and self.monsters_map[i][j]['sawplayer'] and not(x==j and y==i):
                    if not (i, j) in integrity:
                        # ~ monsters_sawplayer.append(self.monsters_map[i][j])
                        monsters_sawplayer.append((i, j))
                    else:
                        sum_dx = 0
                        sum_dy = 0
                        y1 = i
                        x1 = j


                        for i in range(1, Const.MONSTERS_SPEED-1):
                            d = dxy(self.map_obj.modm[y1+sum_dy][x1+sum_dx])
                            direction = choice(d)
                            # ~ dirs.append(direction)
                            sum_dx += direction[0]
                            sum_dy += direction[1]

                        obj.Canvas1.coords(self.monsters_map[i][j]['tk_id'],
                            (j+sum_dx)*180+self.monsters_map[i][j]['coords'][0]*30+15,
                            (i+sum_dy)*180+self.monsters_map[i][j]['coords'][1]*30+30
                        )

                        self.move(j, i, sum_dx, sum_dy)
                        # ~ if (j+sum_dx==x and i+sum_dy==y):
                            # ~ self.player_obj.combatmode = 1

        # ~ print("MONSTERS_SAWPLAYER: ", len(monsters_sawplayer))
        obj.message("MONSTERS_SAWPLAYER: %s" %(len(monsters_sawplayer), ))
        multipath = self.multipathfind(x, y, monsters_sawplayer)
        # ~ print("MULTIPATH: ", multipath)

        for i in range(Y):
            for j in range(X):
                if not(self.monsters_map[i][j]==0) and self.monsters_map[i][j]['sawplayer'] and not(x==j and y==i):
                    if (i, j) in multipath:
                        # ~ print("SHOULD MOVE")
                        sum_dx = multipath[(i, j)][1]
                        sum_dy = multipath[(i, j)][0]
                        

                        if not(self.monsters_map[i+sum_dy][j+sum_dx]):

                            print("SUM_DX %d, SUM_DY %d" %(sum_dx, sum_dy))
                            
                            obj.Canvas1.coords(self.monsters_map[i][j]['tk_id'],
                                (j+sum_dx)*180+self.monsters_map[i][j]['coords'][0]*30+15,
                                (i+sum_dy)*180+self.monsters_map[i][j]['coords'][1]*30+30
                            )

                            self.move(j, i, sum_dx, sum_dy)
                            # ~ if (j+sum_dx==x and i+sum_dy==y):
                                # ~ self.player_obj.combatmode = 1

        print("DONE")

class Craft(object):
    @classmethod
    def craft(self, item1, item2):
        if not(item1 in self.recipes) or not(item2 in self.recipes[item1]):
            return None
        else:
            return self.recipes[item1][item2]

    recipes = {'flashlight': {'cutting torch': 'health pot'},
               'mallet': {'flashlight': 'strength pot'},
               'cutting torch': {'mallet': 'agility pot'},
               'mallet': {'wrench': 'cake'},
               'wrench': {'mallet': 'ekac'},
               'ekac': {'ekac': 'double ekac'},
               'kettle': {'hammer': 'kettmer'},
               'wrench': {'hammer': 'wrenchmer'},
               'hammer': {'hammer': 'double hammer'},
               'crowbar': {'hammer': 'crowhammer'},
               'crowhammer': {'crowhammer': 'double crowhammer'},
               'double hammer': {'double hammer': 'super hammer'},
               'super hammer': {'super hammer': 'mega hammer'},
               'mega nammer': {'mega hammer': 'healing pot'},
               'Y': {'O': 'YO'},
               'YO': {'B': 'YOB'},
               'YOB': {'A': 'YOBA'},
               'kettle': {'hammer': 'pistol'},
               'A': {'B': 'AB'},
               'AB': {'O': 'ABO'},
               'ABO': {'Y': 'ABOY'},
               'YOBA': {'ABOY', 'piece of friendship'}
               }


class Items(object):
    items_list = ("flashlight", "cutting torch", "mallet",
                  "hammer", "double hammer", "wrench", "cake", "ekac",
                  "health pot", "agility pot", "strength pot",
                  "kettle", "kettmer", "pistol", "arc welder", "crowbar",
                  "wrenchmer", "crowhammer", "double crowhammer",
                  "Y", "O", "B", "A", "YO", "YOB", "YOBA", "AB", "ABO",
                  "ABOY", "hand", "detail1", "detail2", "detail3",
                  "detail4"
                  )
        # ~ "super hammer", "mega hammer", "healing pot", "double ekac")

    map_items_list = ("mallet", "hammer", "wrench", "health pot",
                      "agility pot", "strength pot", "kettle", "pistol",
                      "arc welder", "crowbar", "Y", "O", "B", "A"
                      )

    items_properties = {'reactor': {'charges': 1},
                        'detail1': {'charges': 1},
                        'detail2': {'charges': 1},
                        'detail3': {'charges': 1},
                        'detail4': {'charges': 1},
                        'flashlight': {'attack': 0},
                        'cutting torch': {'attack': 0},
                        'hand': {'attack': 1, 'charges': 50},
                        'mallet': {'attack': 2, 'charges': 2},
                        'wrench': {'attack': 2, 'charges': 2},
                        'cake': {'attack': 3, 'health': +4, 'charges': 1},
                        'ekac': {'attack': 4, 'health': +5, 'charges': 1},
                        'arc welder': {'attack': 15, 'charges': 1},
                        'crowbar': {'attack': 3, 'charges': 2},
                        'crowhammer': {'attack': 8, 'charges': 1},
                        'double crowhammer': {'attack': 16, 'charges': 1},
                        # ~ 'double ekac': {'attack': 40, 'charges': 5},
                        'hammer': {'attack': 3, 'charges': 2},
                        'double hammer': {'attack': 10, 'charges': 1},
                        # ~ 'super hammer': {'attack': 20, 'charges': 5},
                        # ~ 'mega hammer': {'attack': 20, 'charges': 5},
                        'health pot': {'health': +5, 'charges': 1},
                        'agility pot': {'agility': +5, 'charges': 1},
                        'strength pot': {'strength': +5, 'charges': 1},
                        'kettle': {'attack': 2, 'charges': 2},
                        'pistol': {'attack': 12, 'charges': 2},
                        'piece of friendship': {'heal': 100, 'charges': 1},
                        'Y': {'charges': 1},
                        'O': {'charges': 1},
                        'B': {'charges': 1},
                        'A': {'charges': 1},
                        'YO': {'charges': 1},
                        'YOB': {'charges': 1},
                        'YOBA': {'attack': 40, 'charges': 1},
                        'A': {'charges': 1},
                        'AB': {'charges': 1},
                        'ABO': {'charges': 1},
                        'ABOY': {'attack': 40, 'charges': 1}
                        }
