from kivy.app import App
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

class BeerConsuptiom(Screen):
    entrada = StringProperty()

    def do_simulate(self, temp_max, chuva, fds):
        app = App.get_running_app()
        
        app.temp_max = temp_max
        app.chuva = chuva
        app.fds = fds

        df = pd.read_csv('../datasets/Consumo_cerveja.csv', sep=';')
        y = df['consumo']
        X = df[['temp_max','chuva','fds']]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2811)
        modelo = LinearRegression()
        modelo.fit(X_train,y_train)
        y_previsto = modelo.predict(X_test)
        
        entrada = X_test[0:1]
        entrada = [[float(temp_max), float(chuva), float(fds)]]
        
        self.entrada = str(modelo.predict(entrada)[0].round(2))
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
