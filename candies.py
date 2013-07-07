# making the candies web game in terminal
import time
import threading

class Player(object):
    def __init__(self):
        self.candies = 0
        self._inventory = {} 

    @property
    def all_commands(self):
        """dictionary of all commands in the game"""
        return {'candies':self.check_candy, 
                'inventory':self.get_inventory,
                'throw 10 candies':self.throw_candy,
                'eat all the candies':self.eat_candy,
                'buy a lollipop':self.buy('lollipop'),
                'buy an icecream':self.buy('icecream'),
                'buy a fish':self.buy('fish') }
             
    @property
    def avai_commands(self):
        """available actions as a function of num of candies"""
        return [ command for threshold,command in thresholds if threshold< self.candies ] 
        
    def get_inventory(self):
        for key, value  in self._inventory.items():
           print 'you have '+str(value)+' '+key
           show_ascii(key, value)
     
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

    def buy(self, item):
        self.candies = self.candies - price.get(item)
        self.set_inventory(item,1)

    def buy_lollipop(self):
        self.candies = self.candies - 10 
        self.set_inventory('lollipop',1)

    def buy_fish(self):
        self.candies = self.candies - 20
        self.set_inventory('fish',1)

    def buy_icecream(self):
        self.candies = self.candies - 20
        self.set_inventory('icecream',1)

    def play(self):
        command = get_input()
        if command == 'menu':
            if self.candies > 10:
                show_ascii('merchant')
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

"""num of candies needed to execute commands"""
thresholds = [ (0,'candies'),
               (0, 'eat all the candies'),
               (0, 'inventory'),
               (10,'throw 10 candies'),
               (10,'buy a lollipop'),
               (20,'buy a fish'),
               (20,'buy an icecream')]
              
"""ascii art look-up.combine with thresholds??? """
ascii = { 'fish': '<>{',
          'lollipop': 'O-',
          'icecream': '((>-',
          'merchant': 'o[-(\n I am the candy merchant\n I trade things with candies' }

#"""price look-up"""
price = { 'fish': 20, 
          'lollipop': 10,
          'icecream': 20,
}

class Timer(threading.Thread):
    def __init__(self, player):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.player = player 

    def run(self):
        """increment candy by 1 every second"""
        while not self.event.is_set():
            self.player.candies += 1
            self.event.wait(1)

    def stop(self):
        self.event.set()
        
def main():
    player = Player()
    timer = Timer( player )
    timer.start()
    print "enter menu to see menu"
    while True:
        player.play()

if __name__ == '__main__':
    main()

