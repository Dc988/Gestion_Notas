import flet as ft

class General(ft.Column):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.panel_menu = ft.Row()
        self.panel_container =ft.Row()

        self.controls=[self.panel_menu,self.panel_container]
    
    def add_btn_switch(self,text,target):
        btn = ft.ElevatedButton(text=text, on_click=self.switch_panel,data=target)
        self.panel_menu.controls.append(btn)
    
    def add_Panel(self, panel):
        self.panel_container.controls.append(panel)

    def switch_panel(self,e):
        target = e.control.data

        for control in self.panel_container.controls:
            if(isinstance(control,ft.Column)):
                control.visible = control==target
        self.update()