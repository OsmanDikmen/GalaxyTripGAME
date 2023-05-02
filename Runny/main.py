import random

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Line, Quad, Triangle
from kivy.lang import Builder
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):
    from transforms import transform_2d, transform_perspective, transfor
    from user_actions import on_touch_down, on_touch_up

    menu_widget = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    menu_title = StringProperty("R   U   N   N   Y")
    menu_button_title = StringProperty("START")
    score_txt = StringProperty("Score: 0")
    way = StringProperty(" ")
    voice_title = StringProperty("Mute")
    hight_score_txt = StringProperty("Score: 0")
    bck_image = StringProperty("image/bckimg.jpg")

    V_NB_LINES = 8
    V_NB_SPACING = .4
    verticial_lines = []

    H_NB_LINES = 10
    H_NB_SPACING = .25
    horizontal_lines = []

    current_offset_y = 0
    SPEED = 1.1
    current_y_loop = 0

    current_offset_x = 0
    current_speed_x = 0
    SPEED_X = 3.0

    NB_TILES = 4
    tiles = []
    tiles_cordinates = []

    SHIP_WITH = .1
    SHIP_HEIGHT = 0.035
    SHIP_Y_BASE = 0.04
    ship = None
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    state_game_over = False
    state_game_has_started = False
    start_music = True

    sound_main = None

    store = JsonStore('hello.json')

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_audio()
        self.init_verticial_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.reset_game()
        self.bck()



        #self.store.put('tito', HighScore="0")
        Clock.schedule_interval(self.update, 1.0/60.0)

    def init_audio(self):
       self.sound_main = SoundLoader.load("music/bckmusc.mp3")


       self.sound_main.volume = .8

    def reset_game(self):
        self.current_offset_y = 0
        self.current_y_loop = 0
        self.current_offset_x = 0
        self.current_speed_x = 0

        self.tiles_cordinates = []
        self.pre_fill_tile_coordinates()
        self.generate_tiles_coordinates()

        self.state_game_over = False





    def check_ship_collision(self):
       for i in range(0, len(self.tiles_cordinates)):
           ti_x, ti_y = self.tiles_cordinates[i]
           if ti_y > self.current_y_loop + 1:
               return False
           if self.check_ship_collision_with_tile(ti_x, ti_y):
               return True
       return False


    def check_ship_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)

        for i in range(0, 3):
            px, py = self.ship_coordinates[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False


    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.NB_TILES):
                self.tiles.append(Quad())


    def init_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()


    def update_ship(self):
        center_x = self.width / 2
        base_y = self.SHIP_Y_BASE * self.height
        ship_half_width = self.SHIP_WITH * self.width /2
        ship_height = self.SHIP_HEIGHT * self.height

        self.ship_coordinates[0] = (center_x - ship_half_width, base_y)
        self.ship_coordinates[1] = (center_x, base_y + ship_height)
        self.ship_coordinates[2] = (center_x + ship_half_width, base_y)

        x1, y1 = self.transfor(*self.ship_coordinates[0])
        x2, y2 = self.transfor(*self.ship_coordinates[1])
        x3, y3 = self.transfor(*self.ship_coordinates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]


    def pre_fill_tile_coordinates(self):
        for i in range(0, 7):
            self.tiles_cordinates.append((0, i))



    def generate_tiles_coordinates(self):
        last_x = 0
        last_y = 0

        for i in range(len(self.tiles_cordinates) - 1, -1, -1):
            if self.tiles_cordinates[i][1]< self.current_y_loop:
                del self.tiles_cordinates[i]


        if len(self.tiles_cordinates) > 0:
            last_cordinates = self.tiles_cordinates[-1]
            last_x = last_cordinates[0]
            last_y = last_cordinates[1] + 1

        for i in range(len(self.tiles_cordinates), self.NB_TILES):
            r = random.randint(0, 2)

            start_index = -int(self.V_NB_LINES / 2) + 1
            end_index = start_index + self.V_NB_LINES - 1

            if last_x <= start_index:
                r = 1
            if last_x >= end_index:
                r = 2

            self.tiles_cordinates.append((last_x, last_y))

            if r == 1:
                last_x += 1
                self.tiles_cordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_cordinates.append((last_x, last_y))

            if r == 2:
                last_x -= 1
                self.tiles_cordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_cordinates.append((last_x, last_y))

            last_y += 1



    def init_verticial_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            #self.line=Line(points=[100, 0, 100, 100])
            for i in range(0, self.V_NB_LINES):
                self.verticial_lines.append(Line())


    def get_line_x_from_index(self, index):
        center_line_x = self.perspective_point_x
        spacing = self.V_NB_SPACING * self.width
        ofset = index - 0.5
        line_x = center_line_x + ofset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.H_NB_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x= self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_verticial_lines(self):
        start_index = -int(self.V_NB_LINES/2) + 1

        for i in range(start_index, start_index + self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transfor(line_x, 0)
            x2, y2 = self.transfor(line_x, self.height)
            self.verticial_lines[i].points = [x1, y1, x2, y2]

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            #self.line=Line(points=[100, 0, 100, 100])
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_tiles(self):
        for i in range(0, self.NB_TILES):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_cordinates[i]
            xmin, ymin =self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)


            x1, y1 = self.transfor(xmin, ymin)
            x2, y2 = self.transfor(xmin, ymax)
            x3, y3 = self.transfor(xmax, ymax)
            x4, y4 = self.transfor(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_horizontal_lines(self):

        start_index = -int(self.V_NB_LINES / 2) + 1
        end_index = start_index + self.V_NB_LINES - 1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for i in range(0, self.H_NB_LINES):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transfor(xmin, line_y)
            x2, y2 = self.transfor(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]


    def update(self, dt):
        time_factor = dt*60
        self.update_verticial_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()
        self.score_jason_UP()
        self.bck_change()
        self.time_change()



        if not self.state_game_over and self.state_game_has_started:
            speed_y = self.SPEED * self.height / 100
            self.current_offset_y += speed_y * time_factor

            spacing_y = self.H_NB_SPACING * self.height

            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.generate_tiles_coordinates()
                self.score_txt ="Score: "+str(self.current_y_loop)

            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x += speed_x * time_factor

        if not self.check_ship_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_title = "G  A  M  E    O  V  E  R"
            self.menu_button_title = "RESTART"
            self.menu_widget.opacity = 1
            self.sound_main.stop()
            print("game over")
            if self.store:
                if self.current_y_loop >= int(self.store.get('tito')['HighScore']):
                    self.score_jason()


    def on_menu_button_pressed(self):
        print("button")
        self.reset_game()
        self.state_game_has_started = True
        self.menu_widget.opacity = 0

        if self.start_music:
            self.sound_main.play()


    def on_voice_pressed(self):

        if self.voice_title =="Mute":
            self.start_music = False
            print("button31")
            self.voice_title = "Voice"
        else:
            self.start_music = True
            print("button32")
            self.voice_title = "Mute"

    def score_jason(self):
        self.store.put('tito', HighScore=str(self.current_y_loop))
        print(self.store.get('tito')['HighScore'])

    def score_jason_UP(self):
        self.hight_score_txt = "High Score: " + self.store.get('tito')['HighScore']

    def bck_change(self):
        if self.current_y_loop > int( self.store.get('tito')['HighScore']):
            if 400>self.current_y_loop > 250:
                self.bck_image = "image/dragon.jpg"
                self.SPEED = 1.2
            elif 600>self.current_y_loop > 400:
                self.bck_image = "image/sea.jpg"
                self.SPEED = 1.3
            elif 900>self.current_y_loop > 600:
                self.bck_image = "image/sea.jpg"
                self.SPEED = 1.4
            elif self.current_y_loop > 1100:
                self.SPEED = 1.6
                self.bck_image = "image/sea.jpg"

    def bck(self):
        if self.store:
            if 400 > int( self.store.get('tito')['HighScore']) > 250:
                self.bck_image = "image/dragon.jpg"
            elif 600> int(self.store.get('tito')['HighScore']) > 400:
                self.bck_image = "image/sea.jpg"
            elif 900> int(self.store.get('tito')['HighScore']) > 600:
                self.bck_image = "image/light.jpg"
            elif int(self.store.get('tito')['HighScore']) > 1100:
                self.bck_image = "image/moutans.jpg"

    def time_change(self):
        if self.store:
            if 250 > self.current_y_loop > 0:
                self.way = str(250 - self.current_y_loop) + " last steps to jump in time"
            if 400 > self.current_y_loop > 250:
                self.way = str(650 - self.current_y_loop) + " last steps to jump in time"
            if 600 > self.current_y_loop > 400:
                self.way = str(1250 - self.current_y_loop) + " last steps to jump in time"
            elif 900 > self.current_y_loop > 600:
                self.way = str(2150 - self.current_y_loop) + " last steps to jump in time"
            elif self.current_y_loop > 1100:
                self.way ="You're on your way grand master"




class GalaxyApp(App):
    pass

GalaxyApp().run()