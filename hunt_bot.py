__module_name__ = "Hexchat hunt and fish Bot"
__module_version__ = "0.1"
__module_description__ = "Hunts and fishes periodicaly"
__author__ = "curly-brace" 

import xchat as XC
import random

game = None
msg_count = 0
hunt_wait = 0
fish_wait = 0

def init_cb(arg):
    global game
    game = XC.find_context(channel='#gridcoin-games')
    
    if game is not None:
        game.prnt('-= hunter bot loaded =-')
        hunt_cb(0)
    else:
        XC.hook_timer(4000, init_cb)

# status callback
def bot_cb(word, word_eol, userdata):
    game.prnt('-= hunt bot status =-');
    game.prnt('hunt timer: ' + str(hunt_wait));
    game.prnt('fish timer: ' + str(fish_wait));
        
# hunt callback
def hunt_cb(arg):
    game.command('say !hunt')
    
    XC.hook_timer(5000 + random.randint(0, 5000), hunt_time_cb)

# hunt time getter
def hunt_time_cb(arg):
    game.command('say !hunt')

# fish callback
def fish_cb(arg):
    game.command('say !cast')
    
    XC.hook_timer(5000 + random.randint(0, 5000), fish_time_cb)

# fish time getter
def fish_time_cb(arg):
    game.command('say !cast')

# get message with waiting time
def message_cb(word, word_eol, userdata):
    global hunt_wait
    global fish_wait
    
    if word[0] == '[-KriStaL-]':
        if 'hunt again' in word[1]:
            hunt_wait = [int(s) for s in word[1].split() if s.isdigit()][0]
            hunt_wait += random.randint(0, 60000)
            XC.hook_timer(hunt_wait, hunt_cb)
        elif 'fish again' in word[1]:
            fish_wait = [int(s) for s in word[1].split() if s.isdigit()][0]
            fish_wait += random.randint(0, 60000)
            XC.hook_timer(fish_wait, fish_cb)




#XC.hook_timer(4000, init_cb)
#XC.hook_print("Channel Message", message_cb)
#XC.hook_command("hbot", bot_cb, help="/hbot prints status of bot")
