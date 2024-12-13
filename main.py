
import flet as ft
from layouts.TapContainer import TapContainer

from Config_view import Config_view
from Notas_view import Notas_view

class principal(TapContainer):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.page = None
        
    
    def setPage(self,page):
        self.page = page


    def Data_panel_container(self):
        
        self.config_panel = Config_view(self.page)
        self.add_Panel(
            text="Configuraciones",
            target=self.config_panel,
            icon=ft.Icons.SETTINGS)

        self.nota_panel = Notas_view(self.page)
        self.add_Panel(
            text="Notas",
            target=self.nota_panel,
            icon=ft.Icons.NOTES)
        

def main(page:ft.Page):
  
    page.window.maximized = True
    page.theme_mode=ft.ThemeMode.LIGHT
    page.title="Gestor de Notas Sena"
    prin.setPage(page)
    prin.Data_panel_container()

    page.add(prin)
    

prin = principal()

print("ejecutando")
ft.app(target=main)
prin.nota_panel.exportData()
print("finalizada")

