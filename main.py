
import flet as ft
from General import General
from Config_view import Config_view
from Notas_view import Notas_view

class principal(General):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.Data_panel_container()
        self.Data_panel_menu()

        
        self.visable =True

    def Data_panel_menu(self):
        self.add_btn_switch("Configuraciones",self.config_panel)
        self.add_btn_switch("Notas",self.nota_panel)
    
    def Data_panel_container(self):
        self.config_panel = Config_view(True)
        self.add_Panel(self.config_panel)

        self.nota_panel = Notas_view(False)
        self.add_Panel(self.nota_panel)
    
    


def main (page:ft.Page):
    page.add(principal())
    

print("ejecutando")
# Ejecuta la aplicación

ft.app(target=main)

print("finalizada")

