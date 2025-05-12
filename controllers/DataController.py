import pandas as pd
import os
from controllers.ConfigController import ConfigController

class DataController():

    _instance = None

    def __init__(self):
         
        self.config = ConfigController()
        self.config.archivo = 'controllers/Data_Base.json'

        self._document = None
        self.data = None
    
    def read_file(self):
        try:
            self._document = None
            
            data = self.config.read_document()
    
            if(data != {}):
                self._document = pd.DataFrame(data)
                data = self.getRow(0)
        
                if (not len(data)):
                    self.drop_row(0)
                
                self.initializeFrame()          
            else:
                self._document = pd.DataFrame()       

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
        col =None
        if data is not None:
            col = data.columns
        return col
    
    def getData(self):
        
        return self._document if self.data is None else self.data
    
    def selectColumns(self,colums):
        data = self.getData()
        if data is not None:
            try:
                self.initializeFrame()
                
                #self.data = data[colums]
            except Exception as ex:
                print(self.__class__,"selectColumns",ex)

        return self
    
    def setFilter(self, filter: dict):
        print(filter)
        data = self.getData()
        if data is not None:
            try:
                for columna, options in filter.items():
                    for tipo, valores in options.items():
                                                
                        if tipo == "igual a":
                            data =  data[data[columna].isin(valores)]
                        
                        elif tipo == "no igual":
                            data =  data[~data[columna].isin(valores)]
                        
                        elif tipo == "contiene":
                            data =  data[data[columna].astype(str).apply(lambda x: any(val in x for val in valores))]
                        
                        elif tipo == "no contiene":
                            data =  data[~data[columna].astype(str).apply(lambda x: any(val in x for val in valores))]
                        
                        elif tipo == "empieza":
                            data =  data[data[columna].astype(str).apply(lambda x: any(x.startswith(val) for val in valores))]
                        
                        elif tipo == "no empieza":
                            data =  data[~data[columna].astype(str).apply(lambda x: any(x.startswith(val) for val in valores))]
                        
                        elif tipo == "termina":
                            data =  data[data[columna].astype(str).apply(lambda x: any(x.endswith(val) for val in valores))]
                        
                        elif tipo == "no termina":
                            data =  data[~data[columna].astype(str).apply(lambda x: any(x.endswith(val) for val in valores))]
                        
                        else:
                            print(f"Operación no soportada: {tipo}")
                
                self.data = data
            except Exception as e:
                print(self.__class__, "setFilter", e)
        return self

    def setOrder(self,order:bool, column:str):
        data = self.getData()
        if data is not None:
            
            if column.upper() == "INDEX":
                data.sort_index(ascending=order,inplace=True)
            else:
                data.sort_values(by=column.upper(),ascending=order,inplace=True)
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
            row = pd.DataFrame([row])
            index = -1
            if(self.getLen()>=0):
                index = self.getLen()

                self._document = pd.concat([self._document,row],ignore_index=True)
                band = True

        except Exception as e:
            print(self.__class__,"add_row",e)
                
        return band,index



    def edit_row(self,index:int,row:dict):
        try:
            band = True
            self._document.loc[index] = row

        except Exception as e:
            print(self.__class__,"edit_row",e)
            band = False
        return band
        
    def drop_row(self, index:int):
        try:
            band = True
            self._document = self._document.drop(index).reset_index(drop=True)

        except Exception as e:
            print(self.__class__,"drop_row",e)
            band = False

        return band
    
    def saveDataFile(self):
        try:
            data = None
            band = True

            data = self._document.to_dict(orient="list")
            self.config.edit_json(data)
        except Exception as e:
            print(self.__class__,"saveDataFile",e)

            band = False
        return band
    
    def importDataFrame(self,ruta_archivo):
        try:
            _, extencion = os.path.splitext(ruta_archivo)
            data = None
            band = True

            match(extencion):
                case ".xlsx":
                    data = pd.read_excel(ruta_archivo,dtype=str,header=0)
                case ".csv":
                    data = pd.read_csv(ruta_archivo,sep=";")
                case _:
                    pass
            
            if data is not None:
                self._document = pd.concat([self._document,data],ignore_index=True)
                self.initializeFrame()
                self.saveDataFile()         
            
        except Exception as e:
            print(self.__class__,"exportDataFrame",e)
            band = False

        return band
        
    def exportDataFrame(self,ruta_archivo):
        try:
            band = False

            if self.read_file():
                self._document.to_excel(ruta_archivo, sheet_name="Hoja 1", index = False)
                band = True
            
            
        except Exception as e:
            print(self.__class__,"exportDataFrame",e)

            band = False
        return band

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataController, cls).__new__(cls)
        return cls._instance
"""
print("Empezando")
d = DataController()
ruta = "c:\\Users\\dicma\\Documents\\Seguimiento de notas.xlsx"
row1 = {
            "FASE": "fase_txt 1",
            "ACTIVIDAD": "actividad_txt 1",
            "CODIGO ACTIVIDAD": "cod_act_txt 1",
            "EVIDENCIA": "evid_txt 1",
            "FECHA": "fecha_txt 1",
            "NOTA": "nota_txt 1",
            "OBSERVACION": "observacion_txt 1",
            "IMPORTANTE": "impr_check1",
        }
row2 = {
            "FASE": "fase_txt 2",
            "ACTIVIDAD": "actividad_txt 2",
            "CODIGO ACTIVIDAD": "cod_act_txt 2",
            "EVIDENCIA": "evid_txt 2",
            "FECHA": "fecha_txt 2",
            "NOTA": "nota_txt 2",
            "OBSERVACION": "observacion_txt 2",
            "IMPORTANTE": "impr_check2",
        }
row3 = {
            "FASE": "fase_txt 3",
            "ACTIVIDAD": "actividad_txt 3",
            "CODIGO ACTIVIDAD": "cod_act_txt 3",
            "EVIDENCIA": "evid_txt 3",
            "FECHA": "fecha_txt 3",
            "NOTA": "nota_txt 3",
            "OBSERVACION": "observacion_txt 3",
            "IMPORTANTE": "impr_check3",
        }

if (d.read_file()):

    #d.add_row(row1)
    #d.add_row(row3)
    print(d.importDataFrame(ruta))
    print(d.getData())
    d.saveDataFile()
    
else:
    print("error")

#"""
