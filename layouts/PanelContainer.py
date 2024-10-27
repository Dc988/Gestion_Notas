
import flet as ft
class PanelContainer(ft.Container):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)
      
   def showAlertDialog(self,title,content,icon:ft.icons=None):
      self.alert = ft.AlertDialog(
         title= ft.Text(title),
         content=ft.Text(content),
         icon=self.defineIcon(icon),
      )

      self.alert.actions=[
         ft.TextButton("Aceptar", on_click=self.close_alert,data=self.alert)
      ]
      
      self.page.open(self.alert)
      
   def showOptionDialog(self,title,YesOption,icon:ft.icons=None):
      
      def onYesOption(e):
         YesOption()
         self.close_alert(e)
      
      self.dlg_modal = ft.AlertDialog(
         modal=True,
         title= ft.Text(title),
         icon=self.defineIcon(icon),
         actions_alignment=ft.MainAxisAlignment.END)
      
      self.dlg_modal.actions=[
         ft.TextButton("Aceptar", on_click=onYesOption,data=self.dlg_modal),
         ft.TextButton("Cancelar", on_click=self.close_alert,data=self.dlg_modal),
      ]

      self.page.open(self.dlg_modal)
   
   def defineIcon(self,icon):
      
      match(icon):
         case ft.icons.WARNING:
              color = ft.colors.AMBER
         case ft.icons.INFO:
            color = ft.colors.LIGHT_BLUE
         case ft.icons.CHECK:
            color = ft.colors.GREEN
         case ft.icons.ERROR:
            color = ft.colors.RED
         case _:
            color= None

      return ft.Icon(name=icon, color=color,size=80) if icon !=None else None
          
   def close_alert(self, e):
        self.page.close(e.control.data)