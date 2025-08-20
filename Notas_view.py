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
            ft.Column([
                    self.tableData
                           ], alignment=ft.MainAxisAlignment.START, expand=True)
        ]
        self.setDataTable()

    def initialize_components(self):
        self.dataController = None
        self.tableData = DataTable(self.page,self.dataController)
        self.fr = Form(self.page,self.dataController,self.tableData)

        self.tableData.setForm(self.fr)

        col = ft.Column(expand=True)
        self.content = col

    def getBtnOptions(self):
        return [
                ft.ElevatedButton(
                    content=ft.Icon(ft.Icons.UPDATE),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),  # Bordes redondeados
                        padding=20,  # Espaciado interno para que el ícono tenga espacio
                    ),
                    tooltip=ft.Tooltip('ACTUALIZAR TABLA'),
                    # bgcolor='#f0f0f0',
                    on_click=lambda _: self.showOptionDialog("Desea actualizar los datos?",self.setDataTable,icon=ft.Icons.INFO)
                    ),
                ft.ElevatedButton(
                    content=ft.Icon(ft.Icons.ADD),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),  # Bordes redondeados
                        padding=20,  # Espaciado interno para que el ícono tenga espacio
                    ),
                    tooltip=ft.Tooltip('FORMULARIO DE REGISTRO'),
                    # bgcolor='#f0f0f0',
                    on_click=lambda _: self.showInfoEviModal()
                ),
                # ft.ElevatedButton(
                #     content=ft.Icon(ft.Icons.SAVE),
                #     style=ft.ButtonStyle(
                #         shape=ft.RoundedRectangleBorder(radius=8),  # Bordes redondeados
                #         padding=20,  # Espaciado interno para que el ícono tenga espacio
                #     ),
                #     tooltip=ft.Tooltip('GUARDAR CAMBIOS'),
                #     # bgcolor='#f0f0f0',
                #     on_click=lambda _: self.showOptionDialog("Desea guardar los cambios?",self.exportData,icon=ft.Icons.INFO)
                # )
                ]
    
    def showInfoEviModal(self):
        self.fr.clear_data() 
        self.fr.showModalDialog()

    def exportData(self):
        self.showLoadingDialog()
        band = True#self.dataController.saveDataFile()

        if(band):
            self.showAlertDialog("OK","Cambios Guardados Correctamente!", ft.Icons.THUMB_UP)

        else:
            self.showAlertDialog("Error!","no se pudo Guardar los Cambios", ft.Icons.ERROR)
        self.closeLoadingDialog()

        
    def setDataTable(self):
        self.showLoadingDialog()
        self.dataController = DataController(self.page)

        if self.page.session.get("visibleColumns") != [] and self.page.session.get("RutaOrigen") != "" :
            # Actualiza el DataTable existente en lugar de crear uno nuevo
            self.tableData.dataController = self.dataController
            self.fr.dataController = self.dataController
            self.tableData.setDataTable()
            self.showAlertDialog("Mensaje!! Panel Notas", "Información cargada correctamente", ft.Icons.THUMB_UP)
        else:
            self.showAlertDialog("Error!! Panel Notas", "actualice panel de configuraciones", ft.Icons.ERROR)
        self.closeLoadingDialog()


            
    

