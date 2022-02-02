from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from datetime import datetime

expedit_list = []

class History(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        for i in expedit_list:
            size = dp(50)
            lb = Label(text=str(i), size_hint=(1, None), height=size)
            self.add_widget(lb)

class RegisterBtn(Button):
    my_text = StringProperty()
    def on_button_click(self):
        print("Button Clicked")
        input_text = self.parent.parent.ids.input_money.text
        if input_text.isdigit():
            print("Digit!")
            item = {
                "time": datetime.now().strftime("%Y/%m/%d"),
                "expedite": input_text,
            }
            expedit_list.append(item)
            size = dp(50)
            lb = Label(text=str(item), size_hint=(1, None), height=size)
            self.parent.parent.ids.svc.ids.history.add_widget(lb)
            self.parent.parent.ids.accumulated_money.text = str(int(self.parent.parent.ids.accumulated_money.text) - int(input_text))

        else:
            print("No digit")


class TheLabApp(App):
    current_money = 0
    accumulated_expedite = 0
    target_money = 1000000
    now = datetime.now()
    seconds_since_this_month = (now - now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    seconds_in_this_month = (
            now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0) - now.replace(day=1,
                                                                                                             hour=0,
                                                                                                             minute=0,
                                                                                                             second=0,
                                                                                                             microsecond=0)).total_seconds()
    passing_speed = target_money / seconds_in_this_month

    def on_start(self):
        Clock.schedule_interval(self.update_label, 1/self.passing_speed)
        start_point = self.target_money*self.seconds_since_this_month/self.seconds_in_this_month
        self.current_money = int(start_point)
        self.root.ids.accumulated_money.text = str(self.current_money)

    def update_label(self, *args):

        self.root.ids.accumulated_money.text = str(int(self.root.ids.accumulated_money.text) + 1)
        self.current_money = int(self.root.ids.accumulated_money.text)
        print(self.current_money)

TheLabApp().run()