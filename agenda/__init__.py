import display
import utime
from system import app, screen, Input, Kernel, Accelerometer


class Agenda:

    def __init__(self, days, x1=65, x2=235):
        self.xDraw1 = x1
        self.xDraw2 = x2
        if days is None:
            days = []
        self.days = days
        self.dayNumber = 0
        self.trackNumber = 0
        self.offset = 0
        self.showRating = False
        self.rating = 0
        self.yVoting = 25
        self.xVoting = 40
        self.nahuel = [
            dict(
                name='Wednesday',
                tracks=[
                    dict(
                        name='Elevator 1',
                        talks=[
                            dict(
                                id=1,
                                title='Keynote "NFC - Nahuel Field Communication, discussing a method of telepathy between Nahuels"',
                                speaker='Nahuel Grisolia',
                                time='09:00',
                            ),
                            dict(
                                id=2,
                                title='Mate Break',
                                speaker='',
                                time='10:00',
                            ),
                            dict(
                                id=3,
                                title='Serverless Snape - demystifying the need for hardware',
                                speaker='Nahuel Branco',
                                time='10:30',
                            ),
                            dict(
                                id=4,
                                title='Military-grade BROT64, the encryption scheme nobody talks about',
                                speaker='Nahuel Turbing & Nahuel Heinzelmann',
                                time='11:30',
                            ),
                            dict(
                                id=5,
                                title='Chimichurri Break',
                                speaker='',
                                time='12:30',
                            ),
                            dict(
                                id=6,
                                title='IPvSexy, Germany and IPv6',
                                speaker='Nahuel Rey',
                                time='13:30',
                            ),
                            dict(
                                id=7,
                                title='Ethics of conference hijacking',
                                speaker='Nahuel Hager',
                                time='14:30',
                            ),
                            dict(
                                id=8,
                                title='Mate Break',
                                speaker='',
                                time='15:30',
                            ),
                            dict(
                                id=9,
                                title='Just Out Of Time Rapid Hardware Development on Fire - How I soldered 500 badges by hand',
                                speaker='Nahuel Gough',
                                time='16:00',
                            ),
                            dict(
                                id=10,
                                title='SHARED DINNER - You may freely share your dinner with anyone, if you\'d like to',
                                speaker='',
                                time='17:00',
                            ),
                        ]
                    )
                ]
            ),
            dict(
                name='Thursday',
                tracks=[
                    dict(
                        name='Elevator 1',
                        talks=[
                            dict(
                                id=11,
                                title='Exploitable backdoors in Ghidra',
                                speaker='Nahuel Auglend',
                                time='09:00',
                            ),
                            dict(
                                id=12,
                                title='Mate Break',
                                speaker='',
                                time='10:00',
                            ),
                            dict(
                                id=13,
                                title='If only - examining a computer language without \'else\'',
                                speaker='Nahuel Albertini',
                                time='10:30',
                            ),
                            dict(
                                id=14,
                                title='Dark clouds, dark lightning, dark blockchain',
                                speaker='Nahuel D. Sanchez',
                                time='11:30',
                            ),
                            dict(
                                id=15,
                                title='Asado Break',
                                speaker='',
                                time='12:30',
                            ),
                            dict(
                                id=16,
                                title='New old things: an examination of the latest smartphones',
                                speaker='Nahuel Cayetano Riva',
                                time='13:30',
                            ),
                            dict(
                                id=17,
                                title='Cyberdiplomacy strategies for sensitive CISOs',
                                speaker='Nahuel Hauenstein',
                                time='14:30',
                            ),
                            dict(
                                id=18,
                                title='Mate Break',
                                speaker='',
                                time='15:30',
                            ),
                            dict(
                                id=19,
                                title='Closing Keynote - Lit Ways to Spend Your 25th Birthday, Nerd',
                                speaker='Nahuel Boissard',
                                time='16:00',
                            ),
                            dict(
                                id=19,
                                title='Fernet Cola & something to drink',
                                speaker='',
                                time='Later',
                            ),
                        ]
                    )
                ]
            ),
            dict(
                name='Friday',
                tracks=[
                    dict(
                        name='Squaretables 1',
                        talks=[
                            dict(
                                id=20,
                                title='Passive Directory',
                                speaker='',
                                time='09:00',
                            ),
                        ]
                    ),
                    dict(
                        name='Squaretables 2',
                        talks=[
                            dict(
                                id=21,
                                title='Incident Ignorance',
                                speaker='',
                                time='09:00',
                            ),
                        ]
                    ),
                ]
            ),
        ]
        self.isNahuel = False

    def activateNahuel(self):
        self.isNahuel = True
        self.dayNumber = 0
        self.trackNumber = 0
        self.offset = 0
        self.showRating = False

    @property
    def entries(self):
        return self.days if not self.isNahuel else self.nahuel

    def right(self):
        if self.showRating:
            self.voteUp()
        else:
            if self.trackNumber < len(self.entries[self.dayNumber]['tracks']) - 1:
                self.trackNumber += 1
            elif self.dayNumber < len(self.entries) - 1:
                self.trackNumber = 0
                self.dayNumber += 1
            self.offset = min(self.offset, len(self.entries[self.dayNumber]['tracks'][self.trackNumber]['talks']) - 1)

    def left(self):
        if self.showRating:
            self.voteDown()
        else:
            if self.dayNumber > 0 and self.trackNumber == 0:
                self.dayNumber -= 1
                self.trackNumber = len(self.entries[self.dayNumber]['tracks']) - 1
            elif self.trackNumber > 0:
                self.trackNumber -= 1
            self.offset = min(self.offset, len(self.entries[self.dayNumber]['tracks'][self.trackNumber]['talks']) - 1)


    def up(self):
        self.offset = max(0, self.offset - 1)

    def down(self):
        self.offset = min(self.offset + 1, len(self.entries[self.dayNumber]['tracks'][self.trackNumber]['talks']) - 1)

    def back(self):
        if self.showRating:
            self.showRating = False
            return Kernel.ACTION_RELOAD
        else:
            return Kernel.ACTION_LOAD_APP, Kernel.DEFAULT_APP

    def draw(self, screen, clear=True):
        if clear:
            screen.fill(display.BACKGROUND)
        if self.showRating and not self.isNahuel:
            self.drawVote(screen)
        elif len(self.entries) is 0:
            screen.text("Agenda is empty!",0 ,0 )
        else:
            # Hilfsvariable fuer den Abstand der Eintraege
            distance = 25

            # Eintraege
            day = self.entries[self.dayNumber]
            tracks = day['tracks']
            track = tracks[self.trackNumber]
            talks = track['talks']
            talk = talks[self.offset]
            screen.text(talk['time'][:5], x=5, y=distance, wrap=display.WRAP_INDENT)

            counterTitle = \
            screen.text(talk['title'], x=self.xDraw1 + 5, y=distance, wrap=display.WRAP_INDENT, max_width=self.xDraw2 - self.xDraw1 - 10)[
                'height']

            counterSpeaker = \
            screen.text(talk['speaker'], x=self.xDraw2 + 5, y=distance, wrap=display.WRAP_INDENT, max_width=296 - self.xDraw2 - 10)[
                'height']

            distance += max(counterTitle, counterSpeaker) + 5

            # Layout
            screen.hline(0,15, width=screen.width)
            screen.vline(self.xDraw1, 0, height=screen.height)
            screen.vline(self.xDraw2, 0, height=screen.height)
            screen.text('TIME', x=5, y=3)
            screen.text('SPEAKER', x=self.xDraw2 + 5, y=3)
            screen.text(track['name'], x=self.xDraw1 + 5, y=3, wrap=display.WRAP_INDENT, max_width=self.xDraw2 - 5)
            screen.text(day['name'], x= self.xDraw1 + 5, y=screen.height-screen.fontSize[1])

            screen.text('Track >\nTrack <\nTalk  ^\nTalk  v\n' + ('Vote  V' if not self.isNahuel else ''), x=5, y=screen.height - 5*screen.fontSize[1], wrap=display.WRAP_INDENT, max_width=self.xDraw1-5)
            screen.font(display.FONT_DEJAVU_12)

        screen.update()

    def drawStars(self, screen):
        x = (screen.width-10*screen.fontSize[0])//2
        y = (screen.height//2)-screen.fontSize[1]//2
        font = screen.font()
        screen.font(display.FONT_DEJAVUEMOJI_16)
        for i in range(5):
            x += screen.text(b'\x86' if i < self.rating else b'\x87', x=x, y=y)['width']
        screen.font(font)

    def vote(self):
        if self.isNahuel:
            return
        self.showRating = True
        self.rating = 3

    def submitVote(self):
        if not self.showRating or self.isNahuel:
            return
        self.showRating = False
        return self.getTalk()['id']

    def voteUp(self):
        self.rating += 1

    def voteDown(self):
        self.rating -= 1

    def getTalk(self):
        if self.entries is None:
            return
        day = self.entries[self.dayNumber]
        if day is None:
            return
        tracks = day['tracks']
        if tracks is None:
            return
        track = tracks[self.trackNumber]
        if track is None:
            return
        talks = track['talks']
        if talks is None:
            return
        return talks[self.offset]

    def drawVote(self, screen):

        # Layout
        screen.hline(0, self.yVoting, width=screen.width)
        screen.hline(0, screen.height-self.yVoting, width=screen.width)
        font = screen.font()
        screen.font(display.FONT_DEJAVUEMOJI_16)
        screen.text('VOTING', x=(screen.width-6*screen.fontSize[0])//2, y=(self.yVoting//2)-5)
        screen.font(font)
        screen.text('< STARS >', x=(screen.width-9*screen.fontSize[0])//2, y=screen.height-(self.yVoting//2)-5)
        screen.vline(screen.width-self.xVoting, screen.height-self.yVoting, height=screen.height)
        screen.text('OK o', x=screen.width-self.xVoting//2-screen.fontSize[0], y=screen.height-screen.fontSize[1]-5)

        # Zugriff
        talk = self.getTalk()

        # Hilfsvariable fuer For-Schleife title
        x1=10

        if len(talk['title'])>40:
            for i in range(35):
                x1 += screen.text(talk['title'][i], x=x1, y=screen.height // 2 - 2 * screen.fontSize[1])['width']

            screen.text('...', x=x1, y=screen.height // 2 - 2 * screen.fontSize[1])
        else:
            screen.text(talk['title'], x=(screen.width // 2 - len(talk['title']) // 2 * screen.fontSize[0]),
                        y=screen.height // 2 - 2 * screen.fontSize[1])

        # Hilfsvariable fuer For-Schleife speaker
        x2 = 10

        if len(talk['speaker'])>40:
            for i in range(35):
                x2 += screen.text(talk['speaker'][i], x=x2, y=screen.height // 2 + screen.fontSize[1] + screen.fontSize[1] // 2)['width']

            screen.text('...', x=x2, y=screen.height // 2 + screen.fontSize[1] + screen.fontSize[1] // 2)
        else:
            screen.text(talk['speaker'], x=(screen.width // 2 - len(talk['speaker']) // 2 * screen.fontSize[0]),
                        y=screen.height // 2 + screen.fontSize[1] + screen.fontSize[1] // 2)
            self.drawStars(screen)


class AgendaScreen(screen.Screen):

    agenda = None

    def register(self):
        self.agenda = Agenda(self.storage.SCHEDULE)

        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_LEFT)), self.left)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_RIGHT)), self.right)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_UP)), self.up)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_DOWN)), self.down)
        self.events.on('input.up.{}'.format(Input.key_name(Input.KEY_V)), self.vote)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_A)), self.submitVote)
        self.events.on('input.nahuel', self.nahuel)

    def update(self):
        self.agenda.draw(self.display)

    def left(self, event):
        self.agenda.left()
        return Kernel.ACTION_RELOAD

    def right(self, event):
        self.agenda.right()
        return Kernel.ACTION_RELOAD

    def up(self, event):
        self.agenda.up()
        return Kernel.ACTION_RELOAD

    def down(self, event):
        self.agenda.down()
        return Kernel.ACTION_RELOAD

    def back(self, event):
        return self.agenda.back()

    def vote(self, event):
        self.agenda.vote()
        return Kernel.ACTION_RELOAD

    def submitVote(self, event):
        result = self.agenda.submitVote()
        if result is None:
            return
        try:
            self.kernel.wifi(10000)
            r = self.kernel.http.post('/vote/send', json={'talk': result, 'rating': self.agenda.rating})
            try:
                r.content
            except:
                pass
            self.kernel.wifi_off()
        except OSError:
            r = None
        return Kernel.ACTION_RELOAD

    def nahuel(self, event):
        self.agenda.activateNahuel()
        return Kernel.ACTION_RELOAD


class App(app.App):

    VERSION = 1

    screens = [
        AgendaScreen(),
    ]
