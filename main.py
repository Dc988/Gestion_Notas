
import flet as ft
from layouts.TapContainer import TapContainer

from Config_view import Config_view
from Notas_view import Notas_view

class principal(TapContainer):

    def __init__(self,page,**kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.Data_panel_container()
       
    def Data_panel_container(self):
        
        config_panel = Config_view(self.page)
        self.add_Panel(
            text="Configuraciones",
            target=config_panel,
            icon=ft.icons.SETTINGS)

        nota_panel = Notas_view(self.page)
        self.add_Panel(
            text="Notas",
            target=nota_panel,
            icon=ft.icons.NOTES)
        
    
def main (page:ft.Page):
    page.window.maximized = True
    page.window.resizable=False
    page.window.maximizable=False
    page.window.minimizable=False

    page.theme_mode=ft.ThemeMode.LIGHT
    page.title="Gestor de Notas Sena"
    
    page.add(principal(page))
    

print("ejecutando")
ft.app(target=main)
print("finalizada")

