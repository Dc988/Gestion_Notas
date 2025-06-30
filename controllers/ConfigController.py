import json
import os
class ConfigController():
    def __init__(self):
        
        r1 ='_internal/controllers/Data_Config.json'
        r2='controllers/Data_Config.json'
        self.archivo = r1 if os.path.exists(r1) else  r2 
       
    def read_document(self):
        datos = None
        if(os.path.exists):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
            except Exception as e:
                print(self.__class__,"read_document",e)
        else:
            print(self.__class__,"read_document","File not exists")

        return datos
    
    def edit_json(self,data):
        datos = self.read_document()
        
        if datos is not None:
            datos.update(data)
            
            try:
                with open(self.archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)
                return True
            except Exception as e:
                print(self.__class__,"edit_json",e)
        return False




