# making the candies web game in terminal
import time
import threading

class Player(object):
    def __init__(self, farm):
        self.candies = 0
        self._inventory = {} 
        self.timer = Timer(1, self.increment_candy)
        self.timer.start()
        self.farm = farm
        self.symbol = '\o/'
        self.quest = False
        self._commands = []

    @property
    def all_commands(self):
        """dictionary of commands and their function and price thresholds """
        return {'check candies':(self.check_candy, True), 
                'inventory':(self.get_inventory, True),
                'check farm':(self.show_farm, self._inventory!= {}),
                'throw 10 candies on the ground':(self.throw_candy, self.candies > 10),
                'eat all the candies':(self.eat_candy, True),
                'buy a lollipop': (self.buy('lollipop'), self.candies>price.get('lollipop')),
                'buy a wooden sword': (self.buy('wooden sword'), self.candies > price.get('wooden sword')),
                'plant a lollipop': (self.plant('lollipop'), self._inventory.has_key('lollipop')),
                'go on a quest': (self.go_quest, self._inventory.has_key('wooden sword')),
                'peaceful forest': (self.start_quest('peaceful forest'), self.quest), 
                'mount goblin': (self.start_quest('mount goblin'), self.quest),
                'underwater cave': (self.start_quest('underwater cave'), self.quest),
                'buy a fish': (self.buy('fish'), price.get('fish')) }
             
    @property
    def commands(self):
        """available actions if their criteria is met""" 
        return [ command for command, value in self.all_commands.items() if value[1]==True ]

    def get_inventory(self):
        if self._inventory:
            for key, quantity in self._inventory.items():
                if quantity > 0:
                    print key 
                    print quantity
                    show_ascii(key, quantity)
        else:
            print "your inventory is empty"
     
    def set_inventory(self, item, quantity):
        if item in self._inventory:
           self._inventory[item] += 1
        else:
           self._inventory[item] = 1

    def do_command(self, command):
        """get the func from dictionary. execute func"""
        self.all_commands.get(command)[0]()
       
    def check_candy(self):
        print "you have %s candies" %self.candies

    def throw_candy(self):
        self.candies = self.candies - 10

    def eat_candy(self):
        self.candies = 0

    def increment_candy(self):
        self.candies += 1

    def buy(self, item_name):
        def buy_stuff():
            self.candies = self.candies - price.get(item_name)
            self.set_inventory(item_name,1)
            print "thanks for buying!"
            print "here's your %s for %d candies" %(ascii.get(item_name), price.get(item_name))
            print "''''''''''''''''''''''''''''''''''''''''''''''''''"
            print "here's your current inventory"
            self.get_inventory() 
        return buy_stuff 

    def plant(self, item_name):
        def plant_things():
            self.farm.plant(item_name)
            self._inventory[item_name] -= 1
            print " go check out your farm! " 
        return plant_things

    def show_farm(self):
        print self.farm

    def go_quest(self):
        avai_quests = [ k for k in quest_lookup.keys() ] 
        self.quest = True
        print " choose a quest to go on ! " 
        print '* '+ '\n* '.join(avai_quests)
    
    def start_quest(self, quest_name):
        def _quest():
            quest = Quest( quest_name, self)
            quest.start()
            self.play()
        return _quest

    def show_menu(self):
        print"'''''''''''''''''''''''''''''''''''''''''''''''''"
        print"~~~available actions:~~~~"
        if self.candies > 10:
              show_ascii('merchant')
        print '* '+ '\n* '.join(self.commands)

    def play(self):
        command = raw_input(">  ")
        if command in self.commands:
            print"'''''''''''''''''''''''''''''''''''''''''''''''''''"
            self.do_command(command)  
            self.show_menu()
        else:
            print 'that action is not available. try again'
           
def show_ascii(name, quantity=1):
    print (ascii.get(name) + '\n')* quantity

"""info look-up ascii art + price + growth rates as factor of 1 second"""
lookup = { 'fish':['<>{',20, 0.3],
           'lollipop':['O-',10, 1],
           'wooden sword':['<(|>--',20, 0.05],
           'merchant':['o[-(\n I am the candy merchant\nwant to trade with candies?',0,0] 
          }
ascii = { key:value[0] for key, value in lookup.items() }
price = { key:value[1] for key, value in lookup.items() if value[1]>0 }
growth= { key:value[2] for key, value in lookup.items() if value[2]>0 } 

class Timer(threading.Thread):
    def __init__(self, interval, action=None, duration=None):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.interval = interval
        self.action = action
        if duration != None:
            self.clock = threading.Timer(duration, self.stop)

    def run(self):
        while not self.event.is_set():
            self.action()
            self.event.wait(self.interval)

    def stop(self):
        self.event.set()
        
class Item(object):
    """ojbects that a player can buy/grow on farm etc"""
    def __init__(self, name):
        self.name = name
        self.ascii_art = ascii.get(name)
        self.price = price.get(name)
        self.grow_rate = growth.get(name) 
    
    @classmethod
    def growth_rate(cls):
        return self.grow_rate

class Farm(object):
    """representation of items in the farm"""
    def __init__(self, crops={}):
        """crops is a dictionary of item objects"""
        self.crops = crops
        self.timer = Timer(1, self.grow)
        self.timer.start()

    def plant(self, item_name):
        self.crops[item_name] = 1 

    def grow(self):
        if self.crops:
            for crop in self.crops.keys():
                #print self.crops.get(crop)
                self.crops[crop] += growth.get(crop)

    def __repr__(self):
        all_crops = ''
        for crop, quantity in self.crops.items():
             all_crops = (ascii.get(crop)+' ') * int(quantity)
        return all_crops + "\n......YYY../\/\/\...|||||.....|||"
     
quest_lookup = {'peaceful forest':[3,10, 'YYY__YYYYYYY_YY_YYYYYYYY__YYY_Y'],
                'mount goblin':[3, 10, '../^^^^^^^\../^^\...../^\..'],
                'underwater cave': [3, 10, '~~vv~~~~~~~~v~~'] }
quest_duration  = { name:value[1] for name, value in quest_lookup.items() }
quest_framerate = { name:value[0] for name, value in quest_lookup.items() }
quest_ascii     = { name:value[2] for name, value in quest_lookup.items() }

def replace_sym( string, sym, index):
    """helper function: replace part of the string at index with new sym"""
    len_sym = len(sym)
    if len(string)> index + len_sym:
        l = list(string)
        l[index] = sym[0]
        l[index+1] = sym[1]
        l[index+2] = sym[2]
        return ''.join(l)
    else:
        return string
    
class Quest(object):
    """a fight player goes on. he uses things from inventory. pick up items"""
    def __init__(self, name, player):
        self.player = player
        self.name = name
        self.timer = Timer(1, self.animate, quest_duration.get(self.name))
        self.frame = -len(self.player.symbol) 
        self.framerate = quest_framerate.get(self.name)
        self.strg = quest_ascii.get(self.name)

    def __repr__(self):
        """replace part of ascii with player symbol depending on frame num"""
        self.strg = replace_sym(self.strg, '___', self.frame+3)
        return replace_sym(self.strg, self.player.symbol, self.frame) 
        
    def animate(self):
        """increment frame number every second"""
        print self
        self.frame += self.framerate

    def start(self):
        self.timer.start()
        self.timer.clock.start()

def main():
    farm = Farm()
    player = Player(farm)
    print "~~~enter a command to play~~~" 
    player.show_menu()
    testing = False 

    def test(player):
        #player.start_quest('peaceful forest')        
        def printing():
            print 'hello'
        t = Timer(1, printing, 5)
        t.start()
        t.clock.start()
    if testing:
        test(player)
    else:
        while not testing:
            player.play()

if __name__ == '__main__':
    main()

