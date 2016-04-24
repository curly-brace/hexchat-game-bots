__module_name__ = "Hangman Bot"
__module_version__ = "0.1"
__module_description__ = "Solves Hangman games"
__author__ = "curly-brace" 

import xchat as XC
import requests
from BeautifulSoup import BeautifulSoup
import random

counter = 0
timeless = False

def init_cb(arg):
    global game
    game = XC.find_context(channel='#gridcoin-games')
    
    if game is not None:
        game.prnt('-= hangman bot loaded =-')
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
        game.prnt('-= hangman game stoped =-')
    elif word[1] == 'status':
        game.prnt('-= hangman bot status =-')
        game.prnt('timeless mode: ' + str(timeless))
        game.prnt('games left: ' + str(counter))
    else:
        counter = int(word[1])
        fire(0)

def fire(arg):
    global first_turn
    global counter
    global h_timer
    
    game.command('say !hangmanstart')
    first_turn = True
    
    if counter > 0:
        counter -= 1
        
def message_cb(word, word_eol, userdata):
    global first_turn
    global guess
    global used_letters
    global patt
    
    if word[0] == '[-KriStaL-]':
        if 'Puzzle' in word[1]:
            if first_turn:
                first_turn = False
                used_letters = ''
                
                patt = word[1][10:]
                
                r = requests.post('http://nmichaels.org/hangsolve.py', data = {
                        'pattern' : patt,
                        'guessed' : '',
                        'game' : 'hangman',
                        'action' : 'display'
                    })
                guess = str(BeautifulSoup(r.content).find('span', {'class':'guess'}).text[0])
                XC.hook_timer(random.randint(2000, 5000), guess_letter)
                used_letters += guess
            else:
                patt = word[1][10:]
                request_letter()
        elif 'Sorry, there is no' in word[1]:
            request_letter()
        elif 'Congratulations' in word[1]:
            game.prnt('-= we won! =-')
            endgame()
        elif 'No one guessed' in word[1]:
            game.prnt('-= we lose! =-')
            endgame()

def endgame():
    global counter
    global h_timer
    global timeless
    
    if counter > 0 or timeless:
        h_timer = XC.hook_timer(random.randint(10000, 20000), fire)

def request_letter():
    global used_letters
    global guess
    global patt
    
    args = {'pattern' + str(i) : patt[i].lower() if patt[i] !=  '_' else '' for i in range(0,len(patt))}
    args['guessed'] = used_letters
    args['game'] = 'hangman'
    args['action'] = 'display'
    
    r = requests.post('http://nmichaels.org/hangsolve.py', data = args)
    guess = str(BeautifulSoup(r.content).find('span', {'class':'guess'}).text[0])
    XC.hook_timer(random.randint(2000, 5000), guess_letter)
    used_letters += guess

# for not answering in just a moment when the task appears =)
def guess_letter(arg):
    global game
    global guess
    
    game.command('say !hangman ' + guess)


XC.hook_timer(4000, init_cb)
XC.hook_command("hbot", bot_cb, help="/hbot X - hangman X times (if nothing - 1 time) or start/stop or status")
XC.hook_print("Channel Message", message_cb)
XC.hook_print("Channel Msg Hilight", message_cb)
