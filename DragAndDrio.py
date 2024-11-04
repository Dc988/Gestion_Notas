import flet as ft

def main(page: ft.Page):
    
    page.title = "Drag and Drop example"
    page.theme_mode=ft.ThemeMode.LIGHT
    
    def getContainer(controls):
        return ft.Container(
                padding=5, 
                border=ft.border.all(2,"#ebebeb"),
                border_radius=5,
                alignment=ft.alignment.center,
                content= ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    width=300,
                    height=200,
                    controls=controls
                    ))

    def add_dragtarget_item(text):
        def on_click(e):
            target = e.control.data
            target.visible =True
            e.control.visible =False
            page.update()

        return ft.ElevatedButton(
                bgcolor="#ebebeb",
                text =text,
                width=300,
                visible=False,
                on_click=on_click
                             )
    

    def add_draggle_item(index,text):
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
    
    def drag_accept(e):
        # get draggable (source) control by its ID
        src = page.get_control(e.src_id)
      
        index = src.data

        #DragTarget
        btn = e.control.content.content.controls[index]
        btn.data = src
        btn.visible=True
        src.visible=False

        page.update()


    columns = [1,2,3,4,5,6]
    p2 = getContainer(
        controls=[add_dragtarget_item(item) for index,item in enumerate(columns)]
        )
    
    p1 =getContainer(
            controls=[add_draggle_item(index,item) for index,item in enumerate(columns)]
    )

    def p(e):
        for btn in p2.content.controls:
            print(btn.text) if btn.visible else None
        
    page.add(
        ft.Row(
            [
                p1,
                ft.DragTarget(
                            group="str",
                            content=p2,
                            on_accept=drag_accept,
                        ),
            ]
        ),
        ft.TextButton(
                text ="aceptar",
                width=500,
                visible=True,
                on_click=p
                             )
    )

ft.app(main)