"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
import tracemalloc
import time


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros


def initCatalog():
    """
    Llama la función de inicialización del catalogo del modelo
    """
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos


def loadData(catalog):
    retorno = -1.0
    countries = loadCountries(catalog)
    print('Se cargaron Paises')
    landing = loadLandingPoints(catalog)
    print('Se cargaron Landing Points')
    connect = loadConnections(catalog)
    print('Se cargaron conexiones')
    
    return countries, landing, connect


def loadConnections(catalog):
    connectionsfile = cf.data_dir + 'connections.csv'
    input_file = csv.DictReader(open(connectionsfile, encoding="utf-8-sig"), delimiter=',')

    con = 0
    for entry in input_file:
        model.addConnection(catalog, entry)
        con += 1
    return con


def loadCountries(catalog):
    countriesfile = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(countriesfile, encoding="utf-8"), delimiter=',')
    coun = 0
    for entry in input_file:
        model.addCountry(catalog, entry)
        coun += 1
    return coun


def loadLandingPoints(catalog):
    landingPointsfile = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(landingPointsfile, encoding="utf-8"), delimiter=',')
    land = 0
    for entry in input_file:
        if land == 0:
            model.FirstPoint(catalog, entry)
        model.addLandingPoint(catalog, entry)
        
        land += 1
    return land


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


def getReq1(catalog, landingPoint1, landingPoint2):
    
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    
    result = model.getReq1(catalog, landingPoint1, landingPoint2)
    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return result, delta_time, delta_memory

def getReq3(catalog):
    
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    
    result = model.getReq3(catalog)
    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return result, delta_time, delta_memory

# Funciones para medir tiempo y memoria


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory