import sqlite3

class Model:
    # COSNTRUCTOR
    def __init__(self, table, ruta= None):
        # NOMBRE DE LA TABLA
        self.table = table

        # INICIALIZA VARIABLES
        self.__resetStatements()

        # IMPORTA SCRIPT SQL DESDE UN ARCHIVO
        self.import_query(ruta) if ruta is not None else None

    # ESTABLECE ESTRUCTURA DE UNA RESPUESTA
    def setResponse(self,status:bool,msg:str,data=None):
        self.response = {
            "message":msg,
            "status":status,
            "data":data
        }
    
    # RETORNA LA RESPUESTA
    def getResponse(self):
        return self.response
    
    # RESETEA VALOR DE VARIABLES SQL
    def __resetStatements(self):
        self.query = None
        self.sql=""
        self.where_sentence=""
        self.join_sentence=""
        self.groupby=""
        self.order_sentence=""
        self.limit=""
        self.param = list()

    # REALIZA CONEXION A BBDD
    def __conect(self):
        try:

            # SE CONECTA, SI NO, LA CREA
            self.con = sqlite3.connect("bbdd.db")

            # CREA UN CURSOR
            self.cursor = self.con.cursor()

            # ESTABLECE UNA RESPUESTA OK
            self.setResponse(True,"ok")
        except Exception as ex:
            # ESTABLECE UNA RESPUESTA ERROR
            self.setResponse(False,ex,"__conect")
    
    def close(self):
        try:
            # CIERRA LA CONEXION A LA BBDD
            self.con.close()
            self.cursor.close()
            # ESTABLECE UNA RESPUESTA OK
            self.setResponse(True,"ok")
        except Exception as ex:
            pass
    
    
    # DA FORMATO A LOS PARAMEROS PARA EL QUERY
    def __format_param(self,item):
        # AGREGA COMILLAS SIMPLES SI ES str   
        return f"'{item}'" if isinstance(item,str) else str(item)

    # DA FORMATO A LOS OPERADORES DEL QUERY
    def __structure_condition(self, operator, value):
        # EN EL CASO DE QUE value SEA UN ARRAY EL OPERADOR CAMBIA A UN IN
        if isinstance(value, list):
            operator = "NOT IN" if "!=" == operator else "IN"
        # ESTRUCTURA LOS VALORES DE LAS CONSULTAS
        if isinstance(value, list):
            value = ",".join(self.__format_param(item) for item in value)
        else:
            value = self.__format_param(value)
        return operator, value
   
    # ESTRUCTURA EL QUERY Y LO EJECUTA
    def import_query(self, ruta):
        try:
            # SE CONECTA A LA BBDD
            self.__conect()

            if self.response["status"]:
                # LEE ELARCHIVO Y EJECUTA EL SCRIPT
                query = open(ruta).read()
                self.cursor.executescript(query)

            # ESTABLECE UNA RESPUESTA OK
            self.setResponse(True,"ok")
                
        except Exception as ex:
            # ESTABLECE UNA RESPUESTA ERROR
            self.setResponse(False,ex,"import_query")
        finally:
            # CIERRA LA CONEXION A LA BBDD
            self.close()

    # DA FORMATO AL QUERY Y EJECUTA LA CONSULTA
    def execute_query(self):
        
        # SE CONECTA A LA BBDD
        self.__conect()

        # DA FORMATO AL QUERY
        self.sql = f"{self.sql} {self.join_sentence} {self.where_sentence} {self.groupby} {self.order_sentence} {self.limit}"

        # EJECUTA EL QUERY
        self.query = self.cursor.execute(self.sql,self.param)  
        self.con.commit()           
       
    # AÑADE REGISTRO A LA BBDD
    def insert(self, **data):
        try: 
            # CREA FORMATO PARA EL QUERY
            claves = ', '.join(data.keys())
            into = ",".join("?" for item in data.keys())
            
            self.sql = f"INSERT INTO {self.table} ({claves}) VALUES ({into})"
            self.param = list(data.values())

            # EJECUTA EL QUERY
            self.execute_query()
            id = self.cursor.lastrowid
            
            # ESTABLECE UNA RESPUESTA OK
            self.setResponse(True,"Datos Ingresados",id)
        except Exception as ex:
            # ESTABLECE UNA RESPUESTA ERROR
            self.setResponse(False,ex,"insert")
        finally:
            self.close()
            self.__resetStatements()

    # EXTRAE REGISTROS DEL BBDD
    def select(self,*colums):
        try:
            # SE CONECTA A LA BBDD
            self.__conect()

           # CREA FORMATO PARA EL QUERY 
            colums = ",".join(colums)
            self.sql = f"SELECT {colums} FROM {self.table}"

        except Exception as ex:
            # ESTABLECE UNA RESPUESTA ERROR
            self.setResponse(False,ex,"select")
        finally:

            return self

    # EXTRAE LOS VALORES DEL QUERY
    def get(self):
        try: 
            # EJECUTA LA CONSULTA
            self.execute_query()

            # RETORNA EL VALOR DE LA CONSULTA
            data = self.query.fetchall()
            # data = list(data) if data is not None else []

            self.setResponse(True,"ok",data)

            # CIERRA LA BBDD Y RESETEA LOS QUERY
            self.close()
            self.__resetStatements()
        except Exception as ex:
            # ESTABLECE UNA RESPUESTA ERROR
            self.setResponse(False,ex,"import_query")
        finally:
            # CIERRA LA CONEXION A LA BBDD
            self.close()
        return self.response
    
    # EXTRAE EL PRIMER VALOR DEL QUERY
    def first(self):
        try:
            # EJECUTA LA CONSULTA

            self.execute_query()
            
            data =self.query.fetchone()
            data = list(data) if data is not None else []

            # RETORNA EL VALOR DE LA CONSULTA
            self.response["data"] = data  

            # CIERRA LA BBDD Y RESETEA LOS QUERY
            self.close()
            self.__resetStatements()
        except Exception as ex:
            # ESTABLECE UNA RESPUESTA ERROR
            self.setResponse(False,ex,"import_query")
        finally:
            # CIERRA LA CONEXION A LA BBDD
            self.close()
        return self.response
    
    # ESTRUCTURA LA PARTE DEL WHERE EN EL QUERY
    def where(self,column, value, operador="="):
        # EN EL CASO DE QUE value SEA UN ARRAY EL OPERADOR CAMBIA A UN IN
        operador, value = self.__structure_condition(operador,value)

        # ESTRUCTURA LA CONDICION DEL QUERY
        self.where_sentence = f"WHERE {column} {operador} ({value})"

        return self
    
    # AGREGA LA SENTENCIA OR EN LA PARTE DEL WHERE EN EL QUERY
    def OR(self,column, value, operador="="):
        # EN EL CASO DE QUE value SEA UN ARRAY EL OPERADOR CAMBIA A UN IN
        

        # EN EL CASO DE NO HABER UNA CONDICION ANTES, LA CREA
        if(self.where_sentence == ""):
            self.where(column,value,operador)
        else:
            # ESTRUCTURA LA CONDICION DEL QUERY
            operador, value = self.__structure_condition(operador,value)
            self.where_sentence = f" {self.where_sentence} OR {column} {operador} {value}"

        return self
    
    # AGREGA LA SENTENCIA AND EN LA PARTE DEL WHERE EN EL QUERY
    def AND(self,column, value, operador="="):
        # EN EL CASO DE QUE value SEA UN ARRAY EL OPERADOR CAMBIA A UN IN
        operador, value = self.__structure_condition(operador,value)
        
        # EN EL CASO DE NO HABER UNA CONDICION ANTES, LA CREA
        if(self.where_sentence == ""):
            self.where(column,value,operador)
        else:

            # ESTRUCTURA LA CONDICION DEL QUERY
            self.where_sentence = f" {self.where_sentence} AND {column} {operador} {value}"
        return self

    # ESTRUCTURA LA PARTE DEL LIMIT DEL QUERY
    def take(self,ini, cant):
        self.limit = f"LIMIT {ini},{cant}"
        return self
    
    # ESTRUCTURA LA PARTE DEL ORDER BY DEL QUERY
    def order_by(self,column, orden = "ASC"):
        self.order_sentence = f"ORDER BY {column} {orden}"
        return self
    
    # ESTRUCTURA LA PARTE DEL UPDATE DEL QUERY
    def update(self,**data):
        # ESTRUCTURA LOS VALORES DE LAS CONSULTAS
        data = ",".join(f"{item}={self.__format_param(value)}" for item,value in data.items())
    
        # ESTRUCTURA EL QUERY
        self.sql = f"UPDATE {self.table} SET {data}"
                
        return self
    
    # ESTRUCTURA LA PARTE DEL DELETE DEL QUERY
    def delete(self):
        self.sql = f"DELETE FROM {self.table}"
        return self
    
    # PERMITE OBTENER UN REGISTRO POR ID
    def find(self,id):
        self.select("*")
        self.where("ID",id)

        return self.first()

    # ESTRUCTURA LA PARTE DEL JOIN DEL QUERY
    def join(self,type, table1, id1,table2, id2):
        self.join_sentence = f"{self.join_sentence} {type} JOIN {table1} ON {table1}.{id1}={table2}.{id2}"
        
        return self

    # ESTRUCTURA LA PARTE DEL GROUP BY DEL QUERY
    def Group_By(self,column):
        self.groupby= f"{self.groupby} GROUP BY {column}"
        return self
    




