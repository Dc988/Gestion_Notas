
import flet as ft
class PanelContainer(ft.Container):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.dlg_modal=None
      self.bs =None
      self.modal = None
      self.alert = None
      self.bsmsg =None

      self.textError = ft.Text(color=ft.colors.RED)
      self.error = ft.Row(expand=True,wrap=False, visible=False, controls=[
               ft.Icon(ft.icons.ERROR,color=ft.colors.RED),
               self.textError
      ])

      self.textSuccess = ft.Text(color=ft.colors.GREEN)
      self.success = ft.Row(expand=True,wrap=False, visible=False, controls=[
               ft.Icon(ft.icons.THUMB_UP,color=ft.colors.GREEN),
               self.textSuccess
      ])
      
   def showBottomSheetMsg(self,text:str,icon:ft.icons=None):
      try:
         self.bsmsg = ft.BottomSheet(
      
         content=ft.Container(
               bgcolor="#f2f0f0",
               padding=50,
               border_radius=6,
               content=ft.Column(
                  tight=True,
                  controls=[ft.Row([self.defineIcon(icon),ft.Text(text,size=20,no_wrap=False,weight=ft.FontWeight.BOLD)])]
               ),
         ),
         )
         self.page.open(self.bsmsg)
      except Exception:
         pass


      pass
   def showBottomSheetOption(self,text:str,YesOption:callable=None,NoOption:callable =None):
      def onYesOption(e):
         if YesOption is not None:
            YesOption()
            self.close_alert(e)
         else:
            self.close_alert(e)
      
      def onNoOption(e):
         if NoOption !=None:
            NoOption()
         
         self.close_alert(e)

      self.bs = ft.BottomSheet(
        dismissible=False,
        content=ft.Container(
            bgcolor="#f2f0f0",
            padding=50,
            border_radius=6,
            content=ft.Column(
                tight=True,
                controls=[]
            ),
        ),
      )
      self.bs.content.content.controls=[
                    ft.Text(text,size=15,weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.ElevatedButton("Cancelar",icon =ft.icons.CLOSE,icon_color=ft.colors.RED, on_click=onNoOption,data=self.bs),
                        ft.ElevatedButton("Aceptar",icon =ft.icons.CHECK,icon_color=ft.colors.GREEN, on_click=onYesOption,data=self.bs)
                    ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)                    
                ]
      self.page.open(self.bs)


   def showAlertDialog(self,title:str,content:str,icon:ft.icons=None):
      try:
         self.alert = ft.AlertDialog(
            title= ft.Text(title),
            content=ft.Text(content),
            icon=self.defineIcon(icon),
         )

         self.alert.actions=[
            ft.TextButton("Aceptar", on_click=self.close_alert,data=self.alert)
         ]
         
         self.page.open(self.alert)
      except Exception as ex:
         print(self.__class__,"showAlertDialog",ex)
   
   def setModalDialog(self,title:str,content:ft.Control,YesOption:callable,NoOption:callable =None):
      def onYesOption(e):
         if YesOption is not None:
            if(YesOption()):
               self.close_alert(e)
         else:
            self.close_alert(e)
      
      def onNoOption(e):
         if NoOption !=None:
            NoOption()
         
         self.close_alert(e)
      
      content.controls.extend([self.error,self.success])

      self.modal = ft.AlertDialog(
         modal=True,
         title= ft.Text(title,size=15,weight="bold"),
         content=content,
         actions_alignment=ft.MainAxisAlignment.END)
      
      self.modal.actions=[
         ft.TextButton("Aceptar", on_click=onYesOption,data=self.modal),
         ft.TextButton("Cancelar", on_click=onNoOption,data=self.modal),
      ]
      self.page.overlay.append(self.modal)  # Asegúrate de que se agregue al árbol de la página.


   def showModalDialog(self):
      try:
        self.page.open(self.modal)
      except Exception as ex:
         print(self.__class__,"showModalDialog",ex)
         pass
      

   def showErrorMsg(self, text=None):
      if(text!=None):
         self.error.visible = True
         self.textError.value = text
      else:
         self.error.visible = False
         self.textError.value = ""

      if self.error.page is not None:
         self.error.update()
         self.textError.update()

   def showSuccessMsg(self, text=None):
      if(text!=None):
         self.success.visible = True
         self.textSuccess.value = text
      else:
         self.success.visible = False
         self.textSuccess.value = ""

      if self.success.page is not None:
         self.success.update()
         self.textSuccess.update()

   def showOptionDialog(self,title,YesOption,NoOption=None,icon:ft.icons=None,data=None):
      def onNoOption(e):
         if NoOption !=None:
            NoOption()
         self.close_alert(e)

      def onYesOption(e):
         YesOption(data) if data is not None else YesOption()
         self.close_alert(e)

      
      self.dlg_modal = ft.AlertDialog(
         modal=True,
         title= ft.Text(title),
         icon=self.defineIcon(icon),
         actions_alignment=ft.MainAxisAlignment.END)
      
      self.dlg_modal.actions=[
         ft.TextButton("Aceptar", on_click=onYesOption, data = self.dlg_modal),
         ft.TextButton("Cancelar", on_click=onNoOption, data = self.dlg_modal),
      ]

      self.page.open(self.dlg_modal)
   
   def defineIcon(self,icon):
      
      match(icon):
         case ft.icons.WARNING:
              color = ft.colors.AMBER
         case ft.icons.INFO:
            color = ft.colors.BLUE
         case ft.icons.CHECK:
            color = ft.colors.GREEN
         case ft.icons.ERROR:
            color = ft.colors.RED
         case ft.icons.THUMB_UP:
            color = ft.colors.GREEN
         case _:
            color= None

      return ft.Icon(name=icon, color=color,size=80) if icon !=None else None
          
   def close_alert(self, e):
        self.page.close(e.control.data)
   
   def component_container(self,expand:bool, name:str, control=None,trailing=None,icon=None):
        return ft.Container(
            
            
            bgcolor="#f2f0f0",
            border_radius=6,
            padding=8,
            expand=expand,
            content=ft.CupertinoListTile(
               
                leading=ft.Icon(name=icon),
                title=ft.Text(name),                
                subtitle=control,
                trailing=trailing)
        )
   
   def textfield(self):
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