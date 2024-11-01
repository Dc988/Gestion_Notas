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
            self.initializeFrame()       
        except Exception as e:
            print(self.__class__,"read_file",e)

        return False if self.document is None else True

    def initializeFrame(self):
        if self.document is not None:
            self.document.fillna("", inplace=True)
            self.document.sort_values(by="index",ascending=False)

    def getColumns(self):
        return self.document.columns
    
    def getData(self):
        return self.document
    
    def setFilter(self, filter:dict):
        data = None 
        if self.document is not None:
            try:
                data = self.document
                for columna, valores in filter.items():
                    data = data[data[columna].isin(valores)]
                
            except Exception as e:
                print(self.__class__,"setFilter",e)
        return data

    def add_row(self, row):
        try:
            self.document = pd.concat([self.document, row], ignore_index=True)

        except Exception as e:
            print(self.__class__,"add_row",e)
            
            return False
        return True

    def edit_row(self,index,row):
        self.document.loc[index] = row
        
    def drop_row(self, index):
        self.document = self.document.drop(index).reset_index(drop=True)



