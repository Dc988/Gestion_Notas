import flet as ft
from layouts.PanelContainer import PanelContainer

class DataTable(PanelContainer):
    def __init__(self,data):
        self.dataController =data
        super().__init__()
        self.initialize_components()
        self.scroll=ft.ScrollMode.AUTO
        self.content.controls=[
                self.header,
                ft.Column(
                    controls=[ft.Row(controls=[ self.table])],
                    scroll=ft.ScrollMode.HIDDEN,  # Habilitar el scroll automático
                    height=300,
                    expand=True)
                    ]
        
    def initialize_components(self):
        self.header = Header(self)
        col = ft.Column(expand=True)
        self.content = col
        table_cols=["#",
                    "FASE",
                    "ACTIVIDAD",
                    "CODIGO ACTIVIDAD",
                    "CODIGO EVIDENCIA",
                    "OPCIONES",
                    ]
        table_style={
            "expand":True,
            "border_radius":ft.border_radius.only(bottom_left=8,bottom_right=8),
            "border":ft.border.all(2,"#ebebeb"),
            "horizontal_lines":ft.border.BorderSide(1,"#ebebeb"),
            "columns":[ft.DataColumn(ft.Text(col,size=12,color="black", weight="bold")) for col in table_cols]
        }
        self.table = ft.DataTable(**table_style)
        
        

    def setDataTable(self):
        try:
            if (self.dataController.getData() is not None):
                self.header.add_items_combobox()
    
                self.fill_items(self.dataController.getData())
               
        except Exception as ex:
            print(self.__class__,"setDataTable",ex)
            pass
        
    def clearData(self):
        try:
            #self.table.columns=[ft.DataColumn(ft.Text("",size=12,color="black", weight="bold",text_align=ft.TextAlign.CENTER))]
            self.table.rows=[]
            self.table.update()
        except Exception as ex:
            print(self.__class__,"clearData",ex)
            pass
    
            
    def edit_row(self,e,index):
        self.showAlertDialog("edit_row",index)

    def delete_row(self,e,index):
        self.showAlertDialog("delete",index)

    def fill_items(self,data):
        if data is not None:
            
            data = data[["FASE","ACTIVIDAD","CODIGO ACTIVIDAD","COMPLETO"]]
            rows=[]
            for index,row in data.iterrows():
                cell = [ft.DataCell(ft.Text(index,color="black"))]
                
                cell.extend([ft.DataCell(ft.Text(cell,color="black")) for cell in row])
                cell.extend([
                    ft.DataCell(
                        content=ft.Row(
                            expand=True, 
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.colors.AMBER,
                                    on_click=lambda e, data=index: self.edit_row(e,data)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=ft.colors.RED,
                                    on_click=lambda e, data=index: self.delete_row(e,data)
                                )
                            ]
                        )
                    )
                ])
                rows.append(ft.DataRow(cells=cell))

            self.table.rows=rows
            self.table.update()
        else:
            print("Data None")

class Header(PanelContainer):
 
    def search_bar(self,control):
        return ft.Container(
            
            width=500,
            bgcolor="white10",
            border_radius=6,
            animate_opacity=300,
            padding=8,
            content=control
            )
    
    def __init__(self, dt:DataTable):

        header_style={
            "height" : 50,
            "bgcolor" : "#ebebeb",
            "border_radius" : ft.border_radius.only(top_left=15,top_right=15),
            "padding":ft.padding.only(left=15,right=15,top=5),
            "margin":ft.margin.only(bottom=-10)
        }

        super().__init__(**header_style)
        self.datatable = dt
        self.filterData ={}
        self.fiter_combobox = ft.Dropdown(
                label = "Filtrar por",

                text_size=12,
                border_color="transparent",
                filled=False,
                focused_bgcolor= ft.colors.RED,
                width=120,
                height=40,
                content_padding=10,
                options=[],
            )
        self.txt_filter = ft.TextField(
                            border_color="transparent",
                            height=20,
                            width=100,
                            text_size=14,
                            content_padding=0,
                            cursor_color="white",
                            hint_text="Search"
                        )
        btn_filter = ft.IconButton(
                            icon=ft.icons.SEARCH_ROUNDED,
                            on_click=self.btn_filter_datatable,
                            icon_size=15    
                        )
        
        self.search_bar = self.search_bar(ft.Row(
            expand=True,
            alignment="end",
            spacing=30,
            controls=[self.fiter_combobox,self.txt_filter,btn_filter]
        ))

        self.filter = ft.Row(expand=True,spacing=10,alignment=ft.MainAxisAlignment.START)

        self.content=ft.Row(
            alignment=  ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[self.filter,self.search_bar]
        )

    def add_filter_data(self,filterby, value):
        if filterby in self.filterData:
            if value not in self.filterData[filterby]:
                self.filterData[filterby].append(value)  
        else:
            self.filterData[filterby] = [value]
            
        self.txt_filter.value=""
        
    
    def add_filter_components(self):
        def delete_filter(e,target,data):
            key,item = data
            self.filterData[key].remove(item)
            if not self.filterData[key]:
                del self.filterData[key]
            self.filter_datatable()
            
            target.visible=False
            target.update()

        row =[]
        for key,value in self.filterData.items():
            for item in value :
                content =ft.Container(
                    border=ft.border.all(2,"#E3E3E3"),
                    bgcolor=ft.colors.WHITE,
                    border_radius=8,
                    padding=ft.padding.only(left=10),
                    content=ft.Row(spacing=5
                                ,controls=[ft.Column([ft.Text(key,size=11, weight="bold"),ft.Text(f" {item}",size=10)],spacing=0)])
                )
                btn = ft.IconButton(
                                    icon_size=12,
                                    width=20,
                                    height=20,
                                    padding=2,
                                    icon=ft.icons.CLOSE,
                                    
                                    on_click=lambda e,target=content, data=[key,item]: delete_filter(e,target,data)
                                    )
                content.content.controls.append(btn)
                row.append(content)

        self.filter.controls=row

        
    def filter_datatable(self):
        
        data = self.datatable.dataController.setFilter(
            self.filterData
        )
        
        if(data is not None):
            self.datatable.fill_items(data)
        
       
            

    def btn_filter_datatable(self,e):
        filterby=self.fiter_combobox.value
        value = self.txt_filter.value.upper()

        if(filterby and value):
            self.add_filter_data(filterby,value)
            self.add_filter_components()
            self.filter_datatable()
            self.update()
        else:
            self.showAlertDialog("Error!","ingrese un valor al filtrar", ft.icons.ERROR)

    def add_items_combobox(self):
        self.fiter_combobox.options = [ft.dropdown.Option(item) for item in self.datatable.dataController.getColumns()]

