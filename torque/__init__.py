# This file is part of the Troopers 19 Badge project, https://troopers.de/troopers19/
#
# The BSD 3-Clause License
#
# Copyright (c) 2019 @hnzlmnn, @br3zel
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

from system import app, screen, Kernel
from machine import Pin,I2C

class StartScreen(screen.Screen):
    ACTION_TITLE    = 0
    ACTION_GAME    = 1

    MENU_ITEMS = [

        {'text': 'TORQUE-A TR19 Zork adventure', 'action': ACTION_TITLE},
        {'text': 'Start', 'action': ACTION_GAME},
    ]

    def on_menu_selection(self, item):
        if item['action'] == self.ACTION_GAME:
            return Kernel.ACTION_LOAD_SCREEN, 1

class GameScreen(screen.Screen):

    loop = 4
    response=""
    #So you are using the SOURCE? Good! Here is your not properly secured BROT64: fzKdeUF1NXJjPjJjMDKdeUNxZ0RjPjJ2OEhzMUNyNUVuNEB0Oj1yPUB1MUZ0OUJjgR==

    story={
        4:(
            "You arrive in the cyberspace, west of a datacenter\nA (secret) path leads southwest into a domain forest.\nA mailbox is in front of you ",{
            "open mailbox":(
                "It is secured with military grade encryption.",
                None
            ),
            "break encryption":(
                "Decypting the mailbox reveals tons of\nmails and an attachment that catches your\nattention...a PDF.",
                None
            ),
            "go east":(
                "The datacenter is secured with a firewall.",
                None
            ),
            "bypass firewall":(
                "It is NEXT-GEN...it is impossible to bypass a nextgen firewall.",
                None
            ),
            "look at datacenter":(
                "The datacenter is a beautiful building which is painted in blue, red, yellow, blue, green, red. It is clear that the owners are extremely wealthy and heavily guarded.",
                None
            ),
            "access datacenter":(
                "It is secured with a firewall.",
                None
            ),
            "open pdf":(
                "Howdy F.U.C.S.S Agent.\nYour mission as a F.U.C.S.S agent as part of TORQUE is to find the evil forces\n behind the SHADOWBROKER and VAULT7 leaks. Use the TORQUE, agent. At the end of the message there is a strange string... ",
                None
            ),
            "read pdf": (
                "Howdy F.U.C.S.S Agent.\nYour mission as a F.U.C.S.S agent as part of TORQUE is to find the evil forces\n behind the SHADOWBROKER and VAULT7 leaks. Use the TORQUE, agent. At the end of the message there is a strange string... ",
                None
                ),
            "read string":("n7SlmcN9VfRrXrSamfe1kPe3mPe1if24kf++kvu0hgayk/C8mferigSAhfWxmfCwlAiulvG7iPC+kvlrULSlmcV5h8ZrXrR+VMh7Uch9VMt2Xcp8WL95WMt7Uct/XMlroZ==\nYou save it for later...",
                           None
            ),

            "man torque": (
                "This is a classical text adventure just like the old zork game. Either use directions like go north, go southwest or perform actions on items(e.g. open something, break something,look at,inspect,break,...)",
                None
                ),
            "help": (
                "This is a classical text adventure just like the old zork game. Either use directions like go north, go southwest or perform actions on items(e.g. open something, break something,look at...",
                None
                ),

            "go southwest":(
                "Entering the domain forest...",
                8
            ),
            }
        ),
        8:("Entering the domain forest reveals\nunderground TOR tunnels in all directions.\nThe 0DAY is strong with the east.",{
            "go west":("Darknet dealers are in your way trying to sell you prohibited goods. You leave.",
                       None
            ),
            "go north":("The domain forest becomes impenetrable to the North.",
                        None
                        ),
            "go south":(
                "Darknet hitmen trying to sell you an assissination. You turn around...",
                None),
            "go east":(
                "Naughty Naughty.Following the 0DAY.\nGoing east...",
                9
            ),
        }),
        9: (
        "You are in a clearing, with unproteced\nforests surrounding you on all sides.\nA path leads south.", {
            "go west": ("Your credentails are not valid in this part of the domain forest. You leave ...",
                        None
                        ),
            "go north": ("Dark clouds nebulize your view, you turn back.",
                         None
                         ),
            "go east": (
                "Broadcaststorm-tossed connections block your way.",
                None),
            "go south": ("Going south unveils a cave...",
                        10
                        ),

        }
        ),
        10:("You are in a tiny exploit cave with a\ndark, forbidding staircase leading down. There is a crashed FishBowl agent in one corner.",{
        "take agent":("Why would you do that? Are you some sort of zombie process?",
                      None
                      ),
        "inspect agent":("CONGRATS!\nYou found what you were looking for...\nInfoleaks contain exploit blueprints proving that @FishBowl is behind the leaks. Go deeper...",10),
        "smash agent": ("Sick person. Have some respect mate.",
                           None
                           ),
        "break agent":("I have two questions: Why and with What? It is already crashed.",
                       None
                       ),
        "go deeper":("Going deeper...just like LeoDiCaprio\n*dramaticalmusicinthebackground*",
                     11 #changed from 11
                     ),
        "go down staircase":("Going down...",
                                 11
                                 ),
        "scale staircase": ("Going down...",
                                  11
                                  ),
        "descend staircase": ("Descending the staircase...",
                                11
                                ),
        "suicide":("You disable your Windows XP firewall. You die.",
                       4
                       ),}),
        11:("You have entered a cryptocurrency-floored room. Lying half buried in already used exploits there is an old crypto wallet, bulging with bitcoins.",
            {
                "open wallet": ("Opening...Checking your F.U.C.S.S hacking equipment...", 12),

            })

    }

    def update(self):
        chapter = self.story.get(self.loop, None)

        if self.loop == 12:
            return Kernel.ACTION_LOAD_SCREEN,2
        if chapter == None:
            self.loop=4
            return Kernel.ACTION_RELOAD
        if self.response != '':
            self.display.fill(display.BACKGROUND)
            self.display.text(self.response, 0, y=0, wrap=display.WRAP_INDENT,update=True)
            time.sleep(5)
        self.input.get_user_input(self,1,title=chapter[0]+"\nWhat do you do?",title_wrap=display.WRAP_INDENT)

    def on_text(self,event):
        if event.value is None:
            return self.back()
        self.response = ''
        chapter=self.story.get(self.loop,None)
        if chapter == None:
            self.loop = 4
        else:
            value = event.value.lower()
            if value == "":
                return Kernel.ACTION_RELOAD
            path=chapter[1].get(event.value.lower(),None)
            if path is None:
                return Kernel.ACTION_RELOAD
            else:
                self.response = path[0]
                if path[1] is not None:
                    self.loop = path[1]

        return Kernel.ACTION_RELOAD

    def back(self, event):
        self.RENDER = True
        return Kernel.ACTION_LOAD_SCREEN, 0


class EndScreen(screen.Screen):

    def wheel(self, pos):
        if pos < 85:
            return pos * 3, 255 - pos * 3, 0
        elif pos < 170:
            pos -= 85
            return 255 - pos * 3, 0, pos * 3
        else:
            pos -= 170
            return 0, pos * 3, 255 - pos * 3

    def rainbow(self, state=None, direction=None):
        if state is None:
            state = (0, 1)  # Marks the start of the LED
        if direction is not None:
            state = (state[0], int(direction))
        for i in range(self.count):
            self.set(self.wheel(int(i * 256 / self.count)), lights=(i + state[0]) % self.count)
        return (state[0] + state[1]) % self.count, state[1]

    def update(self,delta=0):

        i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
        i2ccount=i2c.scan() #HACK THE BADGE! JUST ATTACH ANY i2c device :-D
        if len(i2ccount)==5:
            self.display.fill(display.BACKGROUND)
            self.display.text("You receive a (sports car) KEY\n(https://brot64.eu/get-started/) with an engraving. It says:\nQuellentelekommunikationsueberwachungsverordnung.\n\nFIN! \n", 0, y=0, wrap=display.WRAP_INDENT, update=True)
            return Kernel.ACTION_RELOAD
        else:
            self.display.fill(display.BACKGROUND)
            self.display.text(
                "You need F.U.C.C.S Hacking equipment from the soldering corner.\n",0,y=0,wrap=display.WRAP_INDENT,update=True)
            return Kernel.ACTION_RELOAD

class App(app.App):
    VERSION = 1

    screens = [
        StartScreen(),
        GameScreen(),
        EndScreen(),
    ]

