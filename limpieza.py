import numpy as np
import pandas as pd
import os
from pathlib import Path
import logging

root_dir = Path(".").resolve()
bucket ='gs://llamadas123_2022' 

def get_Data(filename):
    logger = logging.getLogger('get_data')
    
    data_dir = 'raw'
    file_path = os.path.join(bucket, data_dir, filename)
    logger.info(f'Leyendo datos : {file_path}')
    datos = pd.read_csv(file_path, encoding ='latin-1', sep = ';')
    
    logger.info(f'leyendo datos:{datos.shape[0]} filas y datos{datos.shape[1]} columnas')
    return datos 

def duplicados (df): 
    df = df.drop_duplicates()
    
    return(df)

def generar_limpieza(datos):
    logger = logging.getLogger('generar_limpieza')
    #tranformacion de fechas y eliminacion de nulls 
    datos['UNIDAD'] = datos['UNIDAD'].fillna('SIN_DATO')
    datos['EDAD'] = datos['EDAD'].replace({'SIN_DATO' : np.nan})
    datos['EDAD'] = datos['EDAD'].apply(lambda x: x if pd.isna(x) == True else int(x))

    #tranformacion de fechas a datetime
    datos['FECHA_INICIO_DESPLAZAMIENTO_MOVIL'] = pd.to_datetime(datos['FECHA_INICIO_DESPLAZAMIENTO_MOVIL'], errors='coerce', format='%Y-%m-%d %H:%M:%S')
    datos['RECEPCION'] = pd.to_datetime(datos['RECEPCION'], errors='coerce', format='%Y-%m-%d %H:%M:%S')
    #eliminacion de espacios vacios 
    datos['LOCALIDAD'].apply(lambda x: x.strip())
    datos.LOCALIDAD = datos.LOCALIDAD.str.replace(' ','_')
    datos = duplicados(datos)
    return datos 

def save_data(reporte, filename):
    
    logger = logging.getLogger('save_data')
    
    out_name = 'resumen_' + filename
    out_path = os.path.join(bucket, 'processed', out_name)
    
    logger.info(f'Saving data in {out_path}')
    reporte.to_csv(out_path)

    table_name = 'llamadas.reporte'
    logger.info(f'Saving table {table_name} into BigQuery')
    reporte.to_gbq(table_name, if_exists = 'replace')
    

def generate_report (df):
    logger = logging.getLogger('generate_report')
    dict_reporte = dict()

    for col in df.columns:
        unicos = df[col].unique( )
        dict_reporte [col] = len(unicos)
        reporte = pd.DataFrame.from_dict(dict_reporte, orient = 'index')
        print("diferente tot dif", col ,"=",len(df[col].unique()))
        print("----------------")
    logger.info(f'generate_report')
    logger.info(reporte.head())
    
    
    return reporte
        
def main (): 
    # Basic configuration for logging
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    logging.captureWarnings(True)
    logging.basicConfig(
        level=logging.INFO, 
        format=log_fmt,
        # filename='data/logs/etl_llamadas.log'
    )
    
    filename ='llamadas123_julio_2022.csv'
    datos = get_Data(filename)
    datos = generar_limpieza(datos)
    reporte = generate_report(datos)
    save_data(reporte, filename)
    loggin.info("Done !!")
if __name__ == '__main__': 
    main()
    



