
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

    def initialize_components(self):
        
        self.fiter_combobox = ft.Dropdown(
                label = "Filtrar por",

                text_size=14,
                border_color="#e0e0e0",
                filled=False,
                focused_bgcolor= ft.Colors.RED,
                height=40,
                width=150,
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
                            width=200,      

                            text_size=14,
                            content_padding=10,
                            cursor_color="#e0e0e0",
                            hint_text="Buscar..."
                        )
        col = ft.Row(
            expand=True,
            spacing=10,
            width=520,
            controls=[
                self.fiter_combobox,
                self.option_combobox,
                self.txt_filter
            ]
        )

        self.setModalDialog("FILTER DATAFRAME",col,self.guardar,self.onNo)
        

    def add_items_combobox_filter(self, opt):
        self.fiter_combobox.options = [ft.dropdown.Option(item) for item in opt]
        self.fiter_combobox.update() if self.fiter_combobox.page else None

    def add_items_combobox_option(self, opt):
        self.option_combobox.options = [ft.dropdown.Option(item) for item in opt]
        self.option_combobox.update() if self.option_combobox.page else None

    def clean_val(self):
        self.fiter_combobox.value = ""
        self.option_combobox.value =""
        self.txt_filter.value =""

    def guardar(self):
        
        band = True
        
        if (self.fiter_combobox.value == "" or
        self.option_combobox.value =="" or
        self.txt_filter.value ==""):
            self.showBottomSheetMsg("Campos obligatorios",icon=ft.Icons.INFO)    
            band=False
        else:
            if self.onYes !=None:
                
                self.onYes(filterby=self.fiter_combobox.value
                            ,option=self.option_combobox.value
                            ,value=self.txt_filter.value)
            self.clean_val()
            band=True

        return band 
        

