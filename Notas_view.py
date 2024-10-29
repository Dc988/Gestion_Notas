import flet as ft
from Config_view import Config_view
from layouts.PanelContainer import PanelContainer
from layouts.NotasFormContainer import Form
from controllers.DataController import DataController

class Notas_view(PanelContainer):
    def __init__(self, page,**kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.initialize_components()
        self.content.controls=[ft.Text("13"),self.fr]
               
    def initialize_components(self):
        self.config_panel = Config_view(self.page)
        self.fr = Form()
        col = ft.Column(expand=True)
        self.margin = 10
        self.padding = 10
        self.content = col
        self.setDataTable()
        
    def setDataTable(self):
        if(self.config_panel.getRuta() !="" or self.config_panel.getExtencion()!=""):
            self.data = DataController(
                ruta=self.config_panel.txt_ruta_archivo.value,
                extencion=self.config_panel.txt_extencion.value)
            
            if not self.data.read_file():
                self.showAlertDialog("Error!! Panel Notas", "No se pudo cargar la información",ft.icons.ERROR)
            else:
                self.showAlertDialog("Mensaje!! Panel Notas", "Información cargada correctamente",ft.icons.THUMB_UP)

        
    def prueba(self,e):
        self.showOptionDialog(
            title="Upps!",
            
            YesOption=self.yes,
            icon=ft.icons.INFO)
        
    def yes(self):
        
        self.showAlertDialog("Prueba 2",self.config_panel.txt_ruta_archivo.value)

class Controller():
    dumy={
        0:{
            "name":"name 0",
            "data":"data 0"
        },
        1:{
            "name":"name 1",
            "data":"data 1"
        },
        2:{
            "name":"name 2",
            "data":"data 2"
        },
        3:{
            "name":"name 3",
            "data":"data 3"
        },
        4:{
            "name":"name 4",
            "data":"data 4"
        },
        

    }
    
    @staticmethod
    def get_items():
        return Controller.dumy
    def add(data):
        Controller.dumy[len(Controller.get_items())] = data
        
    
    

def search_field(function:callable):
           
    return ft.TextField(
        border_color="transparent",
        height=20,
        text_size=14,
        content_padding=0,
        cursor_color="white",
        hint_text="Search",
        on_change=function
    )


def search_bar(control):
    return ft.Container(
        width=350,
        bgcolor="white10",
        border_radius=6,
        opacity=0,
        animate_opacity=300,
        padding=8,
        content=ft.Row(
            controls=[
                ft.Icon(
                name=ft.icons.SEARCH_ROUNDED,
                size=17,
                opacity=0.85
            ),
            control]
        )

    )

class DataTable(ft.DataTable):
    def __init__(self):
        cols=["name","data"]

        table_style={
            "expand":True,
            "border_radius":8,
            "border":ft.border.all(2,"#ebebeb"),
            "horizontal_lines":ft.border.BorderSide(1,"#ebebeb"),
            "columns":[
                ft.DataColumn(ft.Text(index,size=12,color="black", weight="bold")) for index in cols
            ]
        }

        super().__init__(**table_style)


        self.df = Controller.get_items()

    def fill_items(self):
        self.rows=[]
        for values in self.df.values():
            cells = [ft.DataCell(ft.Text(value,color="black"))for value in values.values()]
            data = ft.DataRow(cells=cells)

            self.rows.append(data)
        self.update()




class Header(ft.Container):
    def __init__(self, dt:DataTable):

        header_style={
            "height" : 60,
            "bgcolor" : "#081d33",
            "border_radius" : ft.border_radius.only(top_left=15,top_right=15),
            "padding":ft.padding.only(left=15,right=15)
        }
        super().__init__(**header_style, on_hover=self.toggle_search)
        self.datatable = dt

        self.searchfield = search_field(self.filter_datatable)
        self.search_bar = search_bar(self.searchfield)
        self.name = ft.Text("LINE IDENT")
        self.avatar= ft.IconButton("person")

        self.content=ft.Row(
            alignment="spaceBetween",
            controls=[self.name,self.search_bar,self.avatar]
        )
    def toggle_search(self,e:ft.HoverEvent):
        self.search_bar.opacity = 1 if e.data=="true" else 0
        self.search_bar.update()
    
    def filter_datatable(self,e):
        
        for row in self.datatable.rows:
            cell = row.cells[0]
            print()
            row.visible = e.control.value.lower() in cell.content.value.lower()
            
            self.datatable.update()
            
        
