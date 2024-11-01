import flet as ft
from Config_view import Config_view
from layouts.PanelContainer import PanelContainer
from layouts.NotasFormContainer import Form
from layouts.NotasTableContainer import DataTable
from controllers.DataController import DataController

class Notas_view(PanelContainer):
    def __init__(self, page, **kwargs):
        super().__init__(**kwargs)
        self.page = page

        # Inicializar el controlador de datos y la tabla de datos una vez
        self.dataController = None
        self.tableData = DataTable(self.dataController)
        
        self.initialize_components()
        
        self.content.controls = [
            ft.Row(
             [
                ft.NavigationRail(
                    selected_index=0,
                    label_type=ft.NavigationRailLabelType.ALL,
                    # extended=True,
                    width=40,
                    min_extended_width=400,
                    leading=ft.Column([
                        ft.IconButton(
                            icon=ft.icons.UPDATE,
                            on_click=lambda _: self.setDataTable()
                            )]),
                    group_alignment=-0.9,
                    destinations=[ft.NavigationRailDestination(disabled=True)]
                ),
                ft.VerticalDivider(width=1),
                ft.Column([self.fr,self.tableData], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            expand=True
            )
        ]
        self.setDataTable()

    def initialize_components(self):
        self.config_panel = Config_view(self.page)
        self.fr = Form()
        col = ft.Column(expand=True)
        self.content = col


    def setDataTable(self):
        # Configura el DataController con los valores actuales
        self.dataController = DataController(
            ruta=self.config_panel.txt_ruta_archivo.value,
            extencion=self.config_panel.txt_extencion.value
        )

        # Verifica si se han configurado correctamente los valores de ruta y extensión
        if self.config_panel.getRuta() != "" or self.config_panel.getExtencion() != "":
            if not self.dataController.read_file():
                self.tableData.clearData()
                self.showAlertDialog("Error!! Panel Notas", "No se pudo cargar la información", ft.icons.ERROR)
            else:
                # Actualiza el DataTable existente en lugar de crear uno nuevo
                self.tableData.dataController = self.dataController
                self.tableData.setDataTable()
                self.showAlertDialog("Mensaje!! Panel Notas", "Información cargada correctamente", ft.icons.THUMB_UP)


