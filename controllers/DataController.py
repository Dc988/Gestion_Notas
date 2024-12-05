import pandas as pd
import os

class DataController():
    def __init__(self, ruta):
        nombre, extension = os.path.splitext(ruta)
        self.ruta_archivo = ruta
        self.extencion = extension
 
        
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
            self.document.sort_index(ascending=False,inplace=True)

    def getColumns(self):
        return self.document.columns
    
    def getData(self):
        self.initializeFrame()
        return self.document
    
    def getDataByColumns(self,colums):
        data = None
        
        try:
            self.initializeFrame()
            data = self.document[colums]
        except Exception as ex:
            print(self.__class__,"getDataByColumns",ex)

        return data
    
    def setFilter(self, filter: dict):
        data = None
        if self.document is not None:
            try:
                self.initializeFrame()
                data = self.document
                for columna, valores in filter.items():

                    data = data[data[columna].astype(str).str.startswith(tuple(valores), na=False)]
            except Exception as e:
                print(self.__class__, "setFilter", e)
        return data

    

    def getLen(self):
        lenData = -1
        if self.document is not None:
            lenData = len(self.document)

        return lenData
    
    def getRow(self,index):
        try:
            data = None
            data = self.document.loc[index] 

        except Exception as e:
            print(self.__class__,"getRow",e)
            
        return data

    def add_row(self, row):
        try:
            band=False
            index = -1
            if(self.getLen()>=0):
                index = self.getLen()
                self.document.loc[index] = row
                band = True

        except Exception as e:
            print(self.__class__,"add_row",e)
            
            return False
        
        return band,index



    def edit_row(self,index:int,row:dict):
        try:
            self.document.loc[index] = row

        except Exception as e:
            print(self.__class__,"edit_row",e)
            return False
        return True
        
    def drop_row(self, index:int):
        try:
            self.document = self.document.drop(index).reset_index(drop=True)

        except Exception as e:
            print(self.__class__,"drop_row",e)
            return False
        return True
    
    def exportDataFrame(self):
        try:
            self.document.to_excel(self.ruta_archivo, sheet_name="Hoja 1", index = False)
            band = True
            
        except Exception as e:
            print(self.__class__,"exportDataFrame",e)

            band = False
        return band


