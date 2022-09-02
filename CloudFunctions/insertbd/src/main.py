import os
import json
from google.cloud import storage
from google.cloud import secretmanager
from numpy import append
import mysql.connector



def main(request):
    secret = "projects/{0}/secrets/{1}/versions/{2}".format(
        os.environ.get('secret_project'),
        os.environ.get('secret_name'),
        os.environ.get('secret_version'))

    sm_client = secretmanager.SecretManagerServiceClient()
    response = sm_client.access_secret_version(request={"name": secret})
    args = json.loads(response.payload.data.decode("utf-8"))
    storage_client = storage.Client()

    host = args.get("host")
    database = args.get("database")
    user = args.get("user")
    password= args.get("password")
    bucket_name_insert= args.get("bucket_name_insert")

    connection = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    list_blobs_with_prefix_to_mysql(bucket_name_insert,None,storage_client,connection)

def list_blobs_with_prefix_to_mysql(bucket_name, prefix,storage_client,connection, delimiter=None):
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
    for blob in blobs: 
        a= blob.download_as_string()
        if((a)!=b''):
            s = a.decode('UTF-8')
            d = json.loads(s)
            r = Factura(d,connection)
 
        else:
            r=blob.name
            print("Revisar",r)
                    

class Factura():
    def __init__(self,d,connection):
        self.Document_Content_DTE_Documento_Encabezado_IdDoc_pk=(d['Document']['Content']['DTE']['Documento']['Encabezado']['Emisor']['RUTEmisor'].replace("-", ""))+'_'+(d['Document']['Content']['DTE']['Documento']['Encabezado']['IdDoc']['TipoDTE'])+'_'+(d['Document']['Content']['DTE']['Documento']['Encabezado']['IdDoc']['Folio'])+'_'+(d['Document']['Content']['DTE']['Documento']['Encabezado']['IdDoc']['FchEmis'])
        self.Document_Content_DTE_Documento_Encabezado_IdDoc_TipoDTE=d['Document']['Content']['DTE']['Documento']['Encabezado']['IdDoc']['TipoDTE']
        self.Document_Content_DTE_Documento_Encabezado_IdDoc_Folio=d['Document']['Content']['DTE']['Documento']['Encabezado']['IdDoc']['Folio']
        self.Document_Content_DTE_Documento_Encabezado_IdDoc_FchEmis=d['Document']['Content']['DTE']['Documento']['Encabezado']['IdDoc']['FchEmis']
        _pk_cabecera= self.Document_Content_DTE_Documento_Encabezado_IdDoc_pk
        _TipoDTE=self.Document_Content_DTE_Documento_Encabezado_IdDoc_TipoDTE
        _Folio=self.Document_Content_DTE_Documento_Encabezado_IdDoc_Folio
        _FchEmis=self.Document_Content_DTE_Documento_Encabezado_IdDoc_FchEmis
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO Prueba ( pk_cabecera, TipoDte, Folio, FchEmis) 
                                    VALUES (%s,%s,%s,%s) """
        record = (_pk_cabecera,int(_TipoDTE),int(_Folio),(_FchEmis))
        cursor.execute(mySql_insert_query, record)
        connection.commit()
    

   