# This file is part of the Troopers 19 Badge project, https://troopers.de/troopers19/
#
# The BSD 3-Clause License
#
# Copyright (c) 2019 "Malte Heinzelmann" <malte@hnzlmnn.de>
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
from system import app, screen, Input, Kernel


class FucssScreen(screen.Screen):
    w = 32
    h = 32
    x = 0
    y = 0
    step = 4
    dX = 1
    dY = 1
    animate = False


    def konami(self, event):
        self.animate = True

    def register(self):
        self.events.on('input.konami', self.konami)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_B)), self.check_back)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_START)), self.check_back)
        self.x = self.display.width // 2 - self.w // 2
        self.y = self.display.height // 2 - self.h // 2

    def check_back(self, event):
        if event.code is Input.BTN_B and self.input.KONAMI_COUNTER is 8:
            return
        return self.back(event)

    def update(self, delta=0):
        if not self.animate:
            return
        self.x += self.step * self.dX
        if self.x + self.w > 296 or self.x < 0:
            self.dX *= -1
        self.x = max(0, min(296 - self.w, self.x))
        self.y += self.step * self.dY
        if self.y + self.h > 128 or self.y < 0:
            self.dY *= -1
        self.y = max(0, min(128 - self.h, self.y))

    def render(self):
        self.display.font(display.FONT_LOGOS_32)
        self.display.fill(display.FOREGROUND if self.animate else display.BACKGROUND)
        self.display.text(
            'D',
            self.x, y=self.y, color=display.BACKGROUND if self.animate else display.FOREGROUND
        )
        self.display.update()



class App(app.App):

    VERSION = 3
    NAME = 'Fucss'

    screens = [
        FucssScreen(disable_back=True, continuous_rendering=True),
    ]




