import flet as ft

class General(ft.Tabs):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.selected_index=1
        self.animation_duration=1000
        self.visable =True
        self.expand=1
        
    def add_Panel(self, text,target, icon=None):
        self.tabs.append(
            ft.Tab(
                text=text,
                icon=icon,
                content=target,
            )
        )
        

   