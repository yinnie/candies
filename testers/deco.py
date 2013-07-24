import inspect

commands = {} #'go': (direction, function)

class Game(object):
    def __init__(self):
        self.x = 0
        self.y = 1

def command(function):
    """building the 'commands' dictionary with decorators""" 
    func_name = function.__name__
    func_args = inspect.getargspec(function).args[1:]
    name = func_name + ' '.join(func_args)
    commands[func_name] = (func_args, function)

directions = { 'north': (1,1),
               'south': (1,0),
               'west' : (0,0),
               'east' : (0,1) }

@command
def go(game, direction):
    """the arguments only get passed in after user type"""
    if direction not in directions:
        return 'you should give a valid direction'
    game.x, game.y = directions[direction]
    return "i am going %s to the sea!!" %direction
    
@command
def hi(game):
    return " hi hi hi"

def process_command(game, words):
    '''take the first word of user typed text and look up function in commands'''
    word = words[0]
    if word == 'quit':
       return 'bye'
    if word not in commands:
       print 'that command does not exist'
       print 'The available command are {0}'.format(commands)

    argspec, function = commands[word]
    args = words[1:]
    if len(args) < len(argspec):
        return 'you need to give a {}'.format(argspec)
    if len(args) > len(argspec): 
        return 'you wrote too much'

    return function(game, *args)

def run_game():
    game = Game()
    while True:
         in_words = raw_input('> ')
         words = in_words.lower().split()
         message = process_command(game, words)
         print message

if __name__ == '__main__':
    run_game()
            


