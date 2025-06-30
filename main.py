
import flet as ft
from layouts.TapContainer import TapContainer

from Config_view import Config_view
from Notas_view import Notas_view

# class principal(TapContainer):

#     def __init__(self,**kwargs):
#         super().__init__(**kwargs)
#         self.page = None
        
#     def setPage(self,page):
#         self.page = page

#     def Data_panel_container(self):
        
#         self.config_panel = Config_view(self.page)
#         self.add_Panel(
#             text="Configuraciones",
#             target=self.config_panel,
#             icon=ft.Icons.SETTINGS)
        
#         self.nota_panel = Notas_view(self.page)
#         self.add_Panel(
#             text="Notas",
#             target=self.nota_panel,
#             icon=ft.Icons.NOTES)

def main(page:ft.Page):
    page.window.maximized = True
    page.theme_mode=ft.ThemeMode.LIGHT
    page.title="Gestor de Notas Sena"

    mainContainer = TapContainer()


    config_panel = Config_view(page)
    nota_panel = Notas_view(page)

    mainContainer.add_rail_item(
        "INICIO",
        ft.Icons.HOME_OUTLINED,
        ft.Icons.HOME,
        nota_panel
    )
    
    mainContainer.add_rail_item(
        "CONFIG",
        ft.Icons.SETTINGS_OUTLINED,
        ft.Icons.SETTINGS,
        config_panel
    )

    for btn in nota_panel.getBtnOptions():
        mainContainer.add_leading(btn)

    page.add(mainContainer)
    

print("ejecutando")
ft.app(target=main)
#prin.nota_panel.exportData()
print("finalizada")
# import flet as ft

# from layouts.TapContainer import TapContainer
    

# def main(page: ft.Page):
#     page.title = "Ejemplo NavigationRail"
#     page.horizontal_alignment = "center"
#     page.theme_mode=ft.ThemeMode.LIGHT

#     pageContent = TapContainer()

#     panel_1= ft.Row(vertical_alignment=ft.CrossAxisAlignment.START,expand=True, controls=[ft.Text("Panel_1", size=30, weight="bold")])
#     pageContent.add_rail_item("panel_1",ft.Icons.H_MOBILEDATA,ft.Icons.H_MOBILEDATA_OUTLINED,panel_1)

#     panel_2= ft.Row(vertical_alignment=ft.CrossAxisAlignment.START,expand=True, controls=[ft.Text("Panel_2", size=30, weight="bold")])
#     pageContent.add_rail_item("panel_2",ft.Icons.HOME,ft.Icons.HOME_FILLED,panel_2)

#     panel_3= ft.Row(vertical_alignment=ft.CrossAxisAlignment.START,expand=True, controls=[ft.Text("Panel_3", size=30, weight="bold")])
#     pageContent.add_rail_item("panel_3",ft.Icons.ACCESS_ALARM,ft.Icons.ACCESS_ALARM_OUTLINED,panel_3)

#     pageContent.add_leading(ft.FloatingActionButton(
#                             icon=ft.Icons.UPDATE,
#                             on_click=lambda _: print("click btn")
#                             ))
#     page.add(pageContent)

# ft.app(target=main)

