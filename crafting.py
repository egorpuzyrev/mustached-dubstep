#!/usr/bin/env python3
#-*- coding: utf-8 -*-

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
        #"super hammer", "mega hammer", "healing pot", "double ekac")

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
                        #~ 'double ekac': {'attack': 40, 'charges': 5},
                        'hammer': {'attack': 3, 'charges': 2},
                        'double hammer': {'attack': 10, 'charges': 1},
                        #~ 'super hammer': {'attack': 20, 'charges': 5},
                        #~ 'mega hammer': {'attack': 20, 'charges': 5},
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
