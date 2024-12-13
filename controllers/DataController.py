import pandas as pd
import os

class DataController():
    def __init__(self, ruta):
        nombre, extension = os.path.splitext(ruta)
        self.ruta_archivo = ruta
        self.extencion = extension
        self._document = None
        self.data = None
 
        
    def read_file(self):
        try:
            self._document = None
            
            match(self.extencion):
                case ".xlsx":
                    self._document = pd.read_excel(self.ruta_archivo,dtype=str,header=0)
                case ".csv":
                    self._document = pd.read_csv(self.ruta_archivo,sep=";")
                case _:
                    pass
            self.initializeFrame()       
        except Exception as e:
            print(self.__class__,"read_file",e)

        return False if self._document is None else True

    def initializeFrame(self):
        if self._document is not None:
            self._document.fillna("--", inplace=True)
            self._document.sort_index(ascending=False,inplace=True)

    def setDataFrame(self):
        self.data = self._document
        return self
        
    def getColumns(self):
        data = self.getData()

        return data.columns
    
    def getData(self):
        
        return self._document if self.data is None else self.data
    
    def selectColumns(self,colums):
        data = self.getData()
        
        try:
            self.initializeFrame()
            self.data = data[colums]
        except Exception as ex:
            print(self.__class__,"getDataByColumns",ex)

        return self
    
    def setFilter(self, filter: dict):
        data = self.getData()
        if data is not None:
            try:
                for columna, valores in filter.items():
                    data = data[data[columna].astype(str).str.startswith(tuple(valores), na=True)]
                self.data = data
            except Exception as e:
                print(self.__class__, "setFilter", e)
        return self

    

    def getLen(self):
        data = self.getData()
        lenData = -1
        if data is not None:
            lenData = len(data)

        return lenData
    
    def getRow(self,index):
        try:
            data = self.getData()

            data = data.loc[index] 

        except Exception as e:
            print(self.__class__,"getRow",e)
            
        return data

    def add_row(self, row):
        try:
            band=False
            index = -1
            if(self.getLen()>=0):
                index = self.getLen()
                self._document.loc[index] = row
                band = True

        except Exception as e:
            print(self.__class__,"add_row",e)
            
            return False
        
        return band,index



    def edit_row(self,index:int,row:dict):
        try:
            self._document.loc[index] = row

        except Exception as e:
            print(self.__class__,"edit_row",e)
            return False
        return True
        
    def drop_row(self, index:int):
        try:
            self._document = self._document.drop(index).reset_index(drop=True)

        except Exception as e:
            print(self.__class__,"drop_row",e)
            return False
        return True
    
    def exportDataFrame(self):
        try:
            self._document.to_excel(self.ruta_archivo, sheet_name="Hoja 1", index = False)
            band = True
            
        except Exception as e:
            print(self.__class__,"exportDataFrame",e)

            band = False
        return band


print("Empezando")
d = DataController( "c:\\Users\\dicma\\Documents\\Seguimiento de notas.xlsx")

if (d.read_file()):
    data = d.setDataFrame().getData()

    print(data)
else:
    print("error")