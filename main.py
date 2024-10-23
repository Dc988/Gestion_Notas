
import flet as ft
from General import General
from Config_view import Config_view
from Notas_view import Notas_view

class principal(General):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.Data_panel_container()           
        
    
    def Data_panel_container(self):
        self.config_panel = Config_view()
        self.add_Panel("Configuraciones",self.config_panel,ft.icons.SETTINGS)

        self.nota_panel = Notas_view()
        self.add_Panel("Notas",self.nota_panel,ft.icons.NOTES)
    
    
def main (page:ft.Page):
    page.theme_mode=ft.ThemeMode.LIGHT
    page.title="Gestor de Notas Sena"
    page.add(principal())
    

print("ejecutando")
# Ejecuta la aplicación

ft.app(target=main)

print("finalizada")

