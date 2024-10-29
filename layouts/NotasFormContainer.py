import flet as ft
from layouts.PanelContainer import PanelContainer

class Form(PanelContainer):
    def text_field(self):
        return ft.TextField(
            border_color="transparent",
            height=20,
            text_size=13,
            content_padding=0,
            cursor_color="black",
            cursor_width=1,
            cursor_height=18,
            color="black"
        )

    def text_field_container(self,expand:int|bool, name:str, control:ft.TextField):
        return ft.Container(
            expand=expand,
            height=50,
            bgcolor="#ebebeb",
            border_radius=6,
            padding=8,
            content=ft.Column(
                spacing=1,
                controls=[
                    ft.Text(
                        value=name,
                        size=9,
                        color="black",
                        weight="bold"
                    ),
                    control
                ]
            )
        )

    def __init__(self, dt=None):
        form_style={
            "border_radius":8,
            "border":ft.border.all(1,"#ebebeb"),
            "bgcolor":"white10",
            "padding":15
        }
        super().__init__(**form_style)
        self.datatable = dt
        self.r1_txt = self.text_field()
        self.r2_txt = self.text_field()
        self.r3_txt = self.text_field()
        self.r4_txt = self.text_field()

        self.r1= self.text_field_container(True,"Row 1",self.r1_txt)
        self.r2= self.text_field_container(True,"Row 2",self.r2_txt)
        self.r3= self.text_field_container(True,"Row 3",self.r3_txt)
        self.r4= self.text_field_container(True,"Row 4",self.r4_txt)

        self.submit = ft.ElevatedButton(
            text="Submit",
            style=ft.ButtonStyle(shape={"":ft.RoundedRectangleBorder(radius=8)})
            ,on_click=self.submit_data
        )

        self.clean = ft.ElevatedButton(
            text="Clear",
            style=ft.ButtonStyle(shape={"":ft.RoundedRectangleBorder(radius=8)})
            ,on_click=self.clear_data
        )

        self.content=ft.Column(
            expand=True,
            controls=[
                ft.Row(controls=[self.r1]),
                ft.Row(controls=[self.r2,self.r3]),
                ft.Row(controls=[self.r4]),
                ft.Row(controls=[self.submit,self.clean], alignment="end")
            ]
        )

    def submit_data(self,e):
        data = {"name":self.r1_txt.value,
                "description":self.r2_txt.value}
        #Controller.add(data)
        self.clear_data()
        #self.datatable.fill_items()
        
    def clear_data(self,e=None):
        self.r1_txt.value=""
        self.r2_txt.value=""
        self.r3_txt.value=""
        self.r4_txt.value=""
        self.content.update()