import display

from system import app, screen, Kernel, Input


class TokenScreen(screen.Screen):

    fill = '_'
    token = ''
    errors = None

    def register(self):
        self.events.on('input.up.char', self.parse_input)
        self.events.on('input.up.{}'.format(Input.key_name(Input.KEY_BACKSPACE)), self.backspace)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_A)), self.submit)

    def get_text(self):
        return '{} {} {}\n  {}  {}'.format(
            (self.token[0:4] + self.fill * 4)[:4],
            (self.token[4:8] + self.fill * 4)[:4],
            (self.token[8:12] + self.fill * 4)[:4],
            (self.token[12:16] + self.fill * 4)[:4],
            (self.token[16:20] + self.fill * 4)[:4],
        )

    def update(self):
        font = self.display.font()
        id = self.kernel.id()
        token = self.get_text()
        if self.errors is None:
            errors = ''
        elif len(self.errors) is 0:
            errors = 'Success!'
        else:
            errors = '\n'.join(self.errors)
        space1 = 12
        space2 = 22
        space3 = 16
        self.display.font(display.FONT_DEJAVU_16)
        self.display.text(id, 0, y=0, wrap=display.WRAP_INDENT)
        size1 = self.display.text(id, 0, y=0, max_width=self.display.width - 2 * space1, wrap=display.WRAP_INDENT)
        x1 = self.display.width // 2 - size1['width'] // 2
        y1 = 6
        self.display.font(display.FONT_DEJAVU_24)
        size2 = self.display.text(token, 0, y=0, max_width=self.display.width - 2 * space2, wrap=display.WRAP_INDENT)
        x2 = self.display.width // 2 - size2['width'] // 2
        y2 = y1 * 2 + size1['height']
        self.display.font(display.FONT_DEJAVU_12)
        size3 = self.display.text(errors, 0, y=0, max_width=self.display.width - 2 * space3, wrap=display.WRAP_INDENT)
        x3 = self.display.width // 2 - size3['width'] // 2
        y3 = y2 + size2['height'] + y1
        self.display.fill(display.BACKGROUND)
        self.display.font(display.FONT_DEJAVU_16)
        self.display.text(id, x1, y=y1, max_width=self.display.width - 2 * space1, wrap=display.WRAP_INDENT)
        self.display.font(display.FONT_DEJAVU_24)
        self.display.text(self.get_text(), x2, y=y2, max_width=self.display.width - 2 * space2, wrap=display.WRAP_INDENT)
        self.display.font(display.FONT_DEJAVU_12)
        self.display.text(errors, x3, y=y3, max_width=self.display.width - 2 * space3, wrap=display.WRAP_INDENT)
        self.display.update()
        self.display.font(font)

    def parse_input(self, event):
        if not event.key in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return
        if len(self.token) < 20:
            self.token += event.key
        return Kernel.ACTION_RELOAD

    def backspace(self, event):
        self.token = self.token[:-1]
        return Kernel.ACTION_RELOAD

    def submit(self, event):
        if len(self.token) != 20:
            return
        try:
            self.kernel.wifi(10000)
            r = self.kernel.http.post('/token/submit', json={'token': self.token})
            if r is None or r.status_code is not 200:
                self.errors = ['Transmision error']
            else:
                print(r.status_code)
                data = r.json()
                if data['response']['success']:
                    self.token = ''
                    self.errors = []
                else:
                    self.errors = data['response']['errors']
            self.kernel.wifi_off()
        except OSError:
            r = None
        return Kernel.ACTION_RELOAD


class App(app.App):

    VERSION = 1

    screens = [
        TokenScreen(),
    ]


