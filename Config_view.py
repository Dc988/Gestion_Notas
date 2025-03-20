import flet as ft
from controllers.ConfigController import ConfigController
from layouts.PanelContainer import PanelContainer
from DragAndDrop import editDataframe_view
from controllers.DataController import DataController
import pandas as pd


class Config_view(PanelContainer):
    _instance = None

    def __init__( self, page,**kwargs):
        super().__init__(**kwargs)
        self.page = page
        
        self.initialize_components()     
        
        self.col.controls=[
            self.pick_file_dialogArchivo,
            self.save_file_dialogArchivo,
            self.pick_file_dialogCarpeta,
            ft.Row(controls=[
                ft.ElevatedButton(text="Importar",on_click=lambda _:self.pick_file_dialogArchivo.pick_files(
                                    allow_multiple=False,allowed_extensions=["xlsx"]
                                )),
                ft.ElevatedButton(text="Exportar",on_click=lambda _:self.save_file_dialogArchivo.save_file(file_name="Seguimiento de notas.xlsx",allowed_extensions=["xlsx"]))
            ],alignment=ft.MainAxisAlignment.END),
                     
            self.component_container(expand=False,name="Columnas Visibles",control=self.txt_cols_visible,icon=ft.Icons.FILE_COPY_ROUNDED,trailing=ft.IconButton(
                                                    icon=ft.Icons.ADD,
                                                    on_click=lambda _:self.editColModal.showModalDialog()
                                                    
                                                )),
            self.component_container(expand=False,name="Ruta Carpeta Evidencias",control=self.txt_ruta_carpeta,trailing=ft.IconButton(
                            icon=ft.Icons.ADD,
                            on_click=lambda _: self.pick_file_dialogCarpeta.get_directory_path(),
                        ),icon=ft.Icons.DRIVE_FILE_MOVE_SHARP),            
                       
            ft.Row([
                ft.ElevatedButton(
                        "GUARDAR CAMBIOS",
                        icon=ft.Icons.SAVE,
                        on_click=self.save_data
                    )],alignment="end")
            
            ]
            
         
    def initialize_components(self):
        self.pick_file_dialogArchivo = ft.FilePicker(on_result=self.pick_file_result)
        self.save_file_dialogArchivo = ft.FilePicker(on_result=self.save_file_result)
        ft.FilePicker()
        self.configController = ConfigController()
        self.editColModal = None
        self.col = ft.Column()
        
        self.txt_cols_visible = ft.Text(value="",size=15)
                
        self.txt_ruta_carpeta = ft.Text(value="",size=15)
        
        self.pick_file_dialogCarpeta = ft.FilePicker(on_result=self.get_directory_result)

        self.col.spacing=20
        self.margin=10
        self.content=self.col
        self.set_Data()
        


    def save_data(self,e):
        def yesAction():
            
            data = {
            "RutaOrigen":self.txt_ruta_carpeta.value,
            "visibleColumns":self.editColModal.selectedCols
            }
            data = self.configController.edit_json(data)

            
            self.showAlertDialog(
                title="Mensaje!", 
                content="Datos Guardados Correctamente!", 
                icon=ft.Icons.CHECK) if data else self.showAlertDialog(
                title="Error!", 
                content="No se pudo guardar la informacion!", 
                icon=ft.Icons.ERROR)
            self.set_Data()
            

        if (self.txt_ruta_carpeta.value == "") or (not self.editColModal.selectedCols):
            self.showAlertDialog(
                title="Error!", 
                content="No se permiten campos en blanco!", 
                icon=ft.Icons.ERROR)
        else:
            self.showOptionDialog(
                    title="Deseas Guardar esta información?", 
                    icon=ft.Icons.QUESTION_MARK,
                    YesOption=yesAction)
            
    def set_Data(self):
        data = self.configController.read_document()
        
        if(data):
            self.editColModal = editDataframe_view(self.page, onYes=self.setDataColumn)
            
            self.txt_ruta_carpeta.value=data.get("RutaOrigen")
            self.txt_cols_visible.value= ", ".join(data.get("visibleColumns"))
            
            self.page.session.set("FilterPred",data.get("FilterPred"))
            self.page.session.set("rutaArchivo",data.get("rutaArchivo"))
            self.page.session.set("RutaOrigen",data.get("RutaOrigen"))
            self.page.session.set("visibleColumns",data.get("visibleColumns"))
            self.page.session.set("col_oblig",data.get("col_oblig"))
            self.editColModal.setData(data.get("visibleColumns"))

        else:
            self.editColModal = editDataframe_view(self.page, onYes=self.setDataColumn)
            self.showAlertDialog("Error! Panel Configuraciones","No se pudo cargar información del archivo!",ft.Icons.ERROR)
            
    def setDataColumn(self):
        
        self.txt_cols_visible.value= ", ".join(self.editColModal.selectedCols)
        self.txt_cols_visible.update()
      

    
    def get_directory_result(self,e: ft.FilePickerResultEvent):
        self.txt_ruta_carpeta.value = e.path if e.path else self.txt_ruta_carpeta.value
        self.txt_ruta_carpeta.update()
    
    def getRutaCarpeta(self):
        return self.txt_ruta_carpeta.value
    
    def save_file_result(self,e: ft.FilePickerResultEvent):
        def save():
            self.showLoadingDialog()
            temp = DataController()
            band = temp.exportDataFrame(e.path)
            data = {
                "title":"Accion exitosa" if band else "Ocurrio un error!",
                "content":"Datos importados" if band else "No se pudo importar la informacion",
                "icon": ft.Icons.THUMB_UP if band else ft.Icons.ERROR
            }

            self.showAlertDialog(**data)
        
        self.showOptionDialog("Desea exportar la informacion?",YesOption=save,icon=ft.Icons.INFO_ROUNDED) if e.path is not None else None

            

    def pick_file_result(self,e: ft.FilePickerResultEvent):
        def save():
            self.showLoadingDialog()
            temp = DataController()
            band = temp.importDataFrame(ruta)
            data = {
                "title":"Accion exitosa" if band else "Ocurrio un error!",
                "content":"Datos importados" if band else "No se pudo importar la informacion",
                "icon": ft.Icons.THUMB_UP if band else ft.Icons.ERROR
            }

            self.showAlertDialog(**data)
            
        try:
            if e.files:
                self.showLoadingDialog()
                ruta = (
                    ", ".join(map(lambda f: f.path, e.files)) if e.files else ""
                )
                col = self.page.session.get("col_oblig")
                dt = pd.read_excel(ruta,dtype=str,header=0)
                dt = dt[col]

                self.showOptionDialog("Desea importar la informacion?",YesOption=save,icon=ft.Icons.INFO_ROUNDED) 
        except Exception as ex:
            self.showAlertDialog("Error","No se pudo importar el archivo!",ft.Icons.ERROR)
            print(ex)



    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config_view, cls).__new__(cls)
        return cls._instance
