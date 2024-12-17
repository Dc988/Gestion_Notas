
import flet as ft
class PanelContainer(ft.Container):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)

      self.dlg_modal=None
      self.modal = None
      self.alert = None
      self.loadAlert = ft.AlertDialog(
         modal=True,
         title=ft.Text("",size=20,no_wrap=False,weight=ft.FontWeight.BOLD),
         content=ft.Row([ft.ProgressRing(),ft.Text("Cargando...",size=20,no_wrap=False,weight=ft.FontWeight.BOLD)])
      )
   
      self.bs =None
      self.bsmsg =None
      self.bslmsg = ft.BottomSheet(
         dismissible=False,
         content=ft.Container(
               bgcolor="#f2f0f0",
               padding=50,
               border_radius=6,
               content=ft.Column(
                  tight=True,
                  controls=[ft.Row([ft.ProgressRing(),ft.Text("Cargando...",size=20,no_wrap=False,weight=ft.FontWeight.BOLD)])]
               ),
         ),
      )


   def showLoadingSheetMsg(self):
      try:

         
         self.page.open(self.bslmsg)
      except Exception:
         pass

   def closeLoadingSheetMsg(self):
      try:        
         if ((self.bslmsg is not None) and self.bslmsg.visible):
            self.page.close(self.bslmsg)
      except Exception:
         pass

   def showBottomSheetMsg(self,text:str,icon:ft.Icons=None):
      try:
         self.closeLoadingSheetMsg()
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

      self.closeLoadingSheetMsg()

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
                        ft.ElevatedButton("Cancelar",icon =ft.Icons.CLOSE,icon_color=ft.Colors.RED, on_click=onNoOption,data=self.bs),
                        ft.ElevatedButton("Aceptar",icon =ft.Icons.CHECK,icon_color=ft.Colors.GREEN, on_click=onYesOption,data=self.bs)
                    ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)                    
                ]
      self.page.open(self.bs)


   def showLoadingDialog(self):
      try:
         self.page.open(self.loadAlert)
      except Exception as ex:
         print(self.__class__,"showAlertDialog",ex)

   def closeLoadingDialog(self):
      try:        
         if ((self.loadAlert is not None) and self.loadAlert.visible):
            self.page.close(self.loadAlert)
      except Exception:
         pass

   def showAlertDialog(self,title:str,content:str,icon:ft.Icons=None):
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
      

   

   def showOptionDialog(self,title,YesOption,NoOption=None,icon:ft.Icons=None,data=None):
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
         case ft.Icons.WARNING:
              color = ft.Colors.AMBER
         case ft.Icons.INFO:
            color = ft.Colors.BLUE
         case ft.Icons.CHECK:
            color = ft.Colors.GREEN
         case ft.Icons.ERROR:
            color = ft.Colors.RED
         case ft.Icons.THUMB_UP:
            color = ft.Colors.GREEN
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
