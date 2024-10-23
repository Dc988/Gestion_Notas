import flet as ft
class Notas_view(ft.Container):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        col = ft.Column()
        col.controls =[ft.Text("Non clickable")] 
        self.margin=10
        self.padding=10
        self.content=col
