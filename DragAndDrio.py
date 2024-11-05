import os
import flet as ft
from layouts.PanelContainer import PanelContainer
class editDataframe_view(PanelContainer):

    def __init__(self, page, **kwargs):
        super().__init__(**kwargs)
        self.page = page

        self.initialize_components()
        self.content = ft.Column([ft.ElevatedButton("abrir",on_click= lambda _: self.showModalDialog())])
        
    def initialize_components(self):
        columns = [1,2,3,4,5,6]
        self.txt_ruta_archivo = ft.Text(value="alue",size=15)
        self.pick_file_dialogArchivo = ft.FilePicker(on_result=self.pick_file_result)

        p2 = self.getContainer(
            title="Columas Originales",
            controls=[self.add_dragtarget_item(item) for index,item in enumerate(columns)]
            )
        
        p1 =self.getContainer(
                title="Columas Visibles",
                controls=[self.add_draggle_item(index,item) for index,item in enumerate(columns)]
        )

        col = ft.Column(
            controls=[
                self.pick_file_dialogArchivo,
                self.component_container(
                    expand=False,
                    name="Ruta Archivo Información",
                    control=self.txt_ruta_archivo,
                    icon =ft.icons.DRIVE_FILE_MOVE_SHARP,
                    trailing=ft.IconButton(
                                icon=ft.icons.ADD,
                                on_click=lambda _: self.pick_file_dialogArchivo.pick_files(
                                    allow_multiple=False,allowed_extensions=["xlsx"]
                                ),
                            )
                ),
                self.component_container(
                    expand=False,
                    name="Columnas del Archivo",
                    icon =ft.icons.GRID_3X3,
                    control=ft.Row(
                        controls =[
                            p1,
                            ft.DragTarget(
                                group="str",
                                content=p2,
                                on_accept=self.drag_accept,
                            ),
                        ]
                    )
                )
                
            ]
        )

        self.setModalDialog("EDITOR DATAFRAME",col,self.guardar)

    def pick_file_result(self,e: ft.FilePickerResultEvent):
        self.txt_ruta_archivo.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else self.txt_ruta_archivo.value
        )

        self.txt_ruta_archivo.update()

    def guardar(self):
        return True
    
    def getContainer(self,title,controls):
        con =[ft.Text(title)]
        con.extend(controls)

        return ft.Container(
                padding=5, 
                width=300,
                height=200,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(2,"#E3E3E3"),
                border_radius=5,
                alignment=ft.alignment.center,
                content= ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    width=300,
                    height=200,
                    controls=con
                    ))

    def add_dragtarget_item(self,text):
        def on_click(e):
            target = e.control.data
            panel = e.control

            target.visible =True
            panel.visible =False
            panel.update()
            target.update()

        return ft.ElevatedButton(
                bgcolor="#ebebeb",
                text =text,
                width=300,
                visible=False,
                on_click=on_click
                             )
    

    def add_draggle_item(self,index,text):
        return ft.Draggable(
                    group="str",
                    data=index,
                    content=ft.Container(
                       
                        content=ft.ElevatedButton(
                                bgcolor="#ebebeb",
                                text =text,
                                width=300),
                        alignment=ft.alignment.center,
                    ),
                )
    
    def drag_accept(self,e):
        # get draggable (source) control by its ID
        
        draggable = self.page.get_control(e.src_id)
        index = draggable.data
        
        drag = e.control.content.content
        
        #DragTarget
        btn = drag.controls[index]
        
        btn.data = draggable
        btn.visible=True
        draggable.visible=False
        
        drag.update()
        draggable.update()

def main(page: ft.Page):
    page.title = "Drag and Drop example"
    page.theme_mode=ft.ThemeMode.LIGHT
   
    d = editDataframe_view(page)
    

    page.add(
        d
    )

ft.app(main)