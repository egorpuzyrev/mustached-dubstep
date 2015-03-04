#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from PIL import Image, ImageTk
from random import randint as rnd
from rooms import rooms
from consts import Const
from model import *
from crafting import *
from my_functions import *



class Images(object):
    
    decorations_list = ("barrel2", "table", "plant", "balloon")
    
    def __init__(self):
        self.wall_vert_nodoor = ImageTk.PhotoImage(Image.open("resources/wall_vertical_nodoor2.png"))
        self.wall_vert_door = ImageTk.PhotoImage(Image.open("resources/wall_vertical_door2.png"))
        self.wall_horiz_nodoor = ImageTk.PhotoImage(Image.open("resources/wall_horizontal_nodoor2.png"))
        self.wall_horiz_door = ImageTk.PhotoImage(Image.open("resources/wall_horizontal_door2.png"))
        self.horiz_door = ImageTk.PhotoImage(Image.open("resources/gates_horizontal_opened1.png"))
        self.horiz_door_closed = ImageTk.PhotoImage(Image.open("resources/gates_horizontal_closed1.png"))
        self.vert_door = ImageTk.PhotoImage(Image.open("resources/gates_vertical_opened2.png"))
        self.vert_door_closed = ImageTk.PhotoImage(Image.open("resources/gates_vetrical_closed2.png"))
        
        self.black180 = ImageTk.PhotoImage(Image.open("resources/black180.png"))
        self.black150 = ImageTk.PhotoImage(Image.open("resources/black150.png"))
        
        self.player = ImageTk.PhotoImage(Image.open("resources/Hero.png"))
        
        
        self.decorations_images = {}
        self.pil_decorations_images = {}
        self.map_decorations_images = {}
        for i in self.decorations_list:
            self.pil_decorations_images[i] = Image.open("resources/decorations/"+i+".png")
            self.map_decorations_images[i] = ImageTk.PhotoImage(self.pil_decorations_images[i].resize((30,30)))
        
        
        self.items_images = {}
        self.pil_items_images = {}
        self.map_items_images = {}
        for i in Items.items_list:
            self.pil_items_images[i] = Image.open("resources/items/"+i+".png")
            self.items_images[i] = ImageTk.PhotoImage(self.pil_items_images[i].resize((60,60)))
            self.map_items_images[i] = ImageTk.PhotoImage(self.pil_items_images[i].resize((30,30)))
        self.map_items_images["reactor"] = ImageTk.PhotoImage(Image.open("resources/items/reactor.png"))
        
        
        self.pil_monsters_images = {}
        self.monsters_images = {}
        self.map_monsters_images = {}
        for i in Monsters.monsters_list:
            self.pil_monsters_images[i] = Image.open("resources/monsters/"+i+".png")
            self.monsters_images[i] = ImageTk.PhotoImage(self.pil_monsters_images[i].resize((60,60)))
            self.map_monsters_images[i] = ImageTk.PhotoImage(self.pil_monsters_images[i].resize((30,30)))


class Using(object):
    
    actions = {'flashlight': 'use_flashlight',
               'cutting torch': 'use_cutting_torch',
               'detail1': 'repair_engine',
               'detail2': 'repair_engine',
               'detail3': 'repair_engine',
               'detail4': 'repair_engine',
               'health pot': 'use_pot',
               'agility pot': 'use_pot',
               'strength pot': 'use_pot',
               'hand': 'attack',
               'mallet': 'attack',
               'hammer': 'attack',
               'double hammer': 'attack',
               'wrench': 'attack',
               'kettle': 'attack',
               'kettmer': 'attack',
               'pistol': 'attack',
               'arc welder': 'attack',
               'crowbar': 'attack',
               'wrenchmer': 'attack',
               'crowhammer': 'attack',
               'double crowhammer': 'attack'
               }

    @staticmethod
    def use(obj):
        _, item = obj.getcursel1(obj)
        if item in self.actions:
            pass

    @staticmethod
    def repair_engine(obj):

        x = obj.player_obj.glob_x
        y = obj.player_obj.glob_y

        if obj.goods_obj.goods_map[y][x] and obj.goods_obj.goods_map[y][x]['item']=='reactor':
            _, detail = obj.getcursel1(obj)
            obj.player_obj.collected_details += 1
            obj.player_obj.inventory[detail] -= 1
        if obj.player_obj.collected_details == 4:
            obj.message("YOU ARE WINNER!!!")
            obj.message("YOU ARE WINNER!!!")
            obj.message("YOU ARE WINNER!!!")
            obj.message("YOU ARE WINNER!!!")
        

    @staticmethod
    def use_flashlight(obj):
        if (obj.player_obj.inventory['flashlight']>0):
            side = 0
            if obj.player_obj.room_y==2:
                if obj.player_obj.room_x==0:
                    side = Const.W
                elif obj.player_obj.room_x==4:
                    side = Const.E

            if obj.player_obj.room_x==2:
                if obj.player_obj.room_y==0:
                    side = Const.N
                elif obj.player_obj.room_y==4:
                    side = Const.S
            
            glob_x = obj.player_obj.glob_x
            glob_y = obj.player_obj.glob_y
            
            if not(side == 0) and (obj.map_obj.modm[obj.player_obj.glob_y][obj.player_obj.glob_x] & side):
                x1 = obj.player_obj.glob_x*180 + obj.player_obj.room_x*30 + 15
                y1 = obj.player_obj.glob_y*180 + obj.player_obj.room_y*30 + 15*2

                dx = -(ncmpr(side, 1) + ncmpr(4, side))
                dy = ncmpt(side, 8) + ncmpt(2, side)
                

                x2 = x1 + 30 + 60*dx
                y2 = y1 + 30 + 60*dy

                item = obj.darkness_imgs_ids.intersection(obj.Canvas1.find_overlapping(x1, y1, x2, y2))

                if item:
                    item = item.pop()
                    obj.Canvas1.itemconfigure(item, state=tk.HIDDEN)
                    #~ obj.Canvas1.after(2000, lambda obj=obj: obj.Canvas1.itemconfigure(item, state=tk.NORMAL))
                    obj.player_obj.inventory['flashlight']-=1
                    obj.Label1.textvar.set(str(obj.player_obj.inventory['flashlight']))


                if obj.monsters_obj.monsters_map[glob_y+dy][glob_x+dx]:
                    
                    obj.monsters_obj.monsters_map[glob_y+dy][glob_x+dx]['sawplayer'] = 1


    @staticmethod
    def use_cutting_torch(obj):
        interact_with_door(obj)

    @staticmethod
    def use_pot(obj):
        _, pot = obj.getcursel1(obj)

        #~ obj.message('%s pot used' %(pot,))
        obj.player_obj.inventory[pot] -= 1
        if 'health' in Items.items_properties[pot]:
            obj.player_obj.stats['health'] += Items.items_properties[pot]['health']
            obj.message('Health is increased by %d' %(Items.items_properties[pot]['health'],))
        if 'agility' in Items.items_properties[pot]:
            obj.player_obj.stats['agility'] += Items.items_properties[pot]['agility']
            obj.message('Agility is increased by %d' %(Items.items_properties[pot]['agility'],))
        if 'strength' in Items.items_properties[pot]:
            obj.player_obj.stats['strength'] += Items.items_properties[pot]['strength']
            obj.message('Strength is increased by %d' %(Items.items_properties[pot]['strength'],))

    @staticmethod
    def attack(obj):
        x = obj.player_obj.glob_x
        y = obj.player_obj.glob_y
        if obj.monsters_obj.monsters_map[y][x]:
            cursel, weapon = obj.getcursel1(obj)
            obj.player_obj.inventory[weapon] -= 1
            
            p_health = obj.player_obj.stats['health']
            p_agility = obj.player_obj.stats['agility']
            p_strength = obj.player_obj.stats['strength']

            m_monster = obj.monsters_obj.monsters_map[y][x]['monster']
            m_health = obj.monsters_obj.monsters_map[y][x]['health']
            m_agility = obj.monsters_obj.monsters_map[y][x]['agility']
            m_strength = obj.monsters_obj.monsters_map[y][x]['strength']
            
            p_max_agility = (p_agility//100+1)*100
            m_max_agility = (m_agility//100+1)*100
            
            dice_p_agility = rnd(0, p_max_agility)
            dice_m_agility = rnd(0, m_max_agility)

            if dice_p_agility<p_agility:
                p_mul = 1
            else:
                p_mul = (p_max_agility-dice_p_agility)/(p_max_agility-p_agility)

            if dice_m_agility<m_agility:
                m_mul = 1
            else:
                m_mul = (m_max_agility-dice_m_agility)/(m_max_agility-m_agility)

            p_attack = int(p_mul*p_strength*(1-m_mul) + Items.items_properties[weapon]['attack'])
            m_health -= p_attack

            obj.message("Player damaged %s by %d; %s'shealths is %d" %(m_monster, p_attack, m_monster, m_health))

            m_attack = int(m_mul*m_strength*(1-p_mul))
            p_health -= m_attack

            obj.message("%s damaged player by %d" %(m_monster, m_attack))
            
            obj.player_obj.stats['health'] = p_health
            obj.monsters_obj.monsters_map[y][x]['health'] = m_health

            if p_health<=0:
                obj.message("Player is dead")
                obj.message("Player is dead")
                obj.message("Player is dead")
                obj.message("Player is dead")
                obj.Canvas1.after(5000, exit)

            
            if m_health<=0:
                obj.message("%s is dead" %(m_monster,))
                obj.monsters_obj.monsters_map[y][x] = 0
                monster = obj.monsters_ids.intersection(obj.Canvas1.find_overlapping(x*180+15, y*180+30, x*180+180+15, y*180+180+30))
                obj.Canvas1.delete(monster.pop())
                
                obj.player_obj.stats['health'] = p_health
                
                obj.player_obj.combatmode = 0



#~ def obj.getcursel1(obj):
    #~ cursel1 = obj.Scrolledlistbox1.curselection()
    #~ if cursel1:
        #~ item1 = obj.Scrolledlistbox1.get(cursel1[0])
        #~ return cursel1[0], item1
    #~ else:
        #~ return None, None
    #~ 
#~ def obj.getcursel2(obj):
    #~ cursel2 = obj.Scrolledlistbox2.curselection()
    #~ if cursel2:
        #~ item2 = obj.Scrolledlistbox2.get(cursel2[0])
        #~ return cursel2[0], item2
    #~ else:
        #~ return None, None

#~ def obj.message(obj.message):
    #~ obj.Message1.obj.messages.pop(0)
    #~ obj.Message1.obj.messages.append(str(obj.message))
    #~ obj.Message1.textvar.set('\n'.join(obj.Message1.obj.messages))


#~ def draw_map(obj):
    #~ X = Const.X
    #~ Y = Const.Y
#~ 
    #~ obj.vertical_gates_ids = set()
    #~ obj.horizontal_gates_ids = set()
#~ 
    #~ for i in range(obj.map_obj.Y*6):
        #~ obj.Canvas1.create_line(0, i*30+Const.Y, obj.map_obj.X*Const.X*6, i*30+Const.Y)
        #~ obj.Canvas1.create_line(i*Const.X+Const.X//2, 0, i*Const.X+Const.X//2, obj.map_obj.Y*Const.Y*6)    
#~ 
    #~ for i in range(obj.map_obj.Y):
        #~ for j in range(obj.map_obj.X):
            #~ 
            #~ if '╜' in rooms[obj.map_obj.m[i][j]]:
                #~ obj.Canvas1.create_image(j*X*6-X//2, i*Y*6+Y//2, image=obj.images.wall_vert_door, anchor=tk.NW, tags=('vertical',))
                #~ obj.vertical_gates_ids.add(obj.Canvas1.create_image(j*X*6-X//2, i*Y*6+Y*3-Y//2, image=obj.images.vert_door, anchor=tk.NW, tags=('gates_vertical','gates')))
            #~ else:
                #~ obj.Canvas1.create_image(j*X*6-X//2, i*Y*6+Y//2, image=obj.images.wall_vert_nodoor, anchor=tk.NW, tags=('vertical',))
            #~ 
            #~ if '╙' in rooms[obj.map_obj.m[i][j]]:
                #~ obj.Canvas1.create_image((j+1)*X*6-X//2, i*Y*6+Y//2, image=obj.images.wall_vert_door, anchor=tk.NW, tags=('vertical',))
            #~ else:
                #~ obj.Canvas1.create_image((j+1)*X*6-X//2, i*Y*6+Y//2, image=obj.images.wall_vert_nodoor, anchor=tk.NW, tags=('vertical',))
#~ 
            #~ if '╛' in rooms[obj.map_obj.m[i][j]]:
                #~ obj.Canvas1.create_image(j*X*6, i*Y*6, image=obj.images.wall_horiz_door, anchor=tk.NW, tags=('horizontal',))
            #~ else:
                #~ obj.Canvas1.create_image(j*X*6, i*Y*6, image=obj.images.wall_horiz_nodoor, anchor=tk.NW, tags=('horizontal',))
            #~ 
            #~ if '╕' in rooms[obj.map_obj.m[i][j]]:
                #~ obj.Canvas1.create_image(j*X*6, (i+1)*Y*6, image=obj.images.wall_horiz_door, anchor=tk.NW, tags=('horizontal',))
                #~ obj.horizontal_gates_ids.add(obj.Canvas1.create_image(j*X*6+X*3-X//2, (i+1)*Y*6, image=obj.images.horiz_door, anchor=tk.NW, tags=('gates_horizontal','gates')))
            #~ else:
                #~ obj.Canvas1.create_image(j*X*6, (i+1)*Y*6, image=obj.images.wall_horiz_nodoor, anchor=tk.NW, tags=('horizontal',))
#~ 
#~ 
    #~ obj.Canvas1.create_image(16, 31, image=obj.images.player, anchor=tk.NW, tags=('player',))
    #~ 
    #~ obj.Canvas1.lift("vertical")
    #~ obj.Canvas1.lift("gates")


#~ def draw_decorations(obj):
    #~ X = obj.map_obj.X
    #~ Y = obj.map_obj.Y
#~ 
    #~ for i in range(Y//3):
        #~ for j in range(X//3):
            #~ key = choice(list(obj.images.map_decorations_images.keys()))
            #~ obj.Canvas1.create_image(rnd(0, X-1)*180+15+rnd(0,4)*30, rnd(0, Y-1)*180+30+rnd(0,4)*30, image=obj.images.map_decorations_images[key], anchor=(tk.NW,), tags=('decoration',))
#~ 
#~ def draw_goods(obj):
    #~ X = obj.map_obj.X
    #~ Y = obj.map_obj.Y
    #~ 
    #~ obj.goods_ids = set()
    #~ 
    #~ for i in range(Y):
        #~ for j in range(X):
            #~ if obj.goods_obj.goods_map[i][j]:
                #~ item = obj.goods_obj.goods_map[i][j]
                #~ img = obj.images.map_items_images[item['item']]
                #~ obj.goods_ids.add(obj.Canvas1.create_image(j*180+item['coords'][0]*30+15, i*180+item['coords'][1]*30+30, image=img, anchor=tk.NW, tags=('item',)))
#~ 
    #~ obj.Canvas1.lift("item")
#~ 
#~ def draw_monsters(obj):
    #~ X = obj.map_obj.X
    #~ Y = obj.map_obj.Y
    #~ 
    #~ obj.monsters_ids = set()
    #~ 
    #~ for i in range(Y):
        #~ for j in range(X):
            #~ if obj.monsters_obj.monsters_map[i][j]:
                #~ monster = obj.monsters_obj.monsters_map[i][j]
                #~ img = obj.images.map_monsters_images[monster['monster']]
                #~ newid = obj.Canvas1.create_image(j*180+monster['coords'][0]*30+15, i*180+monster['coords'][1]*30+30, image=img, anchor=tk.NW, tags=('monster',))
                #~ obj.monsters_obj.monsters_map[i][j]['id'] = newid
                #~ obj.monsters_ids.add(newid)
    #~ obj.Canvas1.lift("monster")    
#~ 
#~ 
#~ def hide_map(obj):
    #~ obj.darkness_imgs_ids = set()
    #~ for i in range(obj.map_obj.Y):
        #~ for j in range(obj.map_obj.X):
            #~ obj.darkness_imgs_ids.add(obj.Canvas1.create_image(i*180, j*180+15, image=obj.images.black180, anchor=tk.NW, tags=('darkness',)))


def pick_up(obj):
    x = obj.player_obj.glob_x
    y = obj.player_obj.glob_y

    rx = obj.player_obj.room_x
    ry = obj.player_obj.room_y

    item = obj.goods_obj.goods_map[y][x]

    if item:
        if item['coords'][0]==rx and item['coords'][1]==ry:

            x1 = obj.player_obj.glob_x*180 + obj.player_obj.room_x*30 + 15
            y1 = obj.player_obj.glob_y*180 + obj.player_obj.room_y*30 + 15*2

            x2 = x1 + 30
            y2 = y1 + 30

            obj.goods_obj.goods_map[y][x] = 0

            obj.message("%s picked" %(item['item'],))
            if item['item'] in obj.player_obj.inventory:
                obj.player_obj.inventory[item['item']] += Items.items_properties[item['item']]['charges']
            else:
                obj.player_obj.inventory[item['item']] = Items.items_properties[item['item']]['charges']

            item = obj.goods_ids.intersection(obj.Canvas1.find_overlapping(x1, y1, x2, y2)).pop()
            obj.Canvas1.delete(item)
            


def interact_with_door(obj):
    side = 0
    if obj.player_obj.room_y==2:
        if obj.player_obj.room_x==0:
            side = Const.W
        elif obj.player_obj.room_x==4:
            side = Const.E
        
    if obj.player_obj.room_x==2:
        if obj.player_obj.room_y==0:
            side = Const.N
        elif obj.player_obj.room_y==4:
            side = Const.S

    x = obj.player_obj.glob_x
    y = obj.player_obj.glob_y


    if (obj.map_obj.m[y][x] & side) and (obj.player_obj.inventory['cutting torch']>0):
        
        x1 = obj.player_obj.glob_x*180 + obj.player_obj.room_x*30 + 15
        y1 = obj.player_obj.glob_y*180 + obj.player_obj.room_y*30 + 15*2

        dx = -(ncmpr(side, 1) + ncmpr(4, side))
        dy = ncmpt(side, 8) + ncmpt(2, side)


        x2 = x1 + 30 + 75*dx
        y2 = y1 + 30 + 75*dy

        if (obj.map_obj.modm[y][x] & side):
            obj.map_obj.modm[y][x] &= (~side)
            obj.map_obj.modm[y+dy][x+dx] &= (~ror(side, 2, 4))
            item_v = obj.vertical_gates_ids.intersection(obj.Canvas1.find_overlapping(x1, y1, x2, y2))
            item_h = obj.horizontal_gates_ids.intersection(obj.Canvas1.find_overlapping(x1, y1, x2, y2))
            if item_v:
                obj.Canvas1.itemconfigure(item_v.pop(), image=obj.images.vert_door_closed)
            elif item_h:
                obj.Canvas1.itemconfigure(item_h.pop(), image=obj.images.horiz_door_closed)
        else:
            obj.map_obj.modm[y][x] |= (side)
            obj.map_obj.modm[y+dy][x+dx] |= (ror(side, 2, 4))
            item_v = obj.vertical_gates_ids.intersection(obj.Canvas1.find_overlapping(x1, y1, x2, y2))
            item_h = obj.horizontal_gates_ids.intersection(obj.Canvas1.find_overlapping(x1, y1, x2, y2))
            if item_v:
                obj.Canvas1.itemconfigure(item_v.pop(), image=obj.images.vert_door)
            elif item_h:
                obj.Canvas1.itemconfigure(item_h.pop(), image=obj.images.horiz_door)
        obj.player_obj.inventory['cutting torch'] -= 1



def iface_update(obj):
    items1 = obj.Scrolledlistbox1.get(0, tk.END)
    for i in range(len(items1)):
        if (obj.player_obj.inventory[items1[i]]<=0) and not(items1[i]=='flashlight' or items1[i]=='cutting torch'):
            obj.Scrolledlistbox1.delete(i)

    items2 = obj.Scrolledlistbox2.get(0, tk.END)
    for i in range(len(items2)):
        if (obj.player_obj.inventory[items2[i]]<=0) and not(items2[i]=='flashlight' or items2[i]=='cutting torch'):
            obj.Scrolledlistbox2.delete(i)

    for i in obj.player_obj.inventory.keys():
        if (obj.player_obj.inventory[i]>0) and not(i in items1):
            obj.Scrolledlistbox1.insert(tk.END, i)
            obj.Scrolledlistbox2.insert(tk.END, i)
    
    cursel1 = obj.Scrolledlistbox1.curselection()
    
    if not cursel1:
        cursel1 = 0
        obj.Scrolledlistbox1.selection_set(0)
        select_inventory1(obj)

    cursel2 = obj.Scrolledlistbox2.curselection()
    
    if not cursel2:
        cursel2 = 0
        obj.Scrolledlistbox2.selection_set(0)
        select_inventory2(obj)

    item1 = obj.Scrolledlistbox1.get(cursel1)
    item2 = obj.Scrolledlistbox2.get(cursel2)
    
    obj.Label1.textvar.set(obj.player_obj.inventory[item1])
    obj.Label2.textvar.set(obj.player_obj.inventory[item2])
    
    obj.Label6.textvar.set(obj.player_obj.stats['health'])
    obj.Label7.textvar.set(obj.player_obj.stats['agility'])
    obj.Label8.textvar.set(obj.player_obj.stats['strength'])
    
    obj.Frame1.after(200, lambda: iface_update(obj))
    


def reveal(obj):
    x1 = obj.player_obj.glob_x*180 + obj.player_obj.room_x*30 + 15
    y1 = obj.player_obj.glob_y*180 + obj.player_obj.room_y*30 + 15
    x2 = x1 + 15
    y2 = y1 + 15
    item = obj.darkness_imgs_ids.intersection(obj.Canvas1.find_overlapping(x1, y1, x2, y2))

    if item:
        i = item.pop()
        obj.Canvas1.itemconfigure(i, state=tk.HIDDEN)
        return i
    else:
        return -1

def select_inventory1(obj):

    item = obj.Scrolledlistbox1.get(obj.Scrolledlistbox1.curselection()[0])
    current = obj.images.items_images[item]
    
    obj.message(item + ': ' + str(Items.items_properties[item]))
    
    obj.Canvas2.itemconfigure(obj.Canvas2.find_withtag('item')[0], image = current)
    obj.Label1.textvar.set(str(obj.player_obj.inventory[item]))

def select_inventory2(obj):
    item = obj.Scrolledlistbox2.get(obj.Scrolledlistbox2.curselection()[0])
    current = obj.images.items_images[item]
    obj.Canvas3.itemconfigure(obj.Canvas3.find_withtag('item')[0], image = current)
    obj.Label2.textvar.set(str(obj.player_obj.inventory[item]))


def craft(obj):
    cursel1 = obj.Scrolledlistbox1.curselection()[0]
    cursel2 = obj.Scrolledlistbox2.curselection()[0]
    item1 = obj.Scrolledlistbox1.get(cursel1)
    item2 = obj.Scrolledlistbox2.get(cursel2)
    newitem = Craft.craft(item1, item2)
    if not(item1==item2 and obj.player_obj.inventory[item1]==1) and not(obj.player_obj.inventory[item1]==0 or obj.player_obj.inventory[item2]==0):
        if newitem:
            obj.player_obj.inventory[item1] -= 1            
            obj.player_obj.inventory[item2] -= 1

            if newitem in obj.player_obj.inventory:
                obj.player_obj.inventory[newitem] += Items.items_properties[newitem]['charges']
            else:
                obj.player_obj.inventory[newitem] = 1
            obj.message("%s crafted" %(newitem,))


def use(obj):
    cursel = obj.Scrolledlistbox1.curselection()[0]
    item = obj.Scrolledlistbox1.get(cursel)
    if item in Using.actions:
        Using.__dict__[Using.actions[item]].__func__(obj)

def mv(event, obj):
    X = Const.X
    Y = Const.Y

    
    ex = obj.Canvas1.canvasx(event.x)
    ey = obj.Canvas1.canvasy(event.y)
    
    inx = (ex-obj.player_obj.glob_x*X*6-X//2)//15
    iny = (ey-obj.player_obj.glob_y*Y*6-Y)//15
    if inx>=10 or inx<=-1 or iny>=10 or iny<=-1:
        inx = obj.player_obj.room_x*2
        iny = obj.player_obj.room_y*2
    

    player = obj.Canvas1.find_withtag('player')
    glob_x = obj.player_obj.glob_x
    glob_y = obj.player_obj.glob_y
    obj.Canvas1.coords(player, (glob_x*180+inx//2*30+15, glob_y*180+iny//2*30+30))
    obj.player_obj.prev_room_x = obj.player_obj.room_x
    obj.player_obj.prev_room_y = obj.player_obj.room_y
    obj.player_obj.room_x = inx//2
    obj.player_obj.room_y = iny//2


def move_player(obj, side, dxy, newxy):

    glob_x = obj.player_obj.glob_x
    glob_y = obj.player_obj.glob_y
    if not(obj.player_obj.combatmode==1) and (obj.map_obj.modm[glob_y][glob_x] & side):
        
        obj.player_obj.prev_room_x = obj.player_obj.room_x
        obj.player_obj.prev_room_y = obj.player_obj.room_y

        obj.player_obj.prev_glob_x = obj.player_obj.glob_x
        obj.player_obj.prev_glob_y = obj.player_obj.glob_y

        obj.player_obj.glob_x += dxy[0]
        obj.player_obj.glob_y += dxy[1]
        
        obj.player_obj.room_x = newxy[0]
        obj.player_obj.room_y = newxy[1]
        player = obj.Canvas1.find_withtag('player')
        obj.Canvas1.coords(player, (obj.player_obj.glob_x*180+newxy[0]*30+15, obj.player_obj.glob_y*180+newxy[1]*30+30))
        
        obj.prev_revealed = reveal(obj)
        
        obj.message("YOU NOW AT (%d, %d)" %(obj.player_obj.glob_x, obj.player_obj.glob_y))
        
        X = obj.map_obj.X
        Y = obj.map_obj.Y
        
        obj.Canvas1.yview_moveto((obj.player_obj.glob_y*180-180+1)/(180*Y+15))
        obj.Canvas1.xview_moveto((obj.player_obj.glob_x*180-180+1)/(180*X+30))
        
        if obj.monsters_obj.monsters_map[obj.player_obj.glob_y][obj.player_obj.glob_x]:
            m_monster = obj.monsters_obj.monsters_map[obj.player_obj.glob_y][obj.player_obj.glob_x]['monster']
            m_health = obj.monsters_obj.monsters_map[obj.player_obj.glob_y][obj.player_obj.glob_x]['health']
            m_agility = obj.monsters_obj.monsters_map[obj.player_obj.glob_y][obj.player_obj.glob_x]['agility']
            m_strength = obj.monsters_obj.monsters_map[obj.player_obj.glob_y][obj.player_obj.glob_x]['strength']
            obj.message("There is monster %s with %d health, %d agility and %d strength" %(m_monster, m_health, m_agility, m_strength))
            obj.player_obj.combatmode = 1
        
        obj.player_obj.next_turn()
        obj.monsters_obj.next_turn(obj)


def oncanvas(event, obj):
    X = Const.X
    Y = Const.Y

    ex = obj.Canvas1.canvasx(event.x)
    ey = obj.Canvas1.canvasy(event.y)
    inx = (ex-obj.player_obj.glob_x*X*6-X//2)//15
    iny = (ey-obj.player_obj.glob_y*Y*6-Y)//15


def on_mousewheel(event, obj):
    obj.Canvas1.yview(tk.SCROLL, -1*int(event.delta/120), "units")
    
def on_mousewheel_up(event, obj):
    if event.delta==0:
        event.delta = 120
    obj.Canvas1.yview(tk.SCROLL, -1*int(event.delta/120), "units")

def on_mousewheel_down(event, obj):
    if event.delta==0:
        event.delta = 120
    obj.Canvas1.yview(tk.SCROLL, int(event.delta/120), "units")
    
def mask(obj):
    pass

def unmask(obj, x, y):
    pass
