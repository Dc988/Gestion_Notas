import flet as ft
class Notas_view(ft.Column):
    def __init__(self,visable, **kwargs):
        super().__init__(**kwargs)
        self.controls=[ft.Text("Panel Notas")]
        self.visible=visable