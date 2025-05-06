
import flet as ft
from layouts.PanelContainer import PanelContainer
from controllers.DataController import DataController
from controllers.ConfigController import ConfigController

class FilterTable_view(PanelContainer):

    def __init__(self, page,onYes:callable=None,onNo:callable=None, **kwargs):
        super().__init__(**kwargs)
        self.page = page

        self.onYes=onYes
        self.onNo=onNo
        self.configController = ConfigController()

        self.initialize_components()
        self.add_items_combobox_option(["igual a","no igual","contiene","no contiene"])
        self.initFilterPred()

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
            if filterName.value !="":
                self.predFilterPanel.controls.append(self.getItemFilterPred(filterName.value))
                filterName.value =""

                filterName.update() if filterName.page else None
                self.predFilterPanel.update() if self.predFilterPanel.page else None

        filterName =ft.TextField(
                        border_color="transparent",
                        width=70,
                        height=15,
                        text_size=10,
                        content_padding=0,
                        cursor_color="black",
                        cursor_width=1,
                        cursor_height=18,
                        color="black"
                    )
        header = ft.ListTile(
                    height=35,
                    title=ft.Text("FILTROS PREDETERMINADOS",size=13,weight=ft.FontWeight.BOLD,color=ft.colors.BLUE_900),
                    trailing=ft.Row([filterName,ft.IconButton(icon_size=18,width=35,height=35,icon=ft.Icons.ADD,on_click=btnPredOnclick)],width=110)
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

    def getRowItemFilterPred(self, col, opt, val, item):
        

        def handle_delete_row(e: ft.ControlEvent):
            print(item.controls)
            print(e) 
            item.controls.remove(row)
            item.update() if item.page else None

        row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,data =[col,opt,val] )
        row.controls = [
                    ft.Row([ft.Text(value="Columna:",weight=ft.FontWeight.BOLD),ft.Text(col)]),
                    ft.Row([ft.Text(value="Tipo:",weight=ft.FontWeight.BOLD),ft.Text(opt)]),
                    ft.Row([ft.Text(value="Valor:",weight=ft.FontWeight.BOLD),ft.Text(val)]),
                    ft.IconButton(icon_size=18,width=35,height=35,icon=ft.Icons.DELETE,icon_color=ft.Colors.RED, data =row , on_click=handle_delete_row)]

        

        return row
    
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
            col = self.fiter_combobox.value.upper() 
            opt= self.option_combobox.value.upper() 
            val = self.txt_filter.value.upper() 
            
            if (col == "" or
                opt =="" or
                val ==""):
                    self.showBottomSheetMsg("Campos obligatorios",icon=ft.Icons.INFO)    
                    
            else:
                row = self.getRowItemFilterPred(col,opt,val,item)
                item.controls.append(row)
                item.update() if item.page else None

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
        #self.fiter_combobox.value = ""
        #self.fiter_combobox.update() if self.fiter_combobox.page else None

        #self.option_combobox.value ="igual a"
        #self.option_combobox.update() if self.option_combobox.page else None

        self.txt_filter.value =""
        self.txt_filter.update() if self.txt_filter.page else None


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
                
        if (filterData !={}):
            
            data = {
            "FilterPred":filterData
            }

            data = self.configController.edit_json(data)

            self.showBottomSheetMsg(
                text="Datos Guardados Correctamente!", 
                icon=ft.Icons.CHECK) 
        return False
    
    def setFilter(self,e):
        col = self.fiter_combobox.value.upper() 
        opt= self.option_combobox.value.upper() 
        val = self.txt_filter.value.upper() 
        
        if (col == "" or
            opt =="" or
            val ==""):
            self.showBottomSheetMsg("Campos obligatorios",icon=ft.Icons.INFO)    
        else:
            
            if self.onYes !=None:
            
                self.onYes(filterby=col
                            ,option=opt
                            ,value=val)
            self.clean_val()
            
    def initFilterPred(self):
        data = self.page.session.get("FilterPred")
        self.predFilterPanel.controls=[]

        for filter_name,rows in data.items():
            item_filt = self.getItemFilterPred(filter_name)
            
            for col, data in rows.items():
                opt = data["TYPE"]
                vals = data["VALUES"]
                for val in vals:
                    row = self.getRowItemFilterPred(col,opt,val,item_filt)
                    item_filt.controls.append(row)

            self.predFilterPanel.controls.append(item_filt)
            self.predFilterPanel.update() if self.predFilterPanel.page else None

