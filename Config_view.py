import flet as ft

class Config_view(ft.Column):
    def __init__(self,visable, **kwargs):
        super().__init__(**kwargs)
        self.controls=[ft.Text("Panel Config")]
        self.visible=visable