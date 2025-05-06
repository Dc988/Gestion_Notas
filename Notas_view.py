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
                            on_click=lambda _: self.showOptionDialog("Desea actualizar los datos?",self.setDataTable,icon=ft.Icons.INFO)
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

        if self.page.session.get("visibleColumns") != [] and self.page.session.get("RutaOrigen") != "" :

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
"""
import flet as ft
import fitz  # PyMuPDF

# Función para buscar y extraer texto relacionado con el código
def extraer_evidencia(pdf_path, codigo):
    doc = fitz.open(pdf_path)
    pages =False
    textValue = []

    for page in doc:
        texto = page.get_text()
        encontrado = False
        if codigo in texto:
            
            for line in texto.splitlines() :
                
                if codigo in line:
                    encontrado = True

                if encontrado:
                    if "Para hacer el envío de la evidencia" in line.strip():
                        pages = True
                        break
                    textValue.append(line)
        if pages:
            break

    resultado =  "\n".join(textValue)        
    return resultado if resultado else "Evidencia no encontrada."

def main(page: ft.Page):
    page.theme_mode=ft.ThemeMode.LIGHT
    page.title = "Buscador de Evidencias"
    codigo_input = ft.TextField(label="Código de Evidencia", width=400)
    resultado_output = ft.Text(value="", expand=True)
    page.scroll = ft.ScrollMode.AUTO
    def buscar_click(e):
        codigo = codigo_input.value.strip()
        if codigo:
            resultado = extraer_evidencia("G:/Mi unidad/1. Documentos/1. CURSOS/2. ANALISIS Y DESARROLLO DE SOFTWARE. (2898288)/02. PROYECTO/03. EJECUCIÓN/P6/Guia_aprendizaje.pdf", codigo)
            resultado_output.value = resultado
            page.update()

    page.add(
        ft.Column([
            codigo_input,
            ft.ElevatedButton("Buscar", on_click=buscar_click),
            resultado_output
        ])
    )

ft.app(target=main)

#"""
