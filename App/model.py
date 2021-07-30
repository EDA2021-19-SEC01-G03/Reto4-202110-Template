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


def addCountryHash(hashCountry, country):
    mp.put(hashCountry, country['CountryName'], country)


def addCountryGraph(graph, country):
    vertex = country['CapitalName']
    gr.insertVertex(graph, vertex)


def addLandingPoint(catalog, landingPoint):
    addLandingPointHash(catalog['hashidInfo'], landingPoint)
    addLandingPointGraph(catalog['GraphName'], landingPoint)


def addLandingPointHash(hashidInfo, LandingPoint):
    mp.put(hashidInfo, LandingPoint['landing_point_id'], LandingPoint)
    return None


def getLandingPointInfo(hashidInfo, LandingPointid):
    pair = mp.get(hashidInfo, LandingPointid)
    retorno = {'name': None, 'pos': None}
    if pair:
        info = me.getValue(pair)
        name = info['name'].split()[0]
        pos = [info['latitude'], info['longitude']]
        retorno['name'] = name
        retorno['pos'] = pos
        return retorno
    else:
        print('No se encontro el Landing point. Programa va a explotar')
        return None


def addConnection(catalog, connection):
    originid = connection['origin']
    destinyid = connection['destination']
    graph = catalog['GraphName']
    hashidInfo = catalog['hashidInfo']
    originInfo = getLandingPointInfo(hashidInfo, originid)
    destinyInfo = getLandingPointInfo(hashidInfo, destinyid)
    addConnectionEdge(graph, originInfo, destinyInfo)


def addConnectionEdge(graph, originInfo, destinyInfo):
    costo = hs.haversine(originInfo['pos'], destinyInfo['pos'])
    gr.addEdge(graph, originInfo['name'], destinyInfo['name'], costo)


# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento


"""
loc1 = [28.426846, 77.088834] La primera coordenada de la tupla es la latitud, la segunda coordenada es la longitud
loc2 = [28.394231, 77.050308]
a = hs.haversine(loc1, loc2)  Esta función devuelve la distancia en km. Lo que nos funciona ya que todos los requerimientos piden kilometros como unidades
"""
