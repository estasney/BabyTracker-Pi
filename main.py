import kivy
kivy.require('1.10.0')
from Local_AppConfig import AppConfig, ApiConfig
from kivy.properties import StringProperty, BooleanProperty, DictProperty
from kivy.clock import Clock
from kivy.app import App
import sqlite3
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

# Provide setup for Google Forms
import Data_Functions
import time
from time import strftime
from timeit import default_timer as timer
from datetime import timedelta, datetime
import pickle
from functools import partial

form_url = AppConfig.form_url
entryid_action = AppConfig.entryid_action
entryid_local_time = AppConfig.entryid_local_time
backup_csv = AppConfig.backup_csv
db_conn = sqlite3.connect(AppConfig.sqlite_db, detect_types=sqlite3.PARSE_DECLTYPES)
log_to_google = AppConfig.log_to_google
log_to_csv = AppConfig.log_to_csv
log_to_pkl = AppConfig.log_to_pkl
log_to_gui = AppConfig.log_to_gui
log_to_tally = AppConfig.log_to_tally
log_to_sql = AppConfig.log_to_sql
api_key = ApiConfig.api_key
city_id = ApiConfig.city_id


class pop(BoxLayout):

    Window.clearcolor = (0.2, 0.21, 0.27, 1)

    def post_data_on_close(self, instance):
        if log_to_google:
            params = Data_Functions.params_builder(entry_ids=(entryid_action, entryid_local_time),
                                                   entry_contents=(self.but.text, strftime("%I:%M %p", time.localtime())))
            Data_Functions.post_google_form(form_url, params, backup_csv)
            self.main_pop.dismiss()
        else:
            print("Entry Not Logged to Google")

    def post_data_on_open(self, entry_content):
        if log_to_google:
            params = Data_Functions.params_builder(entry_ids=(entryid_action, entryid_local_time),
                                                   entry_contents=(entry_content, strftime("%I:%M %p", time.localtime())))
            Data_Functions.post_google_form(form_url, params, backup_csv)
        else:
            print("Entry Not Logged To Google")

        if log_to_sql:
            c = db_conn.cursor()
            c.execute('INSERT INTO logs VALUES (?, ?, ?)', (None, datetime.now(), entry_content))
            db_conn.commit()

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
    weather = StringProperty()
    widget_open_times = DictProperty({'medtime': 0, 'feedtime': 0})
    widget_elapsed_times = DictProperty({'medtime': '0', 'feedtime': '(0:00:00)'})
    last_logs = DictProperty({k: '' for k in range(10)})
    elapsed_meta = StringProperty()
    meta_markup_bool = BooleanProperty()

    def get_the_weather(self, *args):
        self.weather = Data_Functions.fetch_weather(city_id, api_key)

    def setup_db(self, *args):
        # Creates the SQL Table if does not exist
        c = db_conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logs 
                            (EntryID INTEGER PRIMARY KEY,
                            Time TIMESTAMP,
                            Action TEXT)''')
        db_conn.commit()

    def fetch_last_n(self, top_n, *largs):
        # Query SQL DB for last ten entries
        c = db_conn.cursor()
        c.execute('SELECT * from logs ORDER BY Time DESC LIMIT {}'.format(top_n))
        last_n = c.fetchall()
        for index, lt in enumerate(last_n):
            clock_time = lt[1].strftime("%I:%M %p")
            day = lt[1].strftime("%b-%d")
            action = lt[2]
            entry = "{} --- {} ({})".format(action, clock_time, day)
            self.last_logs[index] = entry

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
        self.setup_db()
        self.get_the_weather()
        Clock.schedule_interval(self.update, 0.1)
        Clock.schedule_interval(self.get_elapsed_widget_time, 0.1)
        Clock.schedule_interval(partial(self.fetch_last_n, 10), 10)
        Clock.schedule_interval(self.get_the_weather, 1800)
        self.fetch_last_n(top_n=10)
        return pop()


PopApp().run()
