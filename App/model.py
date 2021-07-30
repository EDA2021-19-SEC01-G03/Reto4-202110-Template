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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import haversine as hs
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newCatalog():
    """
    Crea un catalogo vacio
    """
    catalog = {'hashCountryCap': None, 'hashidInfo': None, 'GraphName': None }
    
    catalog['hashCountryCap'] = mp.newMap(maptype='PROBING')
    catalog['hashidInfo'] = mp.newMap(maptype='PROBING')
    catalog['GraphName'] = gr.newGraph(directed=True, size=0)
    
    
    
    
    return catalog
# Funciones para agregar informacion al catalogo


def addCountry(catalog, country):
    addCountryHash(catalog['hashCountryCap'], country)
    addCountryGraph(catalog['GraphName'], country)


def addCountryHash(hash, country):
    mp.put(hash, country['CountryName'], country)


def addCountryGraph(graph, country):
    vertex = country['CapitalName']
    gr.insertVertex(graph, vertex)


def addLandingPoint(catalog, landingPoint):
    addLandingPointHash(catalog['hashidInfo'], landingPoint)
    addLandingPointGraph(catalog['GraphName'], landingPoint)


def addLandingPointHash(hash, LandingPoint):
    mp.put(hash, LandingPoint['landing_point_id'], LandingPoint)


# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento


"""
loc1 = [28.426846, 77.088834] La primera coordenada de la tupla es la latitud, la segunda coordenada es la longitud
loc2 = [28.394231, 77.050308]
a = hs.haversine(loc1, loc2)  Esta función devuelve la distancia en km. Lo que nos funciona ya que todos los requerimientos piden kilometros como unidades
""""
