
import flet as ft
from layouts.PanelContainer import PanelContainer

class editDataframe_view(PanelContainer):

    def __init__(self, page,onYes:callable=None,onNo:callable=None, **kwargs):
        super().__init__(**kwargs)
        self.page = page

        self.onYes=onYes
        self.onNo=onNo

        self.initialize_components()

    def initialize_components(self):
        self.dataController = None
        self.selectedCols = []

        self.dragTarget = self.getContainer(
            title="Columas Visibles",
            controls=[]
            )
        
        self.dragglePanel =self.getContainer(
                title="Columas Originales",
                controls=[]
        )

        col = ft.Column(
            controls=[
                
                self.component_container(
                    expand=False,
                    name="Columnas del Archivo",
                    icon =ft.Icons.GRID_3X3,
                    control=ft.Row(
                        controls =[
                            self.dragglePanel,
                            ft.DragTarget(
                                group="str",
                                content=self.dragTarget,
                                on_accept=self.drag_accept,
                            ),
                        ]
                    )
                ),
            ]
        )

        self.setModalDialog("EDITOR DATAFRAME",col,self.guardar,self.onNo)
        

        



    def guardar(self):
        self.selectedCols = []
        self.ruta = ""
        band = True
        for item in self.dragTarget.content.controls:

            if(type(item) is ft.ElevatedButton  and item.visible):
                self.selectedCols.append(item.text)

        if(not self.selectedCols):

            self.showBottomSheetMsg("Seleccione al menos una columna!!!",ft.Icons.ERROR)
            band = False
            
        if self.onYes !=None:
            self.onYes()

        return band 


        

    
    def getContainer(self,title,controls):
        con =[ft.Text(title)]
        con.extend(controls)

        return ft.Container(
                padding=5, 
                width=300,
                height=200,
                bgcolor=ft.Colors.WHITE,
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

    def add_dragtarget_item(self,index,text):
        def on_click(e):
            index = e.control.data + 1
            
            target = self.dragglePanel.content.controls[index]
            panel = e.control

            target.visible =True
            panel.visible =False
            panel.update()
            target.update()

        return ft.ElevatedButton(
                data=index,
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
        index = draggable.data + 1
        
        drag = e.control.content.content
        
        #DragTarget
        btn = drag.controls[index]

        btn.visible=True
        draggable.visible=False
        
        drag.update()
        draggable.update()

    def setData(self, data):

        self.InitializeData()
        for item in self.dragTarget.content.controls:
            if(type(item) is ft.ElevatedButton and item.text in data):
                item.visible = True
        for item in  self.dragglePanel.content.controls:
            if(type(item) is ft.Draggable and item.content.content.text in data):
                item.visible = False
        self.selectedCols = data

        
    def InitializeData(self):
       
        columns =self.page.session.get("col_oblig")

        con =[ft.Text("Columas Visibles")]
        con.extend([self.add_dragtarget_item(index,item) for index,item in enumerate(columns)])

        self.dragTarget.content.controls = con
    
        con =[ft.Text("Columas Originales")]
        con.extend([self.add_draggle_item(index,item) for index,item in enumerate(columns)])

        self.dragglePanel.content.controls = con

        if self.dragglePanel.page:
            self.dragglePanel.update()
        if self.dragTarget.page:
            self.dragTarget.update()
        
                    #self.showBottomSheetMsg("Columnas no coinciden FASE, ACTIVIDAD, CODIGO ACTIVIDAD, EVIDENCIA, FECHA, NOTA, OBSERVACION",ft.Icons.ERROR)
       
                    
