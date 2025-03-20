
import flet as ft
from layouts.PanelContainer import PanelContainer
from controllers.DataController import DataController

class FilterTable_view(PanelContainer):

    def __init__(self, page,onYes:callable=None,onNo:callable=None, **kwargs):
        super().__init__(**kwargs)
        self.page = page

        self.onYes=onYes
        self.onNo=onNo

        self.initialize_components()
        self.add_items_combobox_option(["igual a","no igual","contiene","no contiene"])
        self.add_items_combobox_filter(["igual a","no igual","contiene","no contiene"])

    def initialize_components(self):
        col = ft.Column(spacing=20,width=650,height=400,controls=[],scroll=ft.ScrollMode.AUTO)
        
        self.fiter_combobox = ft.Dropdown(
                label = "Filtrar por",

                text_size=14,
                border_color="#e0e0e0",
                filled=False,
                focused_bgcolor= ft.Colors.RED,
                height=40,
                width=200,
                content_padding=10,
                options=[],
            )
        
        self.option_combobox = ft.Dropdown(
                label = "Tipo",

                text_size=14,
                border_color="#e0e0e0",
                filled=False,
                focused_bgcolor= ft.Colors.RED,
                height=40,
                width=150,
                content_padding=10,
                options=[],
            )
        
        self.txt_filter = ft.TextField(
                            border_color="#e0e0e0",
                            height=40,
                            width=230,      

                            text_size=14,
                            content_padding=10,
                            cursor_color="#e0e0e0",
                            hint_text="Buscar..."
                        )
        exp =  ft.Column([
                        ft.ListTile(
                            height=35,
                            title=ft.Text("FILTROS",size=13,weight=ft.FontWeight.BOLD,color=ft.colors.BLUE_900)
                        ),
                        ft.Divider(),
                        ft.Container(
                            padding=ft.padding.only(top=10),
                            content=ft.Row(
                                        [self.fiter_combobox,
                                        self.option_combobox,
                                        self.txt_filter,
                                        ft.IconButton(icon_size=18,width=35,height=35,icon=ft.Icons.ADD,on_click=self.setFilter)
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    )
                        )
                    ],spacing=0)
                    
        col.controls.append(exp)

        
                
        self.predFilterPanel = ft.Column(controls=[],alignment=ft.MainAxisAlignment.CENTER,)

        def btnPredOnclick(e):
            index = len(self.predFilterPanel.controls) +1
            self.predFilterPanel.controls.append(self.getItemFilterPred(f"Filtro {index}"))
            self.predFilterPanel.update() if self.predFilterPanel.page else None

        header = ft.ListTile(
                    height=35,
                    title=ft.Text("FILTROS PREDETERMINADOS",size=13,weight=ft.FontWeight.BOLD,color=ft.colors.BLUE_900),
                    trailing=ft.IconButton(icon_size=18,width=35,height=35,icon=ft.Icons.ADD,on_click=btnPredOnclick)
                )
        
        col.controls.append(
            ft.Column([
                header,
                ft.Divider(),
                ft.Container(
                    padding=ft.padding.only(top=10),
                    content=self.predFilterPanel
                )
            ],spacing=0))

        self.setModalDialog("FILTER DATAFRAME",col,self.guardar,self.onNo)
        

    def add_items_combobox_filter(self, opt):
        self.fiter_combobox.options = [ft.dropdown.Option(item) for item in opt]
        self.fiter_combobox.update() if self.fiter_combobox.page else None

    def add_items_combobox_option(self, opt):
        self.option_combobox.options = [ft.dropdown.Option(item) for item in opt]
        self.option_combobox.value = opt[0]
        self.option_combobox.update() if self.option_combobox.page else None

    def addItemFilter(self):
        print("Hola")

    def getItemFilterPred(self,name):
        def handle_delete(e: ft.ControlEvent):
            self.predFilterPanel.controls.remove(e.control.data)
            self.predFilterPanel.update() if self.predFilterPanel.page else None
        
        def setDataFilter(e):
            for row in item.controls:
                data = row.data

                self.onYes(filterby=data[0]
                            ,option=data[1]
                            ,value=data[2])

        def addData(e: ft.ControlEvent):
            def handle_delete_row(e: ft.ControlEvent):
                item.controls.remove(e.control.data)
                item.update() if self.predFilterPanel.page else None

            col = self.fiter_combobox.value 
            opt= self.option_combobox.value 
            val = self.txt_filter.value 
            
            if (col == "" or
                opt =="" or
                val ==""):
                    self.showBottomSheetMsg("Campos obligatorios",icon=ft.Icons.INFO)    
                    
            else:
                row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,data =[col,opt,val] )
                row.controls = [
                                ft.Row([ft.Text(value="Columna:",weight=ft.FontWeight.BOLD),ft.Text(col)]),
                                ft.Row([ft.Text(value="Tipo:",weight=ft.FontWeight.BOLD),ft.Text(opt)]),
                                ft.Row([ft.Text(value="Valor:",weight=ft.FontWeight.BOLD),ft.Text(val)]),
                              ft.IconButton(icon_size=18,width=35,height=35,icon=ft.Icons.DELETE,icon_color=ft.Colors.RED, data =row , on_click=handle_delete_row)]
                item.controls.append(row)
                item.initially_expanded=True
                item.update() if item.page else None
                #self.addItemFilter(col,opt,val)

        item = ft.ExpansionTile(
                title=ft.Text(name,size=12,weight=ft.FontWeight.BOLD),
                affinity=ft.TileAffinity.LEADING,
                initially_expanded=False,
                collapsed_text_color=ft.Colors.BLACK,
                text_color=ft.Colors.BLUE_900,
                controls_padding=ft.padding.only(left=15,right=15),
                controls=[]
            )
        
        item.trailing= ft.Row(width=90,spacing=0,controls=[
            ft.IconButton(icon_size=18,width=35,height=35, icon=ft.Icons.DELETE,icon_color=ft.Colors.RED, data =item , on_click=handle_delete),
            ft.IconButton(icon_size=18,width=35,height=35, icon=ft.Icons.ADD,icon_color=ft.Colors.GREEN, data =item , on_click=addData),
            ft.IconButton(icon_size=18,width=35,height=35, icon=ft.Icons.REMOVE_RED_EYE, data =item, on_click=setDataFilter)
        ])

        return item

    def clean_val(self):
        self.fiter_combobox.value = ""
        self.option_combobox.value ="igual a"
        self.txt_filter.value =""

    def setData(self,filterby,option,value):
        self.fiter_combobox.value = filterby
        self.fiter_combobox.update() if self.fiter_combobox.page else None

        self.option_combobox.value = option
        self.option_combobox.update() if self.option_combobox.page else None

        self.txt_filter.value = value
        self.txt_filter.update() if self.txt_filter.page else None

        
    def guardar(self):
        filterData={}
        
        for item in self.predFilterPanel.controls:
            title = item.title.value
            rows = item.controls
            
            for row in rows:
                
                filterby=row.data[0]
                option=row.data[1]
                value=row.data[2]

                if not title in filterData:
                    filterData[title]={}

                if filterby in filterData[title]:
                    if value not in filterData[title][filterby]["VALUES"]:
                        filterData[title][filterby]["VALUES"].append(value) 
                        filterData[title][filterby]["TYPE"]=option
                else:
                    filterData[title][filterby] = {"VALUES":[value],"TYPE":option}
                
        
        print(filterData)
        return False
    
    def setFilter(self):
        col = self.fiter_combobox.value 
        opt= self.option_combobox.value 
        val = self.txt_filter.value 
        
        if (col == "" or
            opt =="" or
            val ==""):
            self.showBottomSheetMsg("Campos obligatorios",icon=ft.Icons.INFO)    
        else:
            
            if self.onYes !=None:
            
                self.onYes(filterby=self.fiter_combobox.value.upper()
                            ,option=self.option_combobox.value.upper()
                            ,value=self.txt_filter.value.upper())
            self.clean_val()
            
        

