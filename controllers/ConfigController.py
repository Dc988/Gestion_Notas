import json

class ConfigController():
    def __init__(self):
        self.archivo = 'controllers/Data_Config.json'
       
    def read_document(self):
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            return datos
        except Exception as e:
            return None
    
    def edit_json(self,data):
        datos = self.read_document()
        
        if datos is not None:
            datos.update(data)
            
            try:
                with open(self.archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)
                return True
            except Exception as e:
                pass
        return False




