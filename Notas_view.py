import flet as ft

class Notas_view(ft.Container):
    def __init__(self, page, **kwargs):
        super().__init__(**kwargs)
        
        self.page = page  # Guardamos el page para poder usarlo en la clase
        col = ft.Column()

        # Botón que abrirá el AlertDialog
        col.controls = [
            ft.Text("Non clickable"),
            ft.ElevatedButton("Mostrar diálogo", on_click=self.mostrar_alert)
        ]

        self.margin = 10
        self.padding = 10
        self.content = col

    def mostrar_alert(self, e):
        # Crear un AlertDialog
        self.alert = ft.AlertDialog(
            title=ft.Text("Título del diálogo"),
            content=ft.Text("Este es el contenido del diálogo."),
            actions=[
                ft.TextButton("Aceptar", on_click=self.cerrar_alert)
            ]
        )
        # Mostrar el diálogo
        self.page.overlay.append(self.alert)
        self.alert.open = True
        self.page.update()

    def cerrar_alert(self, e):
        # Cerrar el AlertDialog
        self.alert.open = False
        self.page.update()

# Código principal para cargar la vista
def main(page: ft.Page):
    vista = Notas_view(page)
    page.add(vista)

# Ejecutar la aplicación
ft.app(target=main)
