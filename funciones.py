# pseudo codigo 
# main ():
    # datos = get data( )
    #reporte = generate_report()
    #save_data = (reporte)

from pkgutil import get_data
import numpy as np
import pandas as pd
import os
from pathlib import Path

def get_dat(filename):
 root_dir = Path(".").resolve().parent
 file_path = os.path.join(root_dir, filename) #direcciono hacia el archivvo necesario 
 df = pd.read_csv(file_path, sep = ";", encoding="latin-1")
 return(df)
    
def generate_report (df):
    dict_reporte = dict()

    for col in df.columns:
        unicos = df[col].unique( )
        dict_reporte [col] = len(unicos)
        print("diferente tot dif", col ,"=",len(df[col].unique()))
        print("----------------")

def duplicados (df): 
    df = df.drop_duplicates()
    
    return(df)

