import kivy
kivy.require('1.10.0')
from Local_AppConfig import AppConfig
from kivy.properties import StringProperty, BooleanProperty, DictProperty
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

# Provide setup for Google Forms
import GoogleForms
import time
from time import strftime
from timeit import default_timer as timer
from datetime import timedelta
import pickle

form_url = AppConfig.form_url
entryid_action = AppConfig.entryid_action
entryid_local_time = AppConfig.entryid_local_time
backup_csv = AppConfig.backup_csv
log_to_google = AppConfig.log_to_google
log_to_csv = AppConfig.log_to_csv
log_to_pkl = AppConfig.log_to_pkl
log_to_gui = AppConfig.log_to_gui
log_to_tally = AppConfig.log_to_tally


class pop(BoxLayout):

    Window.clearcolor = (0.2, 0.21, 0.27, 1)

    def post_data_on_close(self, instance):
        params = GoogleForms.params_builder(entry_ids=(entryid_action, entryid_local_time),
                                            entry_contents=(self.but.text, strftime("%I:%M %p", time.localtime())))
        GoogleForms.post_google_form(form_url, params, backup_csv, log_to_google)
        self.main_pop.dismiss()

    def post_data_on_open(self, entry_content):
        params = GoogleForms.params_builder(entry_ids=(entryid_action, entryid_local_time),
                                            entry_contents=(entry_content, strftime("%I:%M %p", time.localtime())))
        GoogleForms.post_google_form(form_url, params, backup_csv, log_to_google)

    def close_popup(self, instance):
        self.info_popup.dismiss()

    def elapsed_time(self, *args):
        open_time = float(self.open_time)
        now_time = timer()
        elapsed_time = round((now_time - open_time), 1)
        elapsed_time = int(elapsed_time)
        formatted_time = str(timedelta(seconds=elapsed_time))
        self.timer_label.text = formatted_time

    def get_the_time(self, indicator, target, pickle_file_name):
        if log_to_gui:
            target.text = indicator + " at " + strftime("%I:%M %p", time.localtime())
        if log_to_pkl:
            pickle_it = target.text
            output = open(pickle_file_name, 'wb')
            pickle.dump(pickle_it, output)
            output.close()

    def load_history(self, pickle_file_name, target):
        try:
            pkl_file = open(pickle_file_name, 'rb')
            loaded_history = pickle.load(pkl_file)
            target.text = loaded_history
        except:
            self.text = "No Record Found"

    def tally_count(self, pickle_file_name, target=None, tallybool=True):
        if log_to_tally:
            try:
                pkl_file = open(pickle_file_name, 'rb')
                current_count = pickle.load(pkl_file)
            except:
                current_count = "0"
                output_e = open(pickle_file_name, 'wb+')
                pickle.dump(current_count, output_e)
                output_e.close()
            current_count = int(current_count)
            newCount = str(current_count + 1)
            if target:
                target.text = newCount
                output = open(pickle_file_name, 'wb+')
                pickle.dump(newCount, output)
                output.close()
            else:
                if target:
                    target.text = str(current_count)
                return False
    pass


class PopApp(App):
    clock_time = StringProperty()
    start_time = StringProperty()
    widget_open_times = DictProperty({'medtime': 0, 'feedtime': 0})
    widget_elapsed_times = DictProperty({'medtime': '0', 'feedtime': '(0:00:00)'})
    elapsed_meta = StringProperty()
    meta_markup_bool = BooleanProperty()

    def update(self, *args):
        self.clock_time = strftime("%I:%M:%S %p", time.localtime())

    def update_widget_time(self, k, *args):
        self.widget_open_times[k] = timer()
        self.widget_elapsed_times[k] = '(0:00:00)'

    def get_elapsed_widget_time(self, *args):
        for k, v in self.widget_open_times.items():
            open_time = v
            now_time = timer()
            elapsed_time = round((now_time - open_time), 1)
            elapsed_time = int(elapsed_time)
            formatted_time = timedelta(seconds=elapsed_time)
            self.widget_elapsed_times[k] = "({})".format(str(formatted_time))



    def build(self):

        Clock.schedule_interval(self.update, 0.1)
        Clock.schedule_interval(self.get_elapsed_widget_time, 0.1)
        return pop()


PopApp().run()
