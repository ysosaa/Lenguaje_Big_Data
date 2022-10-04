import numpy as np
import pandas as pd
import os
from pathlib import Path
from funciones import *



filename = "llamadas123_julio_2022.csv"
datos = get_dat(filename)

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

# eliminacion de filas duplicadas 

datos = duplicados(datos)





