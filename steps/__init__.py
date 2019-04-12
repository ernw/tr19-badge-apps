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
import time

from system import app, screen


class StepScreen(screen.Screen):

    STEPS = 0
    STATE = 0
    THRESHOLD = 13
    RENDER = True

    def register(self):
        self.STEPS = self.storage.STEPS
        if not self.STEPS:
            self.STEPS = 0

    def update(self, delta=0):
        y = self.accel.acceleration.y
        if self.STATE is 0 and y > self.THRESHOLD:
            self.STATE += 1
        elif self.STATE is 1 and y < self.THRESHOLD:
            self.STATE += 1
        if self.STATE is 2:
            self.STATE = 0
            self.STEPS += 1
            self.storage['STEPS'] = self.STEPS
            self.RENDER = True

    def render(self):
        if self.RENDER:
            self.display.fill(display.BACKGROUND)
            self.display.font(display.FONT_DEJAVU_42)
            self.display.text('Steps: {}'.format(self.STEPS), 0, y=0, update=True)
            self.RENDER = False



class App(app.App):

    VERSION = 1
    NAME = 'Step Counter'

    screens = [
        StepScreen(continuous_rendering=True),
    ]




