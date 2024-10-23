import flet as ft
from controllers.ConfigController import ConfigController

class Config_view(ft.Container):
    def __init__( self,**kwargs):
        super().__init__(**kwargs)
        self.initialize_components()     
        
        self.col.controls=[
            self.pick_file_dialogArchivo,
            self.pick_file_dialogCarpeta,
            ft.Row([
                    self.txt_ruta_archivo,
                    ft.IconButton(
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=lambda _: self.pick_file_dialogArchivo.pick_files(
                                allow_multiple=False,allowed_extensions=["xlsx","csv"]
                            ),
                        )
                ]),
            ft.Row([
                    self.txt_ruta_carpeta,
                    ft.IconButton(
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=lambda _: self.pick_file_dialogCarpeta.pick_files(
                                allow_multiple=False,allowed_extensions=["xlsx"]
                            ),
                        )
                ]),
            ft.Row([ft.ElevatedButton(
                        "GUARDAR CAMBIOS",
                        icon=ft.icons.SAVE,
                        on_click=self.save_data,
                    )])
            ]
        self.col.spacing=20
        self.margin=10
        self.content=self.col
        self.set_Data()

    def initialize_components(self):
        self.configController = ConfigController()
        self.ConfigController = ConfigController()
        self.col = ft.Column()
        self.txt_ruta_archivo = ft.TextField(value="",read_only=True, label="Ruta Archivo Información", width=800, text_size=12)
        self.txt_ruta_carpeta = ft.TextField(value="",read_only=False, label="Ruta Carpeta Evidencias", width=800, text_size=12)
        self.pick_file_dialogArchivo = ft.FilePicker(on_result=self.pick_file_result)
        self.pick_file_dialogCarpeta = ft.FilePicker(on_result=self.pick_directory_result)
        


    def save_data(self,e):
        data = {
            "rutaArchivo":self.txt_ruta_archivo.value,
            "RutaOrigen":self.txt_ruta_carpeta.value
        }
        data = self.configController.edit_json(data)
        
    
    def set_Data(self):
        data = self.configController.read_document()

        if(data):
            self.txt_ruta_archivo.value=data.get("rutaArchivo")
            self.txt_ruta_carpeta.value=data.get("RutaOrigen")
            
    def pick_file_result(self,e: ft.FilePickerResultEvent):
        self.txt_ruta_archivo.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else ""
        )

        self.txt_ruta_archivo.update()
    
    def pick_directory_result(self,e: ft.FilePickerResultEvent):
        self.txt_ruta_carpeta.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else ""
        )

        self.txt_ruta_carpeta.update()



