__module_name__ = "Scramble Bot"
__module_version__ = "0.1"
__module_description__ = "Solves Scramble games"
__author__ = "curly-brace" 

import xchat as XC
import random
import requests
from BeautifulSoup import BeautifulSoup

game = None
counter = 0
timeless = False
playing = False
cur_letter = -1

def init_cb(arg):
    global game
    game = XC.find_context(channel='#gridcoin-games')
    
    if game is not None:
        game.prnt('-= scrambler bot loaded =-')
    else:
        XC.hook_timer(4000, init_cb)

def bot_cb(word, word_eol, userdata):
    global counter
    global timeless
    global h_timer
    
    if len(word) == 1:
        fire(0)
    elif word[1] == 'start':
        timeless = True
        fire(0)
    elif word[1] == 'stop':
        timeless = False
        counter = 0
        XC.unhook(h_timer)
        game.prnt('-= scramble game stoped =-')
    elif word[1] == 'status':
        game.prnt('-= scramble bot status =-')
        game.prnt('timeless mode: ' + str(timeless))
        game.prnt('games left: ' + str(counter))
    else:
        counter = int(word[1])
        fire(0)

def fire(arg):
    global counter
    global h_timer
    
    game.command('say !scramble')
    
    if counter > 0:
        counter -= 1
    
    if counter > 0 or timeless:
        h_timer = XC.hook_timer(5 * 60000 + random.randint(10000, 30000), fire)

def message_cb(word, word_eol, userdata):
    global game
    global res
    global playing
    global cur_letter
    global answer
    
    if word[0] == '[-KriStaL-]':
        if 'Unscramble' in word[1]:
            playing = True
            cur_letter = -1
            
            r = requests.get('http://www.vocabula.com/feature/unscrambler.aspx?word=' + word[1][17:])
            soup = BeautifulSoup(r.content)
            res = soup.find(id ='lblResults').contents
            
            game.prnt(str([res[i].lower() for i in xrange(0, len(res), 2)]))
            
            if len(res) == 2:
                XC.hook_timer(random.randint(1000, 3000), give_answer)
                answer = res[0]
        elif 'First' in word[1]:
            if playing:
                matching = [res[i] for i in xrange(0, len(res), 2) if res[i].startswith(word[1][cur_letter:])]
                game.prnt(str(matching))
                
                cur_letter -= 1
                
                if len(matching) == 1 or (cur_letter == -4 and len(matching) > 0):
                    XC.hook_timer(random.randint(1000, 3000), give_answer)
                    answer = matching[0]
        elif 'Woohoo' in word[1]:
            playing = False
            game.prnt('-= we won! =-')
        elif 'Nobody got it...' in word[1]:
            playing = False
            game.prnt('-= we are loosers :( =-')

# for not giving answer in just a moment when the task appears =)
def give_answer(arg):
    global game
    game.command('say ' + answer)

XC.hook_timer(4000, init_cb)
XC.hook_command("sbot", bot_cb, help="/sbot X - unscramble X times (if nothing - 1 time) or start/stop or status")
XC.hook_print("Channel Message", message_cb)
