from kivy.app import App
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import pickle
from sklearn.linear_model import LinearRegression

class BeerConsuptiom(Screen):
    entrada = StringProperty()

    def do_simulate(self, temp_max, chuva, fds):
        app = App.get_running_app()

        app.temp_max = temp_max
        app.chuva = chuva
        app.fds = fds

        modelo = open('../datasets/modelo_consumo_cerveja','rb')
        lm_new = pickle.load(modelo)
        modelo.close()
        
        entrada=[[
                float(temp_max if temp_max else 0),
                float(chuva if chuva else 0),
                float(fds if fds else 0),
                ]]

        self.entrada = str(lm_new.predict(entrada)[0].round(2))
        self.manager.get_screen('simulator').reset_form()

    def reset_form(self):
        self.ids['temp_max'].text = ""
        self.ids['chuva'].text = ""
        self.ids['fds'].text = ""

class BeerConsuptiomSimulatorApp(App):
    temp_max = StringProperty(None)
    chuva = StringProperty(None)
    fds = StringProperty(None)

    def build(self):
        manager = ScreenManager()
        manager.add_widget(BeerConsuptiom(name='simulator'))
        return manager

if __name__ == '__main__':
    BeerConsuptiomSimulatorApp().run()
