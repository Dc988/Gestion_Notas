from controllers.Model.Model import Model
import pandas as pd


class DataController:
    _instance = None
    # se inicializa variables globales
    def __init__ (self,page):
        self.evidencia = Model(table="EVIDENCIA",ruta="controllers/Model/query.sql")
        self.actividad = Model(table="ACTIVIDAD")
        self.cod_actividad = Model(table="COD_ACTIVIDAD")
        self.fase = Model(table="FASE")

        self.order=["EVIDENCIA.ID","DESC"]
        self.page = page
        # columnas obligatorias
        
        self.table_cols = ["EVIDENCIA.ID"] + self.page.session.get("visibleColumns") 
        self.columns_valid=["FASE","ACTIVIDAD","CODIGO_ACTIVIDAD", "EVIDENCIA", "FECHA", "NOTA", "OBSERVACION", "IMPORTANTE"]
    
    
    def valid_columns(self,cols):
        cols = all(key in cols for key in self.columns_valid)
        return cols

    def import_data(self,ruta):
                
        try:
            print("------------------------------------")
            df = pd.read_excel(ruta)

            df.fillna("--",inplace=True)
            df = df[self.columns_valid]
            data=[]

            for _,row in df.iterrows():
                row = row.to_dict()

                content={
                        "FASE":row["FASE"],
                        "ACTIVIDAD":row["ACTIVIDAD"],
                        "CODIGO_ACTIVIDAD":row["CODIGO_ACTIVIDAD"],
                        "EVIDENCIA":row["EVIDENCIA"],
                        "FECHA":row["FECHA"],
                        "NOTA":row["NOTA"],
                        "OBSERVACION":row["OBSERVACION"],
                        "IMPORTANTE":row["IMPORTANTE"]
                    }
                                
                res = self.add_row(content)
                print(res)
                if not res['status']:
                    data.append(row["EVIDENCIA"])
            
            if data:
                msg ="Informacion no cargada correctamente"
                status = False
            else:
                msg ="OK"
                status = True

            self.evidencia.setResponse(status,msg, data)
        except Exception as ex:
            self.evidencia.setResponse(False,ex)
        finally:
            return self.evidencia.getResponse()

    def export_data(self,ruta):
        try:
            self.evidencia.select("EVIDENCIA.ID", "FASE","ACTIVIDAD","CODIGO_ACTIVIDAD", "EVIDENCIA", "FECHA", "NOTA", "OBSERVACION", "IMPORTANTE")
            self.evidencia.join("LEFT","FASE ","ID","EVIDENCIA","FASE_FK")
            self.evidencia.join("LEFT","ACTIVIDAD ","ID","EVIDENCIA","ACTIVIDAD_FK")
            self.evidencia.join("LEFT","COD_ACTIVIDAD ","ID","EVIDENCIA","COD_ACTIVIDAD_FK")
            self.evidencia.execute_query()

            df = pd.read_sql_query(self.evidencia.sql,self.evidencia.con)

            df.to_excel(ruta, index=False)
            self.evidencia.setResponse(True,'ok')
        except Exception as ex:
            self.evidencia.setResponse(False,ex)
        finally:
            self.evidencia.close()
            return self.evidencia.getResponse()

    # OBTENER REGISTROS TOTALES
    def getLen(self):
        data = self.evidencia.select("count(EVIDENCIA)").first()
        return data['data'][0]
    
    def setOrder(self,order):
        self.orde = order

    def getData(self):
        self.evidencia.select(*self.table_cols)
        self.evidencia.join("LEFT","FASE ","ID","EVIDENCIA","FASE_FK")
        self.evidencia.join("LEFT","ACTIVIDAD ","ID","EVIDENCIA","ACTIVIDAD_FK")
        self.evidencia.join("LEFT","COD_ACTIVIDAD ","ID","EVIDENCIA","COD_ACTIVIDAD_FK")
        self.evidencia.order_by(*self.order)

        data = self.evidencia.get()

        return data["data"]
    
    def prepare_data(self,data):
        def validate_insert(object,column,column_data,content):
                res = object.select("ID").where(column,column_data).first()
                if(res["data"]):
                    res = res["data"][0]
                else:
                    object.insert(**content)
                    res = object.getResponse()
                    res = res["data"]
                
                return res
        ids={}
        content ={"FASE":data['FASE']}
        ids['ID_FASE'] = validate_insert(self.fase,'FASE',data['FASE'],content)
        
        content = {"ACTIVIDAD":data["ACTIVIDAD"]}
        ids['ID_ACTIVIDAD'] = validate_insert(self.actividad,"ACTIVIDAD",data["ACTIVIDAD"],content)
        
        content = {"CODIGO_ACTIVIDAD":data["CODIGO_ACTIVIDAD"]}
        ids['ID_COD_ACTIVIDAD'] = validate_insert(self.cod_actividad,"CODIGO_ACTIVIDAD",data["CODIGO_ACTIVIDAD"],content)

        content = {
            "EVIDENCIA":data["EVIDENCIA"],
            "FECHA":data["FECHA"],
            "NOTA":data["NOTA"],
            "OBSERVACION":data["OBSERVACION"],
            "IMPORTANTE":data["IMPORTANTE"],
            "FASE_FK":ids["ID_FASE"],
            "ACTIVIDAD_FK":ids["ID_ACTIVIDAD"],
            "COD_ACTIVIDAD_FK":ids["ID_COD_ACTIVIDAD"]
            }
        
        return content

    def getRow(self, index):
        self.evidencia.select("EVIDENCIA.ID", "FASE","ACTIVIDAD","CODIGO_ACTIVIDAD", "EVIDENCIA", "FECHA", "NOTA", "OBSERVACION", "IMPORTANTE")
        self.evidencia.join("LEFT","FASE ","ID","EVIDENCIA","FASE_FK")
        self.evidencia.join("LEFT","ACTIVIDAD ","ID","EVIDENCIA","ACTIVIDAD_FK")
        self.evidencia.join("LEFT","COD_ACTIVIDAD ","ID","EVIDENCIA","COD_ACTIVIDAD_FK")
        self.evidencia.where("EVIDENCIA.ID",index)
        data = self.evidencia.first()

        return data

    def add_row(self, data):
                
        try: 
            if self.valid_columns(data):
                
                content = self.prepare_data(data)
                
                res =self.evidencia.select("ID").where('EVIDENCIA',data["EVIDENCIA"]).first()
                if(res["data"]):
                    id =res["data"][0]
                    res = self.update(id)
                    res["data"] = id if res['status'] else -1
                else:
                    self.evidencia.insert(**content)
                    res = self.evidencia.getResponse()
                    res = res["data"]

            else:
                self.evidencia.setResponse(False,"COLUMNS INVALIDS")
        except Exception as ex:
            self.evidencia.setResponse(False,'ADD ROW METHOD',ex)
        finally:
            return self.evidencia.getResponse()

    def update(self,**content):
        res = {"status":False}
        try:
            if self.valid_columns(content):
                data = self.prepare_data(content)

                self.evidencia.update(**data).where('ID',content["ID"]).get()
                
            else:
                self.evidencia.setResponse(False,"COLUMNS INVALIDS")
        except Exception as ex:
            self.evidencia.setResponse(False,'ADD ROW METHOD',ex)
        finally:
            return self.evidencia.getResponse()
        
    def delete(self,id):
        try:
            self.evidencia.delete().where("ID",id).get()
            
            return True
        except Exception as ex:
            self.evidencia.setResponse(False,'DELETE ROW METHOD',ex)
    
    def setFilter(self,filterData):
        for col,options in filterData.items():
            for opt, values in options.items():
                for value in values :

                    if opt == "igual a":
                        opt = "="
                    
                    elif opt == "no igual":
                        opt = "!="
                    
                    elif opt == "contiene":
                        opt = "LIKE"
                        value = f"%{value}%"
                    
                    elif opt == "no contiene":
                        opt = "NOT LIKE"
                        value = f"%{value}%"
                    
                    elif opt == "empieza":
                        opt = "LIKE"
                        value = f"{value}%"
                    
                    elif opt == "no empieza":
                        opt = "NOT LIKE"
                        value = f"{value}%"
                    
                    elif opt == "termina":
                        opt = "LIKE"
                        value = f"%{value}"
                    
                    elif opt == "no termina":
                        opt = "NOT LIKE"
                        value = f"%{value}"
                    else:
                        print(f"Operación no soportada: {opt}")
                    self.evidencia.AND(col,value,opt)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataController, cls).__new__(cls)
        return cls._instance



