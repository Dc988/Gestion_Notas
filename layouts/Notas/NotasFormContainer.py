import flet as ft
import os
from datetime import datetime
import shutil as sh
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
        self.btn_open_pdf = ft.IconButton(
                                icon=ft.Icons.PICTURE_AS_PDF,
                                on_click=lambda _:self.open_os(f"{self.fase_txt.value}\\{self.actividad_txt.value}\\Guia_aprendizaje.pdf")
                            )

        self.btn_create_file = ft.IconButton(
                                icon=ft.Icons.FILE_COPY,
                                on_click=lambda _:self.copy_file_evi(origen="Format.docx",
                                                                     to=f"{self.fase_txt.value}\\{self.actividad_txt.value}\\{self.cod_act_txt.value}\\{self.evid_txt.value}\\{self.evid_txt.value}.docx")
                            )

        self.btn_open_folder_fase = ft.IconButton(
                                        icon=ft.Icons.FOLDER,
                                        on_click= lambda _: self.open_os(self.fase_txt.value)
                                    )
        
        self.btn_open_folder_act=ft.IconButton(
                                        icon=ft.Icons.FOLDER,
                                        on_click=lambda _:self.open_os(f"{self.fase_txt.value}\\{self.actividad_txt.value}")
                                    )

        self.btn_open_folder_cod_act = ft.IconButton(
                                        icon=ft.Icons.FOLDER,
                                        on_click=lambda _:self.open_os(f"{self.fase_txt.value}\\{self.actividad_txt.value}\\{self.cod_act_txt.value}")
                                    )

        self.btn_open_folder_evi = ft.IconButton(
                                        icon=ft.Icons.FOLDER,
                                        on_click=lambda _:self.open_os(f"{self.fase_txt.value}\\{self.actividad_txt.value}\\{self.cod_act_txt.value}\\{self.evid_txt.value}")
                                    )
        
        col=ft.Row([
                ft.NavigationRail(
                    selected_index=0,
                    label_type=ft.NavigationRailLabelType.NONE,
                    width=40,
                    min_extended_width=400,
                    leading=ft.Column([
                            self.btn_open_pdf,
                            self.btn_create_file
                        ]),
                    group_alignment=-0.9,
                    destinations=[ft.NavigationRailDestination(disabled=True)]
                ),
                ft.VerticalDivider(width=1),
                ft.Column(
                    width=1100,
                    controls=[
                            ft.Row(controls=[
                                self.component_container(
                                    expand=True,name="FASE",
                                    control=self.fase_txt,
                                    icon =ft.Icons.TEXT_FIELDS,
                                    trailing= self.btn_open_folder_fase),
                                self.component_container(
                                    expand=True,name="ACTIVIDAD",
                                    control=self.actividad_txt,
                                    icon =ft.Icons.TEXT_FIELDS,
                                    trailing= self.btn_open_folder_act),
                            
                                self.component_container(
                                    expand=True,name="CODIGO ACTIVIDAD",
                                    control=self.cod_act_txt,
                                    icon =ft.Icons.CODE,
                                    trailing= self.btn_open_folder_cod_act ),
                            ]),
                            ft.Row(controls=[
                                self.component_container(
                                    expand=True,name="EVIDENCIA",
                                    control=self.evid_txt,
                                    icon =ft.Icons.BOOK,
                                    trailing=self.btn_open_folder_evi),
                            ]),
                            
                            ft.Row(controls=[
                                self.component_container(
                                    expand=True,name="NOTA",
                                    control=self.nota_txt,
                                    icon =ft.Icons.NOTES),

                                self.component_container(
                                    expand=True,name="FECHA",
                                    control=self.fecha_txt,
                                    icon =ft.Icons.CALENDAR_MONTH,
                                    trailing=ft.IconButton(
                                        icon=ft.Icons.REMOVE_RED_EYE,
                                        on_click=lambda _:self.page.open(
                                            self.dt
                                        )
                                    )),
                                
                                self.component_container(
                                    expand=True,name="IMPORTANTE",
                                    control=self.impr_check,
                                    icon =ft.Icons.LABEL_IMPORTANT),
                            ]),
                            ft.Row(controls=[
                                self.component_container(
                                            expand=True,name="OBSERVACION",
                                            control=self.observacion_txt,
                                            icon =ft.Icons.MENU_OPEN),
                                ])                                
                            
                    ]
                )
            ],
            expand=True
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
        now = datetime.now()

        self.dt = ft.DatePicker(
                    first_date=datetime(year=2000, month=1, day=1),
                    last_date=datetime(year=now.year, month=now.month, day=now.day),
                    on_change=self.handle_change
                )
    def set_btn_states(self):
        route = f"{self.fase_txt.value}\\{self.actividad_txt.value}\\Guia_aprendizaje.pdf"
        self.validate_route(self.btn_open_pdf,route)

        route = f"{self.fase_txt.value}\\{self.actividad_txt.value}\\{self.cod_act_txt.value}\\{self.evid_txt.value}\\{self.evid_txt.value}.docx"
        self.validate_route(self.btn_create_file,route)

        route = self.fase_txt.value
        self.validate_route(self.btn_open_folder_fase,route)
        
        route = f"{self.fase_txt.value}\\{self.actividad_txt.value}"
        self.validate_route(self.btn_open_folder_act,route)

        route = f"{self.fase_txt.value}\\{self.actividad_txt.value}\\{self.cod_act_txt.value}"
        self.validate_route(self.btn_open_folder_cod_act,route)

        route = f"{self.fase_txt.value}\\{self.actividad_txt.value}\\{self.cod_act_txt.value}\\{self.evid_txt.value}"
        self.validate_route(self.btn_open_folder_evi,route)
        
    def validate_route(self,btn,route):
        print(btn.icon_color)
        route = f"{self.page.session.get("RutaOrigen")}\\{route}"
        btn.icon_color= "ffffff" if os.path.exists(route) else ft.Colors.RED
        btn.update() if btn.page else None
   
    def handle_change(self,e):
        self.fecha_txt.value =e.control.value.strftime('%Y-%m-%d')

        self.fecha_txt.update() if self.fecha_txt.page else None

    def onYesOption(self):
        self.showLoadingSheetMsg()

        if(
            self.fase_txt .value=="" or
            self.actividad_txt .value=="" or
            self.cod_act_txt .value=="" or
            self.evid_txt .value=="" ):
                self.showBottomSheetMsg("Campos obligatorios!!!",ft.Icons.INFO)
        else:
            
            self.data = {
                "FASE":self.fase_txt .value.upper(),
                "ACTIVIDAD":self.actividad_txt .value.upper(),
                "CODIGO ACTIVIDAD":self.cod_act_txt .value.upper(),
                "EVIDENCIA":self.evid_txt .value.upper(),
                "FECHA": "NO HECHO" if self.fecha_txt.value =="" else self.fecha_txt .value.upper(),
                "NOTA": "--" if self.nota_txt .value =="" else self.nota_txt.value.upper(),
                "OBSERVACION":self.observacion_txt .value.upper(),
                "IMPORTANTE":"SI"  if self.impr_check.value else "NO"
            }

            if (self.index_txt.value==""):
                self.save()
            else:
                self.edit()

            if (self.dataTable is not None):
                self.dataTable.setDataTable()
            else:
                self.showBottomSheetMsg("Error!!! no se pudo actualizar la tabla",ft.Icons.ERROR)


        
    def setData(self, data):
        try:
            self.clear_data()
            
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

            self.set_btn_states()
            self.showModalDialog()
        except Exception as e:
            print(self.__class__,"setData",e)

    def edit(self):
        if(self.dataController != None):
            index = self.index_txt.value
            resp = self.dataController.edit_row(index,self.data)
            if(resp):
                self.showBottomSheetMsg("Registro editado!",ft.Icons.THUMB_UP)
            else:
                self.showBottomSheetMsg("Error!!! no se pudo editado el registro",ft.Icons.ERROR)
        else:
            print("edit datacontroller null")


    def save(self):
        if(self.dataController != None):

            resp, index = self.dataController.add_row(self.data)
            if(resp):
                self.index_txt.value = index
                self.showBottomSheetMsg("Registro añadido!",ft.Icons.THUMB_UP)
            else:
                self.showBottomSheetMsg("Error!!! no se pudo agrear el registro",ft.Icons.ERROR)
        else:
            print("save datacontroller null")

    def open_os(self,value):
        self.showLoadingSheetMsg()
        ruta = f"{self.page.session.get("RutaOrigen")}\\{value}"

        print(ruta)
        if(os.path.exists(ruta)):
            os.startfile(ruta)
            self.showBottomSheetMsg("Abriendo Ruta",ft.Icons.THUMB_UP)
        else:
            self.showBottomSheetOption("Ruta no existe, desea crear una?",lambda r = ruta: self.create_folder(r))
        self.closeLoadingSheetMsg()

    def create_folder(self,ruta):
        try:
            self.showLoadingSheetMsg()
            os.makedirs(ruta)
            os.startfile(ruta)
            self.showBottomSheetMsg("Abriendo Ruta",ft.Icons.THUMB_UP)
            self.set_btn_states()
        except Exception as ex:
            self.showBottomSheetMsg("Error al crear la carpeta",ft.Icons.ERROR)
            print(ex)


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

        self.evid_txt.on_submit = self.evidencia_on_submit

    def copy_file_evi(self,origen, to):
        def copy():
            if (os.path.exists(origen)):
                self.showLoadingSheetMsg()

                if(os.path.exists(to)):
                    self.showBottomSheetMsg(f"Ya hay un formato creado",ft.Icons.INFO)
                else:
                    try:
                        sh.copy(origen, to)
                        self.showBottomSheetMsg("Archivo creado correctamente",ft.Icons.INFO)
                        self.set_btn_states()
                    except Exception as e:
                        self.showBottomSheetMsg("Error! No se pudo crear el Archivo",ft.Icons.ERROR)
                        print(e)



            else:
                self.showBottomSheetMsg(f"Plantilla no existe",ft.Icons.ERROR)

            
        origen = f"{self.page.session.get("RutaOrigen")}\\{origen}"
        to = f"{self.page.session.get("RutaOrigen")}\\{to}"

        self.showBottomSheetOption("Desea generar el formato de la evidencia?",copy)


        

    def evidencia_on_submit(self,e):
        def get_cod_evi(evidencia):
            return evidencia[:evidencia.find("-EV")] if evidencia.find("-EV") != -1 else None

        def get_activity(cod):
            try:
                
                inicio = 2  # Corresponde al índice 3 en Excel (base 1)
                longitud = cod.find("-") - inicio
                extraido = cod[inicio:inicio + longitud]
                resultado_si_error = f"P{extraido}"
            except Exception:
                resultado_si_error = None

            return resultado_si_error

        def get_fase(texto_mapeo):
            # Diccionario de equivalencias
            cambiar = {
                "P1": "01. ANALISIS",
                "P2": "01. ANALISIS",
                "P3": "02. PLANEACION",
                "P4": "02. PLANEACION",
                "P5": "02. PLANEACION",
                "P6": "03. EJECUCIÓN",
                "P7": "03. EJECUCIÓN",
                "P8": "03. EJECUCIÓN",
                "P9": "04. EVALUACION"
            }

            return cambiar.get(texto_mapeo, None) 

        evi = e.data

        evi = get_cod_evi(evi)
        self.cod_act_txt.value = evi

        evi = get_activity(evi)
        self.actividad_txt.value = evi

        evi = get_fase(evi)
        self.fase_txt.value = evi

        self.fase_txt.update()  if self.fase_txt.page else None
        self.actividad_txt.update() if self.actividad_txt.page else None
        self.cod_act_txt.update() if self.cod_act_txt.page else None






