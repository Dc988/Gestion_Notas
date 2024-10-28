import pandas as pd
class DataController():
    def __init__(self, ruta,extencion):
        self.ruta_archivo = ruta
        self.extencion = extencion
    
    def read_file(self):
        try:
            self.document = None
            
            match(self.extencion):
                case ".xlsx":
                    self.document = pd.read_excel(self.ruta_archivo,dtype=str,header=0)
                case ".csv":
                    self.document = pd.read_csv(self.ruta_archivo,sep=";")
                case _:
                    pass
        except Exception:
            pass            
        return False if self.document is None else True
    
    
    def add_row(self, row):
        try:
            self.document = pd.concat([self.document, row], ignore_index=True)

        except Exception:
            return False
        return True

    def edit_row(self,index,row):
        self.document.loc[index] = row
        
    def drop_row(self, index):
        self.document = self.document.drop(index).reset_index(drop=True)
        








