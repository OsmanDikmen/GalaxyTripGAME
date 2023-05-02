from kivy.uix.relativelayout import RelativeLayout


def on_touch_down(self, touch):

    #state_game_over = False
    #state_game_has_started = False


    if not self.state_game_over and self.state_game_has_started:

        if touch.x <= self.width / 2:
            self.current_speed_x = self.SPEED_X
        else:
            self.current_speed_x = -self.SPEED_X
    return super(RelativeLayout, self).on_touch_down(touch)


def on_touch_up(self, touch):
    self.current_speed_x = 0