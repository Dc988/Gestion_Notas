
import flet as ft
from Config_view import Config_view
from Notas_view import Notas_view

class principal(ft.Column):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        p1 = Config_view(True)
        p2 = Notas_view(False)

        self.btn_panel1 = ft.ElevatedButton(text="Configuraciones", on_click=self.switch_panel,data=p1)
        self.btn_panel2 = ft.ElevatedButton(text="Panel 2", on_click=self.switch_panel,data=p2)
        self.text = ft.Text("Principal")

        self.controls=[ft.Row(controls=[self.btn_panel1,self.btn_panel2]),
                       p1,
                       p2]
        self.visable =True
    
    def add_btn_switch(self,text,target):
        pass
    
    def switch_panel(self,e):
        target = e.control.data
        for control in self.controls:
            if(isinstance(control,ft.Column)):
                control.visible = control==target
        self.update()


def main (page:ft.Page):
    page.add(principal())
    

print("ejecutando")
# Ejecuta la aplicación

ft.app(target=main)

print("finalizada")

