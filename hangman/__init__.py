# This file is part of the Troopers 19 Badge project, https://troopers.de/troopers19/
#
# The BSD 3-Clause License
#
# Copyright (c) 2019 "Rafael Schaefer" (@h2odriving)
# All Credit to Malte Heinzelmann (@hnzlnn)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import display
import time
import random

from system import app, screen, Kernel, Input


class ModeScreen(screen.Screen):
    ACTION_KIDS = 0
    ACTION_KIDSDE = 1
    ACTION_EASY = 2
    ACTION_MEDIUM = 3
    ACTION_HARD = 4
    ACTION_VERYHARD = 5
    ACTION_TITLE = 6
    ACTION_HIDDENMODE = 7


    MENU_ITEMS = [
        {'text': 'Chose your Difficulty:', 'action': ACTION_TITLE},
        {'text': 'Kids', 'action': ACTION_KIDS},
        {'text': 'Kids (DE)', 'action': ACTION_KIDSDE},
        {'text': 'Easy', 'action': ACTION_EASY},
        {'text': 'Medium', 'action': ACTION_MEDIUM},
        {'text': 'Hard', 'action': ACTION_HARD},
        {'text': 'Very Hard', 'action': ACTION_VERYHARD},
        {'text': '', 'action': ACTION_HIDDENMODE},
    ]
    
    def register(self):
        self.lights.brightness(.05)
        self.app.WIN_LOSE = self.storage.WIN_LOSE
        if not self.app.WIN_LOSE:
            self.app.WIN_LOSE = [0, 0, 0]
        random.seed(sum(self.kernel.RTC.datetime()))
        
    def on_menu_selection(self, item):
        self.screens[1].RENDER = True
        self.app.font = display.FONT_DEJAVU_24
        self.app.color_win = lambda: (0, 112, 0)
        self.app.color_lose = lambda: (210, 34, 45)
        # HANGMAN INIT Bild 125x125
        self.app.image = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//////////////+AAAAAAP//////////////gAAAAAD//////////////4AAAAAA//////////////+AAAAAAP//////////////gAAAAAD//////////////4AAAAAA//////////////+AAAAAAP//////////////gAAAAAD//////////////4AAAAAA//////////////+AAAAAAP//////////////gAAAAAD//////////////4AAAAAA//////////////+AAAAAAP//////////////gAAAAAAAAAAAAP//AD///4AAAAAAAAAAAAB//4Af//+AAAAAAAAAAAAAP//AH///gAAAAAAAAAAAAB//4B///4AAAAAAAHgAAAAP//Af//+AAAAAAAB8AAAAB//4H///gAAAAAAAfAAAAAP//B///4AAAAAAAHwAAAAB//4f//+AAAAAAAB8AAAAAP//H///gAAAAAAAfAAAAAB//5///4AAAAAAAHwAAAAAP//f//+AAAAAAAB8AAAAAB//////gAAAAAAAfAAAAAAP/////4AAAAAAAHwAAAAAB/////+AAAAAAAB8AAAAAAP/////gAAAAAAAfAAAAAAB/////4AAAAAAAHwAAAAAAP////+AAAAAAAB8AAAAAAB/////gAAAAAAAfAAAAAAAP////4AAAAAAAHwAAAAAAB////+AAAAAAAB8AAAAAAAP////gAAAAAAAfAAAAAAAB////4AAAAAAAHwAAAAAAAP///+AAAAAAAB8AAAAAAAB////gAAAAAAAfAAAAAAAAP///4AAAAAAAHwAAAAAAAB///+AAAAAAAB8AAAAAAAAP///gAAAAAAAfAAAAAAAAB///4AAAAAAAHwAAAAAAAAf//+AAAAAAAB8AAAAAAAAH///gAAAAAAAfAAAAAAAAB///4AAAAAAAHwAAAAAAAAf//+AAAAAAAB8AAAAAAAAH///gAAAAAAAfAAAAAAAAB///4AAAAAAAPwAAAAAAAAf//+AAAAAAAD8AAAAAAAAH///gAAAAAAB/gAAAAAAAB///4AAAAAAAf4AAAAAAAAf//+AAAAAAAP/AAAAAAAAH///gAAAAAAD/wAAAAAAAB///4AAAAAAB/+AAAAAAAAf//+AAAAAAAfPgAAAAAAAH///gAAAAAAPz8AAAAAAAB///4AAAAAAD4fAAAAAAAAf//+AAAAAAB+H4AAAAAAAH///gAAAAAAfA+AAAAAAAB///4AAAAAAPwPwAAAAAAAf//+AAAAAAD4B8AAAAAAAH///gAAAAAA+AfgAAAAAAB///4AAAAAAfgD4AAAAAAAf//+AAAAAAHwA+AAAAAAAH///gAAAAAD8APwAAAAAAB///4AAAAAA+AB8AAAAAAAf//+AAAAAAPgAfAAAAAAAH///gAAAAAD4AHwAAAAAAB///4AAAAAA+AB8AAAAAAAf//+AAAAAAPgAfAAAAAAAH///gAAAAAD4AD4AAAAAAB///4AAAAAA+AB+AAAAAAAf//+AAAAAAPgAfAAAAAAAH///gAAAAAD4AHwAAAAAAB///4AAAAAA+AB8AAAAAAAf//+AAAAAAPgAfAAAAAAAH///gAAAAAD8APwAAAAAAB///4AAAAAAfAD4AAAAAAAf//+AAAAAAH4B+AAAAAAAH///gAAAAAA/g/AAAAAAAB///4AAAAAAP//wAAAAAAAf//+AAAAAAB//4AAAAAAAH///gAAAAAAP/8AAAAAAAB///4AAAAAAB/+AAAAAAAAf//+AAAAAAAH+AAAAAAAAH///gAAAAAAAAAAAAAAAAB///4AAAAAAAAAAAAAAAAAf//+AAAAAAAAAAAAAAAAAH///gAAAAAAAAAAAAAAAAB///4AAAAAAAAAAAAAAAAAf//+AAAAAAAAAAAAAAAAAH///gAAAAAAAAAAAAAAAAB///4AAAAAAAAAAAAAAAAAf//+AAAAAAAAAAAAAAAAAH///gAAAAAAAAAAAAAAAAB///4AAAAAAAAAAAAAAAAAf//+AAAAAAAAAAAAAAAAAH///gAAAAAAAAAAAAAAAAB///4AAAAAAAAAAAAAAAAAf//+AAAAAAAAAAAAAAAAAH///gAAAAAAAAAAAAAAAAB///4AAAAAAAAAAAAAAAAAf//+AAAAAAAAAAAAAAAAAH///gAAAAAAAAAAAAAAAAB///4AAAAAAAAAAAAAAAAAf//+AAAAAAAAAAAAAAAAAH///gAAAAAAAAAAAAAAAAB///4AAAAAAAAAAAAAAAAAf//+AAAAAAAAAAAAAAAAAH///gAAAAAAAAAAAAAAAAB///4AAAAAAAAAAAAAAAAAf//+AAAAAAAAAAAAAAAAAH///gAAAAAAAAAAAAAAAAB///4AAAAAAAAAAAAAAAAAf//+AAAAAAAAAAAAAAAAAH///AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='

        if item['action'] == self.ACTION_EASY:
            self.app.color = lambda: (154, 199, 59)
            self.app.difficulty = 2
            self.app.tries = 0
            self.app.font = display.FONT_DEJAVU_24
            self.app.words = []
            with open("/apps/hangman/easy.txt", "r") as file:
                for line in file.readlines():
                    self.app.words.append(line.replace("\\n", "\n").lower())

            return Kernel.ACTION_LOAD_SCREEN, 1

        if item['action'] == self.ACTION_KIDS:
            self.app.color = lambda: (154, 199, 59)
            self.app.difficulty = 1
            self.app.tries = 0
            self.app.font = display.FONT_DEJAVU_24
            self.app.words = []
            #ENGLISCH Animals
            with open("/apps/hangman/kids.txt", "r") as file:
                for line in file.readlines():
                    self.app.words.append(line.replace("\\n", "\n").lower())
            return Kernel.ACTION_LOAD_SCREEN, 1

        if item['action'] == self.ACTION_KIDSDE:
            self.app.color = lambda: (154, 199, 59)
            self.app.difficulty = 1
            self.app.tries = 0
            self.app.font = display.FONT_DEJAVU_24
            #GERMAN Animals
            self.app.words = []
            with open("/apps/hangman/kids_de.txt", "r") as file:
                for line in file.readlines():
                    self.app.words.append(line.replace("\\n", "\n").lower())
            return Kernel.ACTION_LOAD_SCREEN, 1


        if item['action'] == self.ACTION_MEDIUM:
            self.app.color = lambda: (13, 162, 200)
            self.app.font = display.FONT_DEJAVU_12
            self.app.difficulty = 3
            self.app.tries = 0
            self.app.words = []
            with open("/apps/hangman/medium.txt", "r") as file:
                for line in file.readlines():
                    self.app.words.append(line.replace("\n", "").lower())
           
            
            return Kernel.ACTION_LOAD_SCREEN, 1

        if item['action'] == self.ACTION_HARD:
            self.app.font = display.FONT_DEJAVU_12
            self.app.color = lambda: (252, 140, 0)
            self.app.difficulty = 6
            self.app.tries = 0
            self.app.words = []
            with open("/apps/hangman/hard.txt", "r") as file:
                for line in file.readlines():
                    self.app.words.append(line.replace("\\n", "\n").lower())

            return Kernel.ACTION_LOAD_SCREEN, 1
        
        if item['action'] == self.ACTION_VERYHARD:
            self.app.font = display.FONT_DEJAVU_12
            self.app.color = lambda: (118, 0, 137)
            self.app.difficulty = 8
            self.app.tries = 2
            self.app.words = []
            with open("/apps/hangman/veryhard.txt", "r") as file:
                for line in file.readlines():
                    self.app.words.append(line.replace("\\n", "\n").lower())

            return Kernel.ACTION_LOAD_SCREEN, 1

        if item['action'] == self.ACTION_HIDDENMODE:
            self.app.font = display.FONT_DEJAVU_12
            self.app.color = lambda: (118, 0, 137)
            self.app.difficulty = 9
            self.app.tries = 2
            if self.app.WIN_LOSE[2] == 10:
                self.app.words = ['BAEZ-OGBO-BZEI-TIGI-ZAII']
                return Kernel.ACTION_LOAD_SCREEN, 1
            return

class GameScreen(screen.Screen):
    WIN = None
    WIN_LOSE = [0, 0, 0]
    mind = None
    word = None
    word_space = None
    missedLetters = None
    correctLetters = None

    HANGMANPICS = ['''
    +---+
    |   |
        |
        |
        |
        |
  =========''', '''
    +---+
    |   |
    O   |
        |
        |
        |
  =========''', '''
    +---+
    |   |
    O   |
    |   |
        |
        |
  =========''', '''
    +---+
    |   |
    O   |
   /|   |
        |
        |
  =========''', '''
    +---+
    |   |
    O   |
   /|\  |
        |
        |
  =========''', '''
    +---+
    |   |
    O   |
   /|\  |
   /    |
        |
  =========''', '''
    +---+
    |   |
    O   |
   /|\  |
   / \  |
        |
  =========''']
    WINPIC = '''
    .____.
   /|    |\\
  (_|    |_)
     \  /
      )(
    _|__|_
   |______|'''

    def register(self):
        self.events.on('input.up.char', self.check_input)
        self.init_start()

    def check_input(self, event):
        c = event.code - Input.KEY_A + 97
        if not(97 <= c <= 122):
            return
        letter = chr(c)
        guesses = self.missedLetters + self.correctLetters
        if letter in guesses:
            return
        if self.WIN:
            return
        if len(self.missedLetters) + self.app.tries == len(self.HANGMANPICS) - 1:
            return

        if letter in self.word:
            self.correctLetters += letter
            self.word_space = "".join(map(lambda c: ' ' if not c in self.correctLetters else c, self.word))
            if self.word_space == self.word:
                self.WIN = True
            return Kernel.ACTION_RELOAD
        else:
            self.missedLetters += letter
            self.mind = self.strike(self.mind)
            return Kernel.ACTION_RELOAD

    def update(self, delta=0):
        self.display.fill(display.BACKGROUND)
        space = 6

        self.display.text("Status wrong letters: " + " ".join(self.missedLetters), x=20, y=4)
        self.display.hline(x=0, y=20, width=self.display.width)

        if not self.WIN:
            self.display.text(self.HANGMANPICS[len(self.missedLetters) + self.app.tries], x=0, y=30, wrap=display.WRAP_LINE_START)
            self.display.text(' '.join(map(lambda c: '_' if not c in " -'\n" else c, self.word)), x=98, y=50, max_width=198 - space, wrap=display.WRAP_INDENT)
            if self.app.difficulty == 9:
                self.display.text(' '.join(self.word_space.upper()), x=98, y=50, max_width=198 - space, wrap=display.WRAP_INDENT)
            elif self.app.difficulty > 5:
                self.display.text(' '.join(self.word_space), x=98, y=50, max_width=198 - space, wrap=display.WRAP_INDENT)
            else:
                self.display.text(' '.join(self.word_space), x=98, y=50, max_width=198 - space, wrap=display.WRAP_INDENT)
            self.display.update()
        if self.WIN:
            self.display.fill(display.BACKGROUND)
            self.colorize(self.app.color_win())
            self.WIN_LOSE[0] += 1
            self.play_again()
            self.display.text(self.WINPIC, x=10, y=30, wrap=display.WRAP_LINE_START)
            if self.app.difficulty == 9:
                self.display.text('Y0U W0N [' + str(self.WIN_LOSE[2]) + '/10]\n7he w0rd was:\n' + ''.join(self.word).upper(),
                                  x=108, y=50, max_width=188 - space, wrap=display.WRAP_INDENT)
            elif self.app.difficulty > 5:
                self.WIN_LOSE[2] += 1
                self.display.text('YOU WON [' + str(self.WIN_LOSE[2]) + '/10]\nThe word was:\n' + ''.join(self.word),
                                  x=108, y=50, max_width=188 - space, wrap=display.WRAP_INDENT)
            else:
                self.display.text('YOU WON ['+str(self.WIN_LOSE[0])+']\nThe word was:\n' + ''.join(self.word), x=108, y=50,
                                  max_width=188 - space, wrap=display.WRAP_INDENT)
            self.display.update()
            self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_A)), self.init_restart, single=True)

        if len(self.missedLetters) + self.app.tries == len(self.HANGMANPICS) - 1:
            self.display.fill(display.BACKGROUND)
            self.colorize(self.app.color_lose())
            self.WIN_LOSE[1] += 1
            self.WIN = False
            self.play_again()
            self.display.text(self.HANGMANPICS[len(self.missedLetters) + self.app.tries], x=5, y=30, wrap=display.WRAP_LINE_START)
            if self.app.difficulty < 5:
                self.display.text('YOU LOSE\nThe correct word was:\n' + ''.join(self.word) +  '', x=108, y=50,
                                  max_width=188 - space, wrap=display.WRAP_INDENT)
            elif self.app.difficulty != 9:
                self.display.text('YOU LOSE\nThe letters you found:\n' + ''.join(self.word_space) + '', x=108, y=50,
                                  max_width=188 - space, wrap=display.WRAP_INDENT)
            else:
                self.WIN_LOSE[2] -= 1
                self.display.text('YOU LOSE [' + str(self.WIN_LOSE[2]) + '/10]\nThe letters you found:\n' +
                                  ''.join(map(lambda c: '_' if c in " " else c, self.word_space)).upper() + '',
                                  x=108, y=50, max_width=188 - space, wrap=display.WRAP_INDENT)
            self.display.update()
            self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_A)), self.init_restart, single=True)

    def init_restart(self, event=None):
        if (len(self.missedLetters) + self.app.tries == len(self.HANGMANPICS) - 1) or self.WIN:
            self.init_start()
            return Kernel.ACTION_RELOAD
        return

    def init_start(self, event=None):
        # INITIAL START
        self.WIN = False
        self.WIN_LOSE = self.app.WIN_LOSE
        if not self.WIN_LOSE:
            self.WIN_LOSE = [0, 0, 0]
        self.word = random.choice(self.app.words).lower()
        for i in range(3):
            self.mind = self.loading(self.mind)
            time.sleep(.2)
        self.word_space = ''.join(map(lambda c: ' ' if not c in " -'\n" else c, self.word))
        self.correctLetters = ''.join(map(lambda c: '' if not c in " -'\n" else c, self.word))
        self.missedLetters = ""
        self.colorize(self.app.color())
        if self.app.tries != 0:
            for t in range(self.app.tries):
                self.mind = self.init_strike(t, self.mind)
        return Kernel.ACTION_RELOAD

    def play_again(self):
        self.display.text("Want to play again?  Yes:(A) or No:(B)", x=20, y=4,
                          wrap=display.WRAP_INDENT)
        self.display.hline(x=0, y=20, width=self.display.width)

    def loading(self, state=None, direction=None):
        return self.marquee((lambda i: (236, 236, 236) if i%2 == 0 else (191, 191, 191)), state, direction)

    def colorize(self, color, state=None, direction=None):
        return self.marquee(lambda i: color, state, direction)

    def init_strike(self, position, state=None, direction=None):
        return self.set_color(lambda i: (207, 41, 29), position, state, direction)

    def strike(self, state=None, direction=None):
        return self.set_color(lambda i: (207, 41, 29), (len(self.missedLetters) + self.app.tries)-1, state, direction)

    def marquee(self, colorfn, state=None, direction=None):
        if state is None:
            state = (0, 1)  # Marks the start of the LED
        if direction is not None:
            state = (state[0], int(direction))

        for i in range(self.lights.count):
            self.lights.set(colorfn(i), lights=(i + state[0]) % self.lights.count)
        return (state[0] + state[1]) % self.lights.count, state[1]

    def set_color(self, colorfn, position, state=None, direction=None):
        if state is None:
            state = (0, 1)  # Marks the start of the LED
        if direction is not None:
            state = (state[0], int(direction))
        self.lights.set(colorfn(int(position)), lights=(int(position)) % self.lights.count)
        return (state[0] + state[1]) % self.lights.count, state[1]

    def back(self, event):
        self.word = None
        self.storage['WIN_LOSE'] = self.WIN_LOSE
        self.app.WIN_LOSE = self.WIN_LOSE
        return Kernel.ACTION_LOAD_SCREEN, 0


class App(app.App):
    VERSION = 0.98 #Beta

    screens = [
        ModeScreen(),
        GameScreen(),
    ]
