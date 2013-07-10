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
                'buy a fish': (self.buy('fish'), price.get('fish')) }
             
    @property
    def avai_commands(self):
        """available actions as a function of num of candies"""
        return [ command for command, value in self.all_commands.items() if value[1]< self.candies ] 
        
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
            print "thanks for buying! here's your %s for %d candies" %(item_name, price.get(item_name) )
        return buy_stuff 

    def plant(self, item_name):
        def plant_things():
            new_item = Item( item_name )
            self.farm.plant(new_item)
        return plant_things

    def show_farm(self):
        print self.farm

    def play(self):
        command = get_input()
        if command == 'menu':
            if self.candies > 10:
                show_ascii('merchant')
            print '* '+ '\n* '.join(self.avai_commands)
        elif command in self.avai_commands:
            self.do_command(command)  
            if command!= 'inventory' and command!='candies' and command!='farm':
                self.get_inventory()
                self.check_candy()
        else:
            print 'that action is not available. try again'
           
def get_input():
        return raw_input(">  ")

def show_ascii(name, quantity=1):
    print (ascii.get(name) + '\n')* quantity

"""info look-up ascii art + price + growth rates as factor of 1 second"""
lookup = { 'fish':['<>{',20, 0.3],
           'lollipop':['O-',10, 0.1],
           'icecream':['((>-',20, 0.05],
           'merchant':['o[-(\n I am the candy merchant\nwant to trade with candies?',0,0] 
          }
ascii = { key:value[0] for key, value in lookup.items() }
price = { key:value[1] for key, value in lookup.items() if value[1]>0 }
growth= { key:value[2] for key, value in lookup.items() if value[2]>0 } 

class Timer(threading.Thread):
    def __init__(self, interval,action=None):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.interval = interval
        self.action = action

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
                self.crops[crop] += crop.grow_rate            

    def __repr__(self):
        all_crops = ''
        for crop, quantity in self.crops.items():
            #all_crops += crop.ascii_art + ' '+str(quantity)    
             all_crops = (crop.ascii_art+' ') * int(quantity)
        return all_crops + "\n......YYY../\/\/\...|||||.....|||"
     
def main():
    farm = Farm()
    player = Player(farm)
    print "enter menu to see menu"
    while True:
        player.play()

def test():
    print growth.get('lollipop')
    it = Item('lollipop')
    print it.grow_rate
    
if __name__ == '__main__':
    main()

