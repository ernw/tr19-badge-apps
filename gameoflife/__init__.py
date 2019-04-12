# This file is part of the Troopers 19 Badge project, https://troopers.de/troopers19/
#
# The BSD 3-Clause License
#
# Copyright (c) 2019 "Hannes Mohr"
# All Credit to Malte Heinzelmann (@hnzlmnn)
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

from system import app, screen, Kernel, Input


class MenuScreen(screen.Screen):

    def register(self):
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_A)), self.start)
        self.events.on('input.up.{}'.format(Input.key_name(Input.KEY_SPACE)), self.select)

    def update(self, delta=0):
        self.display.text('Press A to load an empty screen.\n'
                          'Press Space to select a template\n'
                          'Before starting you can edit the board using the joystick and Space\n'
                          'When done press A to start/pause the simulation', 0, y=0, wrap=display.WRAP_INDENT)

    def start(self):
            return Kernel.ACTION_LOAD_SCREEN, 1


class GameScreen(screen.Screen):
    # distances from screen edge
    x_offset = 12
    y_offset = 8
    # gap of filled in cell from gridlines
    cell_gap = 2
    # size of a cell of the grid
    box_size = 16
    cursor_pos = None
    # number of cells
    y_cells = 7
    x_cells = 17
    vlines = []
    hlines = []
    paused = True
    # 'bool' field to hold the cells
    board = None
    neighbors = None
    position = None
    initialized = False

    def register(self):
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_LEFT)), self.cursor_left)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_RIGHT)), self.cursor_right)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_UP)), self.cursor_up)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_DOWN)), self.cursor_down)
        self.events.on('input.up.{}'.format(Input.key_name(Input.KEY_SPACE)), self.cursor_toggle)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_A)), self.simulation_toggle)
        self.events.on('input.up.char', self.check_input)
        self.reset()

    def update(self, delta=0):
        self.fill_neighbors()
        self.tick()

    def render(self):
        self.display.fill(display.BACKGROUND)
        for i in range(self.y_cells+1):
            delta_y = 16*(i)
            self.display.hline(self.x_offset, self.y_offset+delta_y, self.display.width-2*self.x_offset)
        for i in range(self.x_cells+1):
            delta_x = 16*(i)
            self.display.vline(self.x_offset+delta_x, self.y_offset, self.display.height-2*self.y_offset)
        if self.paused:
            # Draw cursor
            p = self.get_cell_center(self.cursor_pos[0], self.cursor_pos[1])
            self.display.fill_circ(p[0], p[1], self.box_size // 2 - self.cell_gap, color=display.FOREGROUND if self.board[self.cursor_pos[0]][self.cursor_pos[1]] == 0 else display.BACKGROUND)
        else:
            for xi, x in enumerate(self.board):
                for yi, y in enumerate(x):
                    if y == 1:
                        p = self.get_rect_coords(xi, yi)
                        self.display.fill_rect(p[0], p[1], p[2], p[3])
        self.display.update()

    def cursor_left(self, event):
        self.cursor_pos[0] = max(0, self.cursor_pos[0] - 1)

    def cursor_right(self, event):
        self.cursor_pos[0] = min(self.x_cells - 1, self.cursor_pos[0] + 1)

    def cursor_up(self, event):
        self.cursor_pos[1] = max(0, self.cursor_pos[1] - 1)

    def cursor_down(self, event):
        self.cursor_pos[1] = min(self.y_cells - 1, self.cursor_pos[1] + 1)

    def cursor_toggle(self, event):
        self.board[self.cursor_pos[0]][self.cursor_pos[1]] = 1 - self.board[self.cursor_pos[0]][self.cursor_pos[1]]

    def simulation_toggle(self, event):
        self.paused = not self.paused

    def reset(self):
        self.cursor_pos = [0, 0]
        self.board = []
        self.neighbors = []
        for x in range(self.x_cells):
            x_cells = []
            for y in range(self.y_cells):
                x_cells.append(0)
            # unless you want some weird 2d fibonacci, pass copies [:]
            self.board.append(x_cells[:])
            self.neighbors.append(x_cells[:])

    def check_alive(self):
        for xi in range(self.x_cells):
            for yi in range(self.y_cells):
                if self.board[xi][yi] == 1:
                    return True
        return False

    def tick(self):
        for xi in range(self.x_cells):
            for yi in range(self.y_cells):
                val = self.board[xi][yi]
                neigh = self.neighbors[xi][yi]
                new_val = 0
                if val == 1:
                    if neigh < 2:
                        new_val = 0
                    elif neigh < 4:
                        new_val = 1
                    else:
                        new_val = 0
                else:
                    if neigh == 3:
                        new_val = 1
                self.board[xi][yi] = new_val

    def get_cell_center(self, xi, yi):
        x = 16 * xi + self.x_offset + self.box_size // 2
        y = 16 * yi + self.y_offset + self.box_size // 2
        return x, y

    def fill_neighbors(self):
        for xi in range(self.x_cells):
            for yi in range(self.y_cells):
                self.neighbors[xi][yi] = self.get_cell_neighbors(xi, yi)

    def get_cell_neighbors(self, xi, yi):
        n = 0
        xm = xi-1
        xp = (xi+1)%self.x_cells
        ym = yi-1
        yp = (yi+1)%self.y_cells
        b = self.board[:]
        n = b[xm][yp] + b[xm][yi] + b[xm][ym] +b[xi][yp] + b[xi][ym] + b[xp][yp] + b[xp][yi] + b[xp][ym]
        return n

    def get_rect_coords(self, xi, yi):
        start_x = 16*(xi)+self.x_offset+self.cell_gap
        start_y = 16*(yi)+self.y_offset+self.cell_gap
        end_x = 16*(xi+1)+self.x_offset-self.cell_gap+1
        end_y = 16*(yi+1)+self.y_offset-self.cell_gap+1
        return start_x, start_y, end_x, end_y

    def back(self, event):
        return Kernel.ACTION_LOAD_SCREEN, 0


class App(app.App):
    VERSION = 1

    screens = [
        MenuScreen(),
        GameScreen(continuous_rendering=True),
    ]
