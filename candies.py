# making the candies web game in terminal
import time
import threading

class Player(object):
    def __init__(self):
        self.candies = 0
        self._inventory = {} 
        self.timer = Timer(1, self.increment_candy)
        self.timer.start()

    @property
    def all_commands(self):
        """dictionary of all commands in the game"""
        return {'candies':self.check_candy, 
                'inventory':self.get_inventory,
                'throw 10 candies':self.throw_candy,
                'eat all the candies':self.eat_candy,
                'buy a lollipop': self.buy('lollipop'),
                'buy an icecream': self.buy('icecream'),
                'buy a fish': self.buy('fish') }
             
    @property
    def avai_commands(self):
        """available actions as a function of num of candies"""
        return [ command for threshold,command in thresholds if threshold< self.candies ] 
        
    def get_inventory(self):
        if self._inventory:
            for key, value  in self._inventory.items():
                show_ascii(key, value)
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
        self.all_commands.get(command)()
       
    def check_candy(self):
        print "you have %s candies" %self.candies

    def throw_candy(self):
        self.candies = self.candies - 10

    def eat_candy(self):
        self.candies = 0

    def increment_candy(self):
        self.candies += 1

    def buy(self, item):
        def buy_stuff():
             self.candies = self.candies - price.get(item)
             self.set_inventory(item,1)
             print "thanks for buying! here's your %s for %d candies" %(item, price.get(item) )
        return buy_stuff 

    def play(self):
        command = get_input()
        if command == 'menu':
            if self.candies > 10:
                show_ascii('merchant')
            print 'candies'+ str(self.candies)
            print '* '+ '\n* '.join(self.avai_commands)
        elif command in self.avai_commands:
            self.do_command(command)  
            if command!= 'inventory' and command!='candies':
                self.get_inventory()
                self.check_candy()
        else:
            print 'that action is not available. try again'
           
def get_input():
        return raw_input(">  ")

def show_ascii(name, quantity=1):
    print (ascii.get(name) + '\n')* quantity

"""info look-up ascii art + price + growth rates as factor of 1 second"""
lookup = { 'fish':['<>{',20,1/30],
           'lollipop':['O-',10, 1/60],
           'icecream':['((>-',20, 1/20],
           'merchant':['o[-(\n I am the candy merchant\nwant to trade with candies?',0,0] 
          }
ascii = { key:value[0] for key, value in lookup.items() }
price = { key:value[1] for key, value in lookup.items() }
growth= { key:value[2] for key, value in lookup.items() if value[2]>0 } 

"""item enabled for purchase from num of candies"""
price_limits = [(value, 'buy a '+item) for item, value in price.items() ] 
"""threshold for commands unrelated to buying"""
thresh_commands = [ (0,'candies'),
                    (0, 'eat all the candies'),
                    (0, 'inventory'),
                    (10,'throw 10 candies') ]

"""num of candies needed to execute commands"""
thresholds = price_limits + thresh_commands 
 
class Timer(threading.Thread):
    def __init__(self, interval,action):
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
        
class Farm(object):
    def __init__(self):
        self.crops = None
    def __repr__(self):
        return "......YYY../\/\/\...|||||.....|||"
    def grow(self):
        NotImplementedError
     
def main():
    player = Player()
    print "enter menu to see menu"
    while True:
        player.play()
    player.timer.stop()

def test():
    timer = Timer(1)
    timer0 = Timer(2)
    timer.start()
    timer0.start()
    

if __name__ == '__main__':
    main()

