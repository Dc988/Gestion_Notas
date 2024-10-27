import flet as ft
from Config_view import Config_view
from layouts.PanelContainer import PanelContainer

class Notas_view(PanelContainer):
    def __init__(self, page,**kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.initialize_components()

               
    def initialize_components(self):
        self.config_panel = Config_view(self.page)

        self.margin = 10
        self.padding = 10

        col = ft.Column()

        self.content = col
        
        self.content.controls = [
            ft.ElevatedButton("Mostrar diálogo", on_click=self.prueba)
        ]
        
        
         

    def prueba(self,e):
        self.showOptionDialog(
            title="Upps!",
            
            YesOption=self.yes,
            icon=ft.icons.INFO)
        
    def yes(self):
        
        self.showAlertDialog("Prueba 2",self.config_panel.txt_ruta_archivo.value)
        
