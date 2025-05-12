import flet as ft
from layouts.Notas.FilterTable import FilterTable_view
from collections import defaultdict
from layouts.PanelContainer import PanelContainer
import json

class DataTable(PanelContainer):
    def __init__(self,page,data):
        self.dataController =data
        super().__init__()
        self.page = page
        self.form =None
        self.orderBy=[False,"index"]
        self.initialize_components()
        self.scroll=ft.ScrollMode.ADAPTIVE
        self.content.controls=[
                self.header,
                ft.Column(
                    controls=[ft.Row(controls=[ self.table])],
                    scroll=ft.ScrollMode.HIDDEN,  # Habilitar el scroll automático
                    height=450,
                    expand=True),
                self.footer
                    ]
    def setForm(self,fr):
        self.form = fr

    def initialize_components(self):
        self.header = Header(self)
        self.footer = Footer(self)

        col = ft.Column(expand=True)
        self.content = col

        
  
        self.table_cols= []


        table_style={
            "expand":True,
            "border_radius":ft.border_radius.only(bottom_left=8,bottom_right=8),
            "border":ft.border.all(2,"#ebebeb"),
            "horizontal_lines":ft.border.BorderSide(1,"#ebebeb"),
            "columns":[ft.DataColumn(ft.Text("None",size=12,color="black", weight="bold"))]
        }


        self.table = ft.DataTable(**table_style)
        self.setTableColumns()
        
        
        

    def setDataTable(self):
        
        if (self.dataController.getData() is not None):
            self.setTableColumns()
            self.header.filter_view.add_items_combobox_filter(self.dataController.getColumns())
            
            order, column = self.orderBy

            self.dataController.setDataFrame()
            self.dataController.setOrder(order, column)
            self.dataController.setFilter(self.header.filterData)

            data = self.dataController.getData()

            if(len(data)):
                self.fill_items(data)
            else:
                print("setDataTable,None data")
        try:      
            pass 
        except Exception as ex:
            print(self.__class__,"setDataTable",ex)
            pass
        
    def clearData(self):
        try:
            #self.table.columns=[ft.DataColumn(ft.Text("",size=12,color="black", weight="bold",text_align=ft.TextAlign.CENTER))]
            self.table.rows=[]
            if self.table.page:
                self.table.update()
        except Exception as ex:
            print(self.__class__,"clearData",ex)
            pass
    
    def setTableColumns(self):
        self.clearData()
        self.table_cols= self.page.session.get("visibleColumns")

        cols = [ft.DataColumn(ft.Row([
            ft.Text("#",size=12,color="black", weight="bold"),
            ft.IconButton(
                icon=ft.Icons.ARROW_DROP_DOWN,
                data=[False,"index"],
                on_click=self.order_column
            )
        ],expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN))]


        cols.extend([
            ft.DataColumn(
                ft.Row([
                    ft.Text(col,size=12,color="black", weight="bold"),
                    ft.IconButton(
                        icon=ft.Icons.ARROW_DROP_DOWN,
                        data=[False,col],
                        on_click=self.order_column
                    )
                ],expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ) for col in self.table_cols
        ])

        #cols.append( ft.DataColumn(ft.Text("",size=12,color="black", weight="bold")))
        
        self.table.columns = cols
        if self.table.page is not None:
            self.table.update()

    def edit_row(self,e,index):
        data = self.dataController.getRow(index)

        if data is not None:
            self.form.setData(data)
        else:
            print("none data")

    def order_column(self,e):
        btn = e.control
        
        order, column = btn.data
        self.orderBy = btn.data

        self.dataController.setDataFrame()
        self.dataController.setFilter(self.header.filterData)
        self.dataController.setOrder(order, column)

        data = self.dataController.getData()

        btn.icon = ft.Icons.ARROW_DROP_DOWN if order else ft.Icons.ARROW_DROP_UP
        btn.data = [not order,column]
        btn.update() if btn.page else None

        if(data is not None):
            self.fill_items(data)

    

    def fill_items(self,data):

        if data is not None:
            self.footer.setSize(len(data))
            data = data[self.table_cols]
            data = data.iloc[self.footer.ini:self.footer.fin]
      
            rows=[]
            for index,row in data.iterrows():
                cell = [ft.DataCell(on_double_tap= lambda e, data=index: self.edit_row(e,data) ,content= ft.Text(index,color="black"))]
  
                cell.extend([ft.DataCell(on_double_tap= lambda e, data=index: self.edit_row(e,data),content= ft.Text(cell,color="black",selectable=True)) for cell in row])
                
                rows.append(ft.DataRow(cells=cell))

            self.table.rows=rows
            if self.table.page:
                self.table.update()
        else:
            print("Data None")



class Header(PanelContainer):
     
    def __init__(self, dt:DataTable):

        header_style={
            "height" : 80,
            "bgcolor" : "#ebebeb",
            "border_radius" : ft.border_radius.only(top_left=15,top_right=15),
            "padding":ft.padding.only(left=15,right=15,top=5),
            "margin":ft.margin.only(top=10,bottom=-10)
        }

        super().__init__(**header_style)
        self.datatable = dt
        self.filterData = defaultdict(lambda: defaultdict(list))
        self.filter_view = FilterTable_view(dt.page,onYes=self.btn_filter_datatable)

        self.filter = ft.Row(expand=True,spacing=10,alignment=ft.MainAxisAlignment.START)

        self.content=ft.Row(
            alignment=  ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[self.filter,
                      ft.IconButton(
                        icon=ft.Icons.FILTER_ALT_SHARP,
                        on_click=lambda _: self.filter_view.showModalDialog()
                    )]
        )

    def add_filter_data(self,filterby,option, value):
        if value not in self.filterData[filterby][option]:
            self.filterData[filterby][option].append(value)
        
    def add_filter_components(self):
        def delete_filter(target,data):
            try: 
                key,opt, item = data
            
                self.filterData[key][opt].remove(item)
                
                if not self.filterData[key][opt]:
                    del self.filterData[key]
                self.datatable.setDataTable()
                
                target.visible=False
                
                target.update()
            except:
                pass

        row =[]
        for col,options in self.filterData.items():
            for opt, value in options.items():
                for item in value :
                    content =ft.Container(
                        height=50,
                        border=ft.border.all(2,"#E3E3E3"),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=8,
                        padding=ft.padding.only(left=10),
                        
                        content=ft.Row(spacing=5
                                    ,controls=[ft.Column([ft.Text(col,size=11, weight="bold"),ft.Text(f" {item}",size=10)],spacing=0)])
                    )

                    btn = ft.IconButton(
                                        icon_size=12,
                                        width=20,
                                        height=20,
                                        padding=2,
                                        icon=ft.Icons.CLOSE,
                                        
                                        on_click=lambda e,target=content, data=[col,opt,item]: delete_filter(target,data)
                                        )
                    content.content.controls.append(btn)
                    row.append(content)

        self.filter.controls=row
                  

    def btn_filter_datatable(self,filterby,option,value):
       
        if(filterby):
            self.add_filter_data(filterby,option,value)
            self.add_filter_components()
            self.datatable.setDataTable()
            self.update()
        else:
            self.showAlertDialog("Error!","ingrese un valor al filtrar", ft.Icons.ERROR)

class Footer(PanelContainer):
    
    def __init__(self, dt:DataTable):

        header_style={
            "height" : 60,
            "bgcolor" : "#ebebeb",
            "border_radius" : ft.border_radius.only(bottom_left=15,bottom_right=15),
            "padding":ft.padding.only(left=15,right=15,bottom=5),
            "margin":ft.margin.only(top=-10,bottom=10)
        }

        super().__init__(**header_style)
        self.lenText = ft.Text(value="0" , size=12)
        self.dataTable = dt
        self.pg = 1
        self.rows_per_page=8
        self.total_page = 0
        self.size = 0
        self.ini=0
        self.fin = self.rows_per_page

        self.display=ft.Row(width=500, alignment=  ft.MainAxisAlignment.END, scroll=ft.ScrollMode.AUTO,
            controls=[])
        self.content=ft.Row(
            alignment=  ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
            controls=[self.lenText,self.display]
        )

    def setSize(self,value):
        self.size = value
        
        self.setDisplay()
        self.lenText.value=f"Página {self.pg} de {self.total_page} - Total {value}"
        self.lenText.update() if self.lenText.page else None
        

    def setDisplay(self):
        def btnPage(e):
            page = e.control.data
            self.paginate(
                page=page
            )

        self.total_page = (self.size // self.rows_per_page)
        controls = [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: self.paginate(page= max(1, self.pg - 1))
            )
        ]

        controls.extend([
            ft.ElevatedButton(text=num,
                            width=30 ,
                            data = num,
                            on_click=btnPage,
                            bgcolor= ft.colors.GREY if self.pg == num else ft.colors.WHITE,
            ) for num in range(1,(self.total_page+ 1))
        ])

        controls.append(
            ft.IconButton(
                icon=ft.Icons.ARROW_FORWARD,
                on_click=lambda _: self.paginate(page= self.pg if self.pg == self.total_page else self.pg+1)
            )
        )
    
        self.display.controls =controls
        self.display.update() if self.display.page else None
    
   
    def paginate(self,page):
        self.pg=page

        tot = (self.size // self.rows_per_page)

        self.ini = (self.pg - 1)*self.rows_per_page
        
        self.fin = self.size if self.pg==tot else (self.ini+self.rows_per_page)
        self.dataTable.setDataTable()
        self.setSize(self.size)