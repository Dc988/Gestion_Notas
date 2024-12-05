import flet as ft
from controllers.ConfigController import ConfigController
from layouts.PanelContainer import PanelContainer
from DragAndDrop import editDataframe_view
import os

class Config_view(PanelContainer):
    _instance = None

    def __init__( self, page,**kwargs):
        super().__init__(**kwargs)
        self.page = page
        
        self.initialize_components()     
        
        self.col.controls=[
            #self.pick_file_dialogArchivo,
            self.pick_file_dialogCarpeta,
            self.component_container(expand=False,name="Ruta Archivo Información",
                                     control=self.txt_ruta_archivo,
                                    icon =ft.icons.DRIVE_FILE_MOVE_SHARP,
                                     trailing=ft.IconButton(
                                                    icon=ft.icons.ADD,
                                                    on_click=lambda _:self.editColModal.showModalDialog()
                                                    #lambda _: self.pick_file_dialogArchivo.pick_files(
                                                    #    allow_multiple=False,allowed_extensions=["xlsx"]
                                                    #)
                                                )),
                     
            self.component_container(expand=False,name="Columnas Visibles",control=self.txt_cols_visible,trailing=None,icon=ft.icons.FILE_COPY_ROUNDED),
            self.component_container(expand=False,name="Ruta Carpeta Evidencias",control=self.txt_ruta_carpeta,trailing=ft.IconButton(
                            icon=ft.icons.ADD,
                            on_click=lambda _: self.pick_file_dialogCarpeta.get_directory_path(),
                        ),icon=ft.icons.DRIVE_FILE_MOVE_SHARP),            
                       
            ft.Row([
                ft.ElevatedButton(
                        "GUARDAR CAMBIOS",
                        icon=ft.icons.SAVE,
                        on_click=self.save_data
                    )],alignment="end")
            
            ]
               
    def clear(self,e):
         self.txt_ruta_archivo.value = ""
         self.txt_ruta_archivo.update()
         
    def initialize_components(self):
        self.configController = ConfigController()
        self.editColModal = None
        self.col = ft.Column()
        
        self.txt_ruta_archivo = ft.Text(value="alue",size=15)
        self.txt_cols_visible = ft.Text(value="alue",size=15)
                
        self.txt_ruta_carpeta = ft.Text(value="alue",size=15)
        
        self.pick_file_dialogCarpeta = ft.FilePicker(on_result=self.get_directory_result)

        self.col.spacing=20
        self.margin=10
        self.content=self.col
        self.set_Data()
        


    def save_data(self,e):
        def yesAction():
            data = {
            "rutaArchivo":self.txt_ruta_archivo.value,
            "RutaOrigen":self.txt_ruta_carpeta.value,
            "visibleColumns":self.editColModal.selectedCols
            }
            data = self.configController.edit_json(data)

            
            self.showAlertDialog(
                title="Mensaje!", 
                content="Datos Guardados Correctamente!", 
                icon=ft.icons.CHECK) if data else self.showAlertDialog(
                title="Error!", 
                content="No se pudo guardar la informacion!", 
                icon=ft.icons.ERROR)
            self.set_Data()
            

        if (self.txt_ruta_archivo.value == "") or (self.txt_ruta_carpeta.value == "") or (not self.editColModal.selectedCols):
            self.showAlertDialog(
                title="Error!", 
                content="No se permiten campos en blanco!", 
                icon=ft.icons.ERROR)
        else:
            self.showOptionDialog(
                    title="Deseas Guardar esta informació?", 
                    icon=ft.icons.QUESTION_MARK,
                    YesOption=yesAction)
            
    def set_Data(self):
        data = self.configController.read_document()
        
        if(data):
            self.editColModal = editDataframe_view(self.page,data.get("rutaArchivo"), onYes=self.setDataColumn)
            self.txt_ruta_archivo.value=data.get("rutaArchivo")
            self.txt_ruta_carpeta.value=data.get("RutaOrigen")
            self.txt_cols_visible.value= ", ".join(data.get("visibleColumns"))
            self.editColModal.setData(data.get("visibleColumns"))
            
            self.page.session.set("rutaArchivo",data.get("rutaArchivo"))
            self.page.session.set("RutaOrigen",data.get("RutaOrigen"))
            self.page.session.set("visibleColumns",data.get("visibleColumns"))
        else:
            self.editColModal = editDataframe_view(self.page, onYes=self.setDataColumn)
            self.showAlertDialog("Error! Panel Configuraciones","No se pudo cargar información del archivo!",ft.icons.ERROR)
            
    def setDataColumn(self):
        self.txt_ruta_archivo.value = self.editColModal.ruta
        self.txt_cols_visible.value= ", ".join(self.editColModal.selectedCols)
        self.txt_ruta_archivo.update()
        self.txt_cols_visible.update()
      

    
    def get_directory_result(self,e: ft.FilePickerResultEvent):
        self.txt_ruta_carpeta.value = e.path if e.path else self.txt_ruta_carpeta.value
        self.txt_ruta_carpeta.update()
    
    def getRuta(self):
        return self.txt_ruta_archivo.value
    
    
    def getRutaCarpeta(self):
        return self.txt_ruta_carpeta.value
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config_view, cls).__new__(cls)
        return cls._instance
