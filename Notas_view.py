import flet as ft
from Config_view import Config_view
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
        band = self.dataController.exportDataFrame()

        if(band):
            self.showAlertDialog("OK","Cambios Guardados Correctamente!", ft.Icons.THUMB_UP)

        else:
            self.showAlertDialog("Error!","no se pudo Guardar los Cambios", ft.Icons.ERROR)
        self.closeLoadingDialog()

        
    def setDataTable(self):
        self.showLoadingDialog()
        self.dataController = DataController(
            ruta=self.page.session.get("rutaArchivo")

        )

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


import flet as ft
import pandas as pd

def main(page: ft.Page):
    def setDisplay():
        def btnPage(e):
            page = e.control.data
            update_table(
                filter_text=filter_textfield.value, page_num=page
            )

        fin = (lenText // rows_per_page) + 1
        controls = [
            ft.ElevatedButton(
                "Anterior",
                on_click=lambda _: update_table(
                    filter_text=filter_textfield.value, page_num=max(1, current_page - 1)
                ))
        ]

        controls.extend([
           ft.ElevatedButton(
                num,
                data = num,
                on_click=btnPage,
                bgcolor= ft.colors.GREY if current_page == num else ft.colors.WHITE,
            ) for num in range(1,fin)
        ])

        controls.append(
            ft.ElevatedButton(
                "Siguiente",
                on_click=lambda _: update_table(
                    filter_text=filter_textfield.value, page_num=current_page + 1
                ),
            )
        )
    
        display.controls =controls
        display.update() if display.page else None

    # Configuración inicial de la página
    page.title = "Tabla con Filtro y Paginación"
    page.scroll = "adaptive"

    # DataFrame de ejemplo
    data = {
        "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Nombre": ["Ana", "Luis", "María", "Juan", "Sofía", "Pedro", "Lucía", "Carlos", "Elena", "Miguel"],
        "Edad": [23, 34, 29, 45, 31, 40, 25, 36, 27, 50],
    }
    df = pd.DataFrame(data)

    # Variables para paginación
    rows_per_page = 5
    current_page = 1
    lenText = len(df)
    # Función para actualizar la tabla con base en el filtro y la página
    def update_table(filter_text="", page_num=1):
        
        nonlocal current_page
        current_page = page_num

        filtered_df = df[df["Nombre"].str.contains(filter_text, case=False, na=False)]
        start = (page_num - 1) * rows_per_page
        end = start + rows_per_page

        # Crear filas para la tabla
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(row["ID"])),
                    ft.DataCell(ft.Text(row["Nombre"])),
                    ft.DataCell(ft.Text(row["Edad"])),
                ]
            )
            for _, row in filtered_df.iloc[start:end].iterrows()
        ]

        # Actualizar tabla y paginación
        table.rows = rows
        pagination_label.value = f"Página {current_page} de {max(1, (len(filtered_df) + rows_per_page - 1) // rows_per_page)}"
        page.update()
        setDisplay()

    # Elementos de la tabla
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Edad")),
        ],
        rows=[],
    )
    display=ft.Row(alignment=  ft.MainAxisAlignment.END,
            controls=[])
    
    # Campo de texto para el filtro
    filter_textfield = ft.TextField(
        hint_text="Filtrar por nombre",
        on_change=lambda e: update_table(filter_text=e.control.value, page_num=1),
    )

    # Elementos para la paginación
    pagination_label = ft.Text()
  

    # Disposición en la página
    page.add(
        filter_textfield,
        table,
        pagination_label,
        display,
    )
    page.theme_mode=ft.ThemeMode.LIGHT
    # Inicializar la tabla
    update_table()

# Ejecutar la aplicación
#ft.app(target=main)
 


