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
        self._commands = []

    @property
    def all_commands(self):
        """dictionary of commands and their function and price thresholds """
        return {'candies':(self.check_candy, 0), 
                'inventory':(self.get_inventory, 0),
                'farm':(self.show_farm, 0),
                'throw 10 candies':(self.throw_candy, 10),
                'eat all the candies':(self.eat_candy, 0),
                'buy a lollipop': (self.buy('lollipop'), price.get('lollipop')),
                'buy an icecream': (self.buy('icecream'), price.get('icecream')),
                'plant a lollipop': (self.plant('lollipop'), self._inventory.has_key('lollipop')),
                'go on a quest': (self.go_quest, 100),
                'peaceful forest': (self.go_a_quest('peaceful forest'),100), 
                'mount goblin': (self.go_a_quest('mount goblin'), 130),
                'underwater cave': (self.go_a_quest('underwater cave'), 140),
                'buy a fish': (self.buy('fish'), price.get('fish')) }
             
    def get_commands(self):
        """available actions as a function of num of candies"""
        self._commands = [ command for command, value in self.all_commands.items() if value[1]< self.candies ] 
        return self._commands

    def set_commands(self, new_commands):
        """add to list of available commands"""
        self._commands.append( new_commands )

    commands = property(get_commands, set_commands)

    def get_inventory(self):
        if self._inventory:
            for key, quantity in self._inventory.items():
                show_ascii(key.name, quantity)
        else:
            print "your inventory is empty"
     
    def set_inventory(self, item, quantity):
        if item in self._inventory:
           self._inventory[item] += 1
        else:
           self._inventory[item] = 1

    inventory = property(get_inventory, set_inventory)

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
            new_item = Item( item_name )
            self.set_inventory(new_item,1)
            print "thanks for buying!"
            print "here's your %s for %d candies" %(item_name, price.get(item_name))
        return buy_stuff 

    def plant(self, item_name):
        def plant_things():
            new_item = Item( item_name )
            self.farm.plant(new_item)
        return plant_things

    def show_farm(self):
        print self.farm

    def go_quest(self):
        avai_quests = [ k for k in quest_lookup.keys() ] 
        self.commands.set( avai_quests )        
        print '* '+ '\n* '.join(avai_quests)
    
    def go_a_quest(self, quest_name):
        quest = Quest( quest_name, self)
        quest.start()

    def play(self):
        command = raw_input(">  ")
        if command == 'menu':
            if self.candies > 10:
                show_ascii('merchant')
            print '* '+ '\n* '.join(self.commands)
        elif command in self.commands:
            self.do_command(command)  
            if command!= 'inventory' and command!='candies' and command!='farm':
                self.get_inventory()
                self.check_candy()
        else:
            print 'that action is not available. try again'
           
def show_ascii(name, quantity=1):
    print (ascii.get(name) + '\n')* quantity

"""info look-up ascii art + price + growth rates as factor of 1 second"""
lookup = { 'fish':['<>{',20, 0.3],
           'lollipop':['O-',10, 1],
           'icecream':['((>-',20, 0.05],
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
        
class Farm(object):
    """representation of items in the farm"""
    def __init__(self, crops={}):
        """crops is a dictionary of item objects"""
        self.crops = crops
        self.timer = Timer(1, self.grow)
        self.timer.start()

    def plant(self, item):
        self.crops[item] = 1 

    def grow(self):
        if self.crops:
            for crop in self.crops.keys():
                #print self.crops.get(crop)
                self.crops[crop] += crop.grow_rate            

    def __repr__(self):
        all_crops = ''
        for crop, quantity in self.crops.items():
            #all_crops += crop.ascii_art + ' '+str(quantity)    
             all_crops = (crop.ascii_art+' ') * int(quantity)
        return all_crops + "\n......YYY../\/\/\...|||||.....|||"
     
quest_lookup = {'peaceful forest':[3,20, 'YYY__YYYYYYY_YY_YYYYYYYY__YYY_Y'],
                'mount goblin':[3, 20, '../^^^^^^^\../^^\...../^\..'],
                'underwater cave': [3, 20, '~~vv~~~~~~~~v~~'] }
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
    print "enter menu to see menu"
    while True:
        player.play()

def test():
    farm = Farm()
    player = Player(farm)
    quest = Quest('peaceful forest',player)
    quest.start()
    #print replace_sym( quest_ascii.get('peaceful forest'),player.symbol, 8 ) 

if __name__ == '__main__':
    main()

