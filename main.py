
import flet as ft
from layouts.TapContainer import TapContainer

from Config_view import Config_view
from Notas_view import Notas_view

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
