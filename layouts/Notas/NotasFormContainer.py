import flet as ft
import os
import datetime
from layouts.PanelContainer import PanelContainer

class Form(PanelContainer):
   
    def __init__(self,page,dc=None,dt=None):

        form_style={
            "border_radius":8,
            "border":ft.border.all(1,"#ebebeb"),
            "bgcolor":"white10",
            "padding":15,
            "margin":ft.margin.only(top=15,bottom=5)
        }
        
        super().__init__(**form_style)
        self.page = page
        
        self.dataController = dc
        self.dataTable = dt
    
        self.initComponents()
        self.addControls()
        
    def addControls(self):
        col=ft.Column(
            width=1100,
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                    ft.Row(controls=[
                        self.component_container(
                            expand=True,name="FASE",
                            control=self.fase_txt,
                            icon =ft.icons.TEXT_FIELDS,
                            trailing=ft.IconButton(
                                icon=ft.icons.ADD,
                                on_click= lambda _: self.open_os(self.fase_txt.value)
                            )),
                        self.component_container(
                            expand=True,name="ACTIVIDAD",
                            control=self.actividad_txt,
                            icon =ft.icons.TEXT_FIELDS,
                            trailing=ft.IconButton(
                                icon=ft.icons.ADD,
                                on_click=lambda _:self.open_os(f"{self.fase_txt.value}\\{self.actividad_txt.value}")
                            )),
                    
                        self.component_container(
                            expand=True,name="CODIGO ACTIVIDAD",
                            control=self.cod_act_txt,
                            icon =ft.icons.CODE,
                            trailing=ft.IconButton(
                                icon=ft.icons.ADD,
                                on_click=lambda _:self.open_os(f"{self.fase_txt.value}\\{self.actividad_txt.value}\\{self.cod_act_txt.value}")
                            )),
                    ], expand=True),
                    
                    self.component_container(
                        expand=True,name="EVIDENCIA",
                        control=self.evid_txt,
                        icon =ft.icons.BOOK,
                        trailing=ft.IconButton(
                            icon=ft.icons.ADD,
                            on_click=lambda _:self.open_os(f"{self.fase_txt.value}\\{self.actividad_txt.value}\\{self.cod_act_txt.value}\\{self.evid_txt.value}")
                        )),

                    ft.Row(controls=[
                        self.component_container(
                            expand=True,name="NOTA",
                            control=self.nota_txt,
                            icon =ft.icons.NOTES),

                        self.component_container(
                            expand=True,name="FECHA",
                            control=self.fecha_txt,
                            icon =ft.icons.CALENDAR_MONTH,
                            trailing=ft.IconButton(
                                icon=ft.icons.EDIT_CALENDAR,
                                on_click=lambda _:self.page.open(
                                    self.dt
                                )
                            )),
                        
                        self.component_container(
                            expand=True,name="IMPORTANTE",
                            control=self.impr_check,
                            icon =ft.icons.LABEL_IMPORTANT),
                    ]),
                    self.component_container(
                                    expand=True,name="OBSERVACION",
                                    control=self.cb,
                                    icon =ft.icons.MENU_OPEN),
                    ft.Row(controls=[
                    
                        self.component_container(
                                    expand=True,name="OBSERVACION",
                                    control=self.observacion_txt,
                                    icon =ft.icons.MENU_OPEN),
                        ft.IconButton(
                            icon=ft.icons.PICTURE_AS_PDF,
                            on_click=lambda _:self.open_os(f"{self.fase_txt.value}\\{self.actividad_txt.value}\\Guia_aprendizaje.pdf")
                        )
                    ])
            ]
        )
        self.setModalDialog("EVIDENCIA",col,self.onYesOption)

    def initComponents(self):
        self.data = {}
        self.cb = ft.Dropdown(
                label = "",
                height=20,
                text_size=13,
                border_color="transparent",
                content_padding=10,
                options=[ft.dropdown.Option(1),ft.dropdown.Option(2),ft.dropdown.Option(3)],
            )
        self.index_txt = self.textfield()
        self.fase_txt = self.textfield()
        self.actividad_txt = self.textfield()
        self.cod_act_txt = self.textfield()
        self.evid_txt = self.textfield()
        self.fecha_txt = self.textfield()
        self.nota_txt = self.textfield()
        self.observacion_txt = self.textfield()
        self.impr_check = ft.Checkbox()
        self.dt = ft.DatePicker(
                    first_date=datetime.datetime(year=2000, month=1, day=1),
                    on_change=self.handle_change
                )
       
    def handle_change(self,e):
        self.fecha_txt.value =e.control.value.strftime('%Y-%m-%d')

        self.fecha_txt.update() if self.fecha_txt.page else None

    def onYesOption(self):
        if(
            self.fase_txt .value=="" or
            self.actividad_txt .value=="" or
            self.cod_act_txt .value=="" or
            self.evid_txt .value=="" or
            self.fecha_txt .value=="" or
            self.nota_txt .value==""):
                self.showErrorMsg("Campos obligatorios!!!")
        else:
            self.showErrorMsg()
            self.data = {
                "FASE":self.fase_txt .value,
                "ACTIVIDAD":self.actividad_txt .value,
                "CODIGO ACTIVIDAD":self.cod_act_txt .value,
                "EVIDENCIA":self.evid_txt .value,
                "FECHA":self.fecha_txt .value,
                "NOTA":self.nota_txt .value,
                "OBSERVACION":self.observacion_txt .value,
                "IMPORTANTE":"SI"  if self.impr_check.value else "NO"
            }

            if (self.index_txt.value==""):
                self.save()
            else:
                self.edit()

            if (self.dataTable is not None):
                self.dataTable.setDataTable()
            else:
                self.showErrorMsg("Error!!! no se pudo actualizar la tabla")


        
    def setData(self, data):
        try:
            self.clear_data()
            self.showErrorMsg()
            self.showSuccessMsg()

            self.index_txt.value = data.name
            self.fase_txt .value = data["FASE" ]
            self.actividad_txt .value = data["ACTIVIDAD" ]
            self.cod_act_txt .value = data["CODIGO ACTIVIDAD" ]
            self.evid_txt .value = data["EVIDENCIA" ]
            self.fecha_txt .value = data["FECHA" ]
            self.nota_txt .value = data["NOTA" ]
            self.observacion_txt .value = data["OBSERVACION" ]
            self.impr_check.value = data["IMPORTANTE" ] == "SI"

            self.fase_txt.update()  if self.fase_txt.page else None
            self.actividad_txt.update() if self.actividad_txt.page else None
            self.cod_act_txt.update() if self.cod_act_txt.page else None
            self.evid_txt.update() if self.evid_txt.page else None
            self.fecha_txt.update() if self.fecha_txt.page else None
            self.nota_txt.update() if self.nota_txt.page else None
            self.observacion_txt.update() if self.observacion_txt.page else None
            self.impr_check.update() if self.impr_check.page else None

            self.showModalDialog()
        except Exception as e:
            print(self.__class__,"setData",e)

    def edit(self):
        if(self.dataController != None):
            index = self.index_txt.value
            resp = self.dataController.edit_row(index,self.data)
            if(resp):
                self.showSuccessMsg("Registro editado!")
            else:
                self.showErrorMsg("Error!!! no se pudo editado el registro")
        else:
            print("edit datacontroller null")


    def save(self):
        if(self.dataController != None):

            resp, index = self.dataController.add_row(self.data)
            if(resp):
                self.index_txt.value = index
                self.showSuccessMsg("Registro añadido!")
            else:
                self.showErrorMsg("Error!!! no se pudo agrear el registro")
        else:
            print("save datacontroller null")

    def open_os(self,value):
        ruta = f"{self.page.session.get("RutaOrigen")}\\{value}"

        if(os.path.exists(ruta)):
            os.startfile(ruta)
            self.showSuccessMsg("Abriendo Ruta")
        else:
            self.showErrorMsg("Error!! Ruta Inexistente")
        print(ruta)


    def clear_data(self):
        self.index_txt .value=""
        self.fase_txt .value=""
        self.actividad_txt .value=""
        self.cod_act_txt .value=""
        self.evid_txt .value=""
        self.fecha_txt .value=""
        self.nota_txt .value=""
        self.observacion_txt .value=""
        self.impr_check .value=False


