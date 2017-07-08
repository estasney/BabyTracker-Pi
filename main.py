import kivy
kivy.require('1.10.0')
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
# Provide setup for Google Forms
import GoogleForms
import time
from time import strftime
import pickle

form_url = "https://docs.google.com/forms/d/e/1FAIpQLSc4z-fmhAI9UfJziiv-Bh7yjx1jOFLOxJw77vbFdh5Cd61rjA/formResponse"
entryid = 'entry.1403445275'


class pop(BoxLayout):

    def logitclose(self, instance):
        params = GoogleForms.paramsbuilder(entryid=entryid, entrycontent=self.but.text)
        GoogleForms.postgoogleform(form_url, params)
        self.main_pop.dismiss()

    def logitopen(self, entrycontent):
        params = GoogleForms.paramsbuilder(entryid=entryid, entrycontent=entrycontent)
        GoogleForms.postgoogleform(form_url, params)

    def closeitinfo(self, instance):
        self.info_popup.dismiss()

    def info_pop(self, indicator, labelhint):

        self.box = FloatLayout()

        self.lab = Label(text=labelhint,max_lines=3, text_size=(400,250), valign='middle', halign='center', pos_hint= {'x':0,'y':.35} )

        self.but = Button(text="Close", size_hint=(1, .2), pos_hint={'x': 0, 'y': 0})

        self.box.add_widget(self.lab)

        self.box.add_widget(self.but)

        self.info_popup = Popup(title=indicator + " Cry", content=self.box, size_hint=(None, None), size=(450, 300)
                                , auto_dismiss=False, title_size=15)

        self.but.bind(on_release=self.closeitinfo)

        self.info_popup.open()

    def show_it(self, indicator):

        self.box = FloatLayout()

        self.lab = Label(text="Feeding " + indicator + " In Progress", font_size=15, pos_hint = {'x':0,'y':.35})

        self.but = Button(text="Complete " + indicator, size_hint = (1,.2), pos_hint = {'x':0,'y':0})

        self.box.add_widget(self.lab)

        self.box.add_widget(self.but)

        self.main_pop = Popup(title=indicator + " Feeding", content=self.box,
                              size_hint=(None, None), size=(450, 300), auto_dismiss=False, title_size=15)

        self.but.bind(on_release=self.logitclose)

        self.main_pop.open()

    def getthetime(self, indicator, target, pname):
        target.text = indicator + " at " + strftime("%I:%M %p", time.localtime())
        pickle_it = target.text
        output = open(pname, 'wb')
        pickle.dump(pickle_it, output)
        output.close()

    def load_history(self, pname, target):
        try:
            pkl_file = open(pname, 'rb')
            loaded_history = pickle.load(pkl_file)
            target.text = loaded_history
            print(loaded_history)
        except:
            self.text = ""



    #TODO - Add an elapsed time timer


    def tallycount(self, target, pname, tallybool=True):
        try:
            pkl_file = open(pname, 'rb')
            currentCount = pickle.load(pkl_file)
        except:
            currentCount = "0"
            output_e = open(pname, 'wb')
            pickle.dump(currentCount, output_e)
            output_e.close()
        currentCount = int(currentCount)
        newCount = str(currentCount + 1)
        if tallybool is True:
            target.text = newCount
            output = open(pname, 'wb')
            pickle.dump(newCount, output)
            output.close()
        else:
            target.text = str(currentCount)
            return False

    pass

class PopApp(App):
    time = StringProperty()
    def update(self, *args):
        self.time = strftime("%I:%M:%S %p", time.localtime())

    def build(self):
        Clock.schedule_interval(self.update, 0.1)

        return pop()

PopApp().run()



