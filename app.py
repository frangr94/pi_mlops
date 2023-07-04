# iniciar con comando terminal : uvicorn app:app --reload
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Text,Optional
from datetime import datetime
import pandas as pd

app = FastAPI()


df = pd.read_csv('data_api.csv')
df['prod_companies']=df.prod_companies.str.strip('''""''') # tuve que emparchar esto


@app.get('/')
def read_root():
    return {'bienvenido':'bienvenido a mi REST API'}


# devuelve la cantidad de peliculas producidas en x idioma
@app.get('/count_lang')
def peliculas_idioma(Idioma: str):

    count=0
    for i in df.langs_unn:
        if Idioma in i:
            count+=1
    
    respuesta = "{} de peliculas producidas en: {}".format(count,idioma_iso)

    return respuesta

# devuelve duracion y año de una pelicula
@app.get('/duracion_pelicula')
def get_duracion(Pelicula: str):

    row = df[df['original_title'].str.contains(Pelicula)]
    nombre =row.original_title.values[0]
    año = row.release_year.values[0]
    duracion = row.runtime.values[0]
    if duracion==0:
        duracion='[no-data]'

    respuesta='la pelicula {} dura {} minutos y fue estrenada en {}'.format(nombre,duracion,año)
    
    return respuesta

# devuelve cantidad de peliculas, ganancias totales y promedio
@app.get('/franquicia')
def franquicia(Franquicia: str):

    rows=df.loc[df.collection_unn==Franquicia]
    cantidad_peliculas = len(rows)
    ganancia_total = rows['return'].sum()
    ganancia_promedio = ganancia_total/cantidad_peliculas

    respuesta='la franquicia {} ha producido {} peliculas, con una ganancia total de {} y una ganancia promedio de {}'.format(Franquicia,cantidad_peliculas,ganancia_total,ganancia_promedio)
    
    return respuesta

# devuelve la cantidad de peliculas producidas en un pais
@app.get('/count_pais')
def peliculas_pais( Pais: str ):
    count = 0
    for i in df.prod_countries_unn:
        if Pais in i:
            count+=1
    
    respuesta ='se produjeron {} peliculas en el pais {}'.format(count,Pais)

    return respuesta

# devuelve el revenue total y cantidad de peliculas realizadas
@app.get('/productoras')
def productoras_exitosas( Productora: str ):
    rows = df.loc[df.prod_companies.str.contains(Productora)]
    cantidad_peliculas = len(rows)
    ingresos = rows['revenue'].sum()

    respuesta='la productora {} produjo {} peliculas, con un revenue total de {}'.format(Productora,cantidad_peliculas,ingresos)
    return respuesta

# devuelve el exito de un director, junto a una lista de peliculas con estadisticas
@app.get('/directores')
def get_director(nombre_director: str):
    rows = df.loc[df.directors.str.contains(nombre_director)]
    ingresos = rows['revenue'].sum()
    values=['original_title','release_date','revenue','budget','return']
    peliculas=[]
    for index, row in rows.iterrows():
        z=row[['original_title','release_date','revenue','budget','return']]
        peliculas.append(list(z.values))

    resultado='el director {} ha tenido un revenue de {}'.format(nombre_director,ingresos)
    return resultado,peliculas
