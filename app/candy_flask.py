import sys, time, threading, inspect, collections

class Player(object):
    def __init__(self, farm):
        self.candies = 0
        self._inventory = {} 
        self.timer = Timer(1, self.increment_candy)
        self.timer.start()
        self.farm = farm
        self.symbol = '\\o/'

    def get_inventory(self):
        if self._inventory:
           all_inventory = ""
           #TODO refactoring!! 
           for key, quantity in self._inventory.items():
                if quantity > 0:
                    s0= key 
                    s1= str(quantity)
                    s2= 'insert art of the item' 
                    all_inventory += ( s0+'\n'+s1+'\n'+s2+'\n') 
           return  all_inventory
        else:
            return "your inventory is empty"
     
    def set_inventory(self, item, quantity):
        if item in self._inventory:
           self._inventory[item] += 1
        else:
           self._inventory[item] = 1

    def increment_candy(self):
        self.candies += 1

    def go_quest(self):
        avai_quests = [ k for k in quest_lookup ] 
        self.quest = True
        s= "choose a quest to go on ! \n" 
        s+= '\n'.join(avai_quests)
        s+= '\n'
        return  s 

    def start_quest(self, quest_name):
        quest = Quest(quest_name, self)
        #quest.start()
        #self.play('start_quest(quest_name)')
        return quest.frames         

    def show_menu(self):
        s0= "''''''''''''''''''''''''''''"
        s1= "~~~available actions:~~~~"
        s2= '\n'.join(commands.keys())
        return s0+'\n'+ s1 + '\n'+ s2 + '\n'

class Timer(threading.Thread):
    '''timer for increasing candies and animation'''
    def __init__(self, interval, action=None, duration=None):
        threading.Thread.__init__(self)
        '''stop thread when main program stops'''
        self.daemon = True
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
 
class Farm(object):
    """representation of items in the farm"""
    def __init__(self, crops={}):
        self.crops = crops
        self.timer = Timer(1, self.grow)
        self.timer.start()

    def plant(self, item_name):
        self.crops[item_name] = 1 

    def grow(self):
        if self.crops:
            for crop in self.crops:
                self.crops[crop] += growth.get(crop)

    def __repr__(self):
        all_crops = ''
        for crop, quantity in self.crops.items():
             all_crops = (ascii.get(crop)+' ') * int(quantity)
        return all_crops + "\n" + "YYYYYY|||||||||......YYY../\/\/\...||||" 

   
def replace_sym( string, sym, index):
    """helper func: replace part of the string at index with new sym"""
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
        
    @property
    def frames(self):
        """all the frames of the animation to be sent to browser"""
        frames = [] 
        for x in range(self.frame, quest_duration.get(self.name)):
            frames.append(self.__repr__() )
            self.frame += self.framerate
        return frames

    def animate(self):
        """increment frame number every second"""
        print self
        self.frame += self.framerate

    def start(self):
        self.timer.start()
        self.timer.clock.start()

farm = Farm()
player = Player(farm)

commands = {} #'buy': (func_arguments, function)
              #'hi': ( no arg, function)

def show_ascii(name, quantity=1):
    return (ascii.get(name) + '\n')* quantity


def command(function):
    '''decorator to build commands dictionary'''
    func_name = function.__name__.replace('_',' ')
    func_args = inspect.getargspec(function).args[1:]
    commands[func_name] = (func_args, function) 
    return function


def checks(player):
    return { 'candies'   : player.candies,
             'inventory' : player.get_inventory(),
             'farm'      : player.farm }
@command
def check(player, target):
    if target in checks(player):
        return checks(player)[target]
    else:
        return'you need to give a valid {} to check'.format(target)
    return checks(player)[target]

@command
def throw_10_candies_on_the_ground(player):
    player.candies -= 10

@command
def eat_all_the_candies(player):
    player.candies = 0


Item = collections.namedtuple('Item', 'name art price growth')

name_to_item = {item.name : item for item in [
                Item('fish',        '<>{',    20, 0.3),
                Item('lollipop',    'O--',    10, 1.0),
                Item('wooden sword','<(|>--', 20, 0.05)
                ]}

@command
def buy(player, in_str):
    item = in_str[2:]       
    if item not in name_to_item:
        return 'give a valid {} to buy'.format(item)
    price = name_to_item.get(item).price 
    if player.candies <= price:
        return 'you don\'t have enough candies to buy it!' 
    player.candies -= price 
    player.set_inventory(item,1)
    s0= "thanks for buying!"
    s1= "here's your %s " %( item )
    return s0+'\n'+s1+'\n'

buy = command(has_money(buy))

quest_lookup = {'peaceful forest':[3,10, 'YYY__YYYYYYY_YY_YYYYYYYY__YYY_Y'],
                'mount goblin':[3, 10, '../^^^^^^^\../^^\...../^\..'],
                'underwater cave': [3, 10, '~~vv~~~~~~~~v~~'] }

quest_duration  = { name:value[1] for name, value in quest_lookup.items() }
quest_framerate = { name:value[0] for name, value in quest_lookup.items() }
quest_ascii     = { name:value[2] for name, value in quest_lookup.items() }

quests = {'to peaceful forest': player.start_quest('peaceful forest'),
          'to mount goblin'   : player.start_quest('mount goblin'),
          'to underwater cave': player.start_quest('underwater cave'),
          'on a quest'        : player.go_quest() }

@command
def go(player, place):
    """Go to a place in the kingdom"""
    if place not in quests:
        return 'give a valid {} to go'.format(place)
    if 'wooden sword' not in player._inventory:
        return 'you need a sword to go on a quest'
    return quests[place]

#go.__doc__

@command
def plant(player, item):
    if item not in player._inventory:
        return 'you don\'t have {} to plant'.format(item)
    player.farm.plant(item)
    player._inventory[item] -= 1
    return " you just planted a %s. Go check out your farm! " %item_name 

def process_input(text):
    '''look up commands and return function results'''
    first_w = text[0]   
    args = ' '.join(text[1:])
    if first_w not in commands:
        return 'that command does not exit'

    argspec, function = commands[first_w]
    if len(args) < len(argspec):
        return 'you need to give a {}'.format(argspec)

    return function(player, args)

def play_game():
    print "~~~enter a command to play~~~" 
    while True:
         try:
            user_in = raw_input('>> ')
            words = user_in.lower().split()
            if words == ['quit']:
                 break
            result = process_input(words)
            print player.show_menu()
            print '~~~~~~~~~~~~~~~~~~~~~~~~'
            print result 
         except EOFError:
             print 'oops! wrong key!'
            
farm = Farm()
player = Player(farm)

if __name__== '__main__':
     play_game()


