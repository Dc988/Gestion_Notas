import flet as ft
from layouts.PanelContainer import PanelContainer
from layouts.Notas.NotasFormContainer import Form
from layouts.Notas.NotasTableContainer import DataTable
from controllers.DataController import DataController

class Notas_view(PanelContainer):
    def __init__(self, page, **kwargs):
        super().__init__(**kwargs)
        self.page = page

        # Inicializar el controlador de datos y la tabla de datos una vez
        
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
                            icon=ft.Icons.UPDATE,
                            on_click=lambda _: self.setDataTable()
                            ),
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            on_click=lambda _: self.showInfoEviModal()
                        ),
                        ft.IconButton(
                            icon=ft.Icons.SAVE,
                            on_click=lambda _: self.showOptionDialog("Desea guardar los cambios?",self.exportData,icon=ft.Icons.INFO)
                        )]),
                    group_alignment=-0.9,
                    destinations=[ft.NavigationRailDestination(disabled=True)]
                ),
                ft.VerticalDivider(width=1),
                ft.Column([
                    self.tableData
                           ], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            expand=True
            )
        ]
        self.setDataTable()

    def initialize_components(self):
        self.dataController = None
        self.tableData = DataTable(self.page,self.dataController)
        self.fr = Form(self.page,self.dataController,self.tableData)

        self.tableData.setForm(self.fr)

        col = ft.Column(expand=True)
        self.content = col

    def showInfoEviModal(self):
        self.fr.clear_data() 
        self.fr.showModalDialog()

    def exportData(self):
        self.showLoadingDialog()
        band = self.dataController.saveDataFile()

        if(band):
            self.showAlertDialog("OK","Cambios Guardados Correctamente!", ft.Icons.THUMB_UP)

        else:
            self.showAlertDialog("Error!","no se pudo Guardar los Cambios", ft.Icons.ERROR)
        self.closeLoadingDialog()

        
    def setDataTable(self):
        self.showLoadingDialog()
        self.dataController = DataController()

        if self.page.session.get("rutaArchivo") != "" and self.page.session.get("visibleColumns") != [] and self.page.session.get("RutaOrigen") != "" :

            if not self.dataController.read_file():
                self.tableData.clearData()
                self.showAlertDialog("Error!! Panel Notas", "No se pudo cargar la información", ft.Icons.ERROR)
            else:
                # Actualiza el DataTable existente en lugar de crear uno nuevo
                self.tableData.dataController = self.dataController
                self.fr.dataController = self.dataController
                self.tableData.setDataTable()
                self.showAlertDialog("Mensaje!! Panel Notas", "Información cargada correctamente", ft.Icons.THUMB_UP)
        else:
            self.showAlertDialog("Error!! Panel Notas", "actualice panel de configuraciones", ft.Icons.ERROR)
        self.closeLoadingDialog()
#"""
import flet as ft
from layouts.Notas.FilterTable_2 import FilterTable_view

def main(page: ft.Page):
    filter = {
        "f1":{
                'CODIGO ACTIVIDAD': {'VALUES': ['12'], 'TYPE': 'IGUAL A'}, 
                'EVIDENCIA': {'VALUES': ['12'], 'TYPE': 'IGUAL A'}
            },
        "f2":{
                'CODIGO ACTIVIDAD': {'VALUES': ['12'], 'TYPE': 'IGUAL A'}, 
                'EVIDENCIA': {'VALUES': ['12'], 'TYPE': 'IGUAL A'}
            }
    }

    
    page.theme_mode = ft.ThemeMode.LIGHT  # Modo por defecto
    filter_view = FilterTable_view(page,onYes=None)
    #filter_view.setFilterPred(filter)
    switch = ft.IconButton(
                        icon=ft.Icons.FILTER_ALT_SHARP,
                        on_click=lambda _: filter_view.showModalDialog()
                    )
    page.add(
        switch
        )
    
ft.app(target=main)#"""


