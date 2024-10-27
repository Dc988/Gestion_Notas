import flet as ft
from controllers.ConfigController import ConfigController
from layouts.PanelContainer import PanelContainer
import os

class Config_view(PanelContainer):
    _instance = None

    def __init__( self, page,**kwargs):
        super().__init__(**kwargs)
        self.page = page
        
        self.initialize_components()     
        
        self.col.controls=[
            self.pick_file_dialogArchivo,
            self.pick_file_dialogCarpeta,
            
            ft.CupertinoListTile(
                
                leading=ft.Icon(name=ft.icons.ATTACH_FILE),
                title=ft.Text("Ruta Archivo Información"),                
                subtitle=self.txt_ruta_archivo,
                trailing=ft.IconButton(
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=lambda _: self.pick_file_dialogArchivo.pick_files(
                                allow_multiple=False,allowed_extensions=["xlsx","csv"]
                            ),
                        )),
                    
            ft.CupertinoListTile(
                leading=ft.Icon(name=ft.icons.FILE_COPY_ROUNDED),
                title=ft.Text("Tipo de documento"),                
                subtitle=self.txt_extencion),
            
            ft.CupertinoListTile(
                leading=ft.Icon(name=ft.icons.DRIVE_FILE_MOVE_SHARP),
                title=ft.Text("Ruta Carpeta Evidencias"),                
                subtitle=self.txt_ruta_carpeta,
                trailing=ft.IconButton(
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=lambda _: self.pick_file_dialogCarpeta.get_directory_path(),
                        )),
        
            ft.Row([
                ft.ElevatedButton(
                        "GUARDAR CAMBIOS",
                        icon=ft.icons.SAVE,
                        on_click=self.save_data,
                    )])
            
            ]
               

    def initialize_components(self):
        self.configController = ConfigController()
        
        self.col = ft.Column()
        
        self.txt_ruta_archivo = ft.Text(value="alue",size=15)
        self.txt_extencion = ft.Text(value="alue",size=15)
                
        self.txt_ruta_carpeta = ft.Text(value="alue",size=15)
        
        
        self.pick_file_dialogArchivo = ft.FilePicker(on_result=self.pick_file_result)
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
            "extension": self.txt_extencion.value
            }
            data = self.configController.edit_json(data)

            
            self.showAlertDialog(
                title="Mensaje!", 
                content="Datos Guardados Correctamente!", 
                icon=ft.icons.CHECK) if data else self.showAlertDialog(
                title="Error!", 
                content="No se pudo guardar la informacion!", 
                icon=ft.icons.ERROR)

        if (self.txt_ruta_archivo.value == "") or (self.txt_ruta_carpeta.value == ""):
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

            self.txt_ruta_archivo.value=data.get("rutaArchivo")
            self.txt_ruta_carpeta.value=data.get("RutaOrigen")
            self.txt_extencion.value=data.get("extension")
            
        else:
            try:
                self.showAlertDialog("Error! Panel Configuraciones","No se pudo cargar información del archivo!",ft.icons.ERROR)
            except Exception as ex:
               pass
            
    def pick_file_result(self,e: ft.FilePickerResultEvent):
        self.txt_ruta_archivo.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else self.txt_ruta_archivo.value
        )

        nombre, extension = os.path.splitext(self.txt_ruta_archivo.value)

        self.txt_extencion.value = extension
        
        self.txt_extencion.update()
        self.txt_ruta_archivo.update()
    
    def get_directory_result(self,e: ft.FilePickerResultEvent):
        self.txt_ruta_carpeta.value = e.path if e.path else self.txt_ruta_carpeta.value
        self.txt_ruta_carpeta.update()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config_view, cls).__new__(cls)
        return cls._instance
