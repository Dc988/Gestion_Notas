import flet as ft

# class TapContainer(ft.Tabs):
#     def __init__(self,**kwargs):
#         super().__init__(**kwargs)
#         self.selected_index=1
#         self.animation_duration=500
#         self.visable =True
#         self.expand=1
        

#     def add_Panel(self, text,target, icon=None):
#         self.tabs.append(
#             ft.Tab(
#                 text=text,
#                 icon=icon,
#                 content=target,
#             )
#         )
        
class TapContainer(ft.Row):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.expand=True

        self.column = ft.Column(expand=True, alignment="top",controls=[])
        self.panels=[]

        self.init_components()
    
    def init_components(self):

        
        self.rail = ft.NavigationRail(
                selected_index=0,
                group_alignment=-0.9,
                label_type=ft.NavigationRailLabelType.ALL,
                min_width=40,
                min_extended_width=400,
                destinations=[],
                trailing=ft.Column([],expand=True,alignment=ft.MainAxisAlignment.END),
                on_change=self.rail_changed)
        
        self.controls=[
            self.rail,
                ft.VerticalDivider(width=1),
                self.column,
        ]
    
    def add_rail_item(self,label, icon:ft.Icons, icon_selected:ft.Icons, destiny):
        self.rail.destinations.append(
            ft.NavigationRailDestination(
                icon=icon,
                padding=5,
                selected_icon=icon_selected,
                label=label
            )
        )
        if not self.column.controls:
            self.column.controls.append(destiny)
            self.column.update() if self.page else None

        self.panels.append(destiny)
        
    def add_leading(self, control):
        self.rail.trailing.controls.append(control)
        
    def rail_changed(self, e):
        index = e.control.selected_index
        self.column.controls.clear()
        self.column.controls.append(self.panels[index])

        self.column.update() if self.page else None