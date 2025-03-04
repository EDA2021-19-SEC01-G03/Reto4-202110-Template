﻿"""
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
import folium
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.ADT import stack as st
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import prim as pr
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
    catalog = {'hashCountryCap': None, 'hashidInfo': None, 'GraphName': None, 'FirstPoint': None, 'LastCountry': None, 'hashInfoName':None}
    
    catalog['hashCountryCap'] = mp.newMap(maptype='PROBING')
    catalog['hashidInfo'] = mp.newMap(maptype='PROBING')
    catalog['GraphName'] = gr.newGraph(directed=True, size=0)
    catalog['FirstPoint'] = lt.newList('ARRAY_LIST')
    catalog['LastCountry'] = lt.newList('ARRAY_LIST')
    catalog['hashInfoName'] = mp.newMap(maptype='PROBING')
    
    
    
    
    
    return catalog
# Funciones para agregar informacion al catalogo

def FirstPoint(catalog, elem): 
    info = {'name': elem['name'], 'id': elem['landing_point_id'], 
            'latitude': elem['latitude'], 'longitude': elem['longitude']}
    
    lt.addLast(catalog['FirstPoint'], info)


def InfoCountry(catalog, coun):
    info = {'country': coun['CountryName'], 'population': coun['Population'],
             'internet_users':coun['Internet users']}
    return info


def InfoCap(catalog, coun):
    name = coun['CapitalName'].split(',')[0]
    info = {'name': name, 'latitude': coun['CapitalLatitude'],
             'longitude':coun['CapitalLongitude']}
    return name, info


def addCountry(catalog, country):
    addCountryHash(catalog['hashCountryCap'], country)
    addCountryGraph(catalog['GraphName'], country)
    info = InfoCountry(catalog, country)
    lt.addLast(catalog['LastCountry'], info)
    info2 = InfoCap(catalog, country)
    mp.put(catalog['hashInfoName'], info2[0], info2[1])


def addCountryHash(hashCountry, country):
    mp.put(hashCountry, country['CountryName'], country)


def addCountryGraph(graph, country):
    vertex = country['CapitalName']
    gr.insertVertex(graph, vertex)


def addLandingPoint(catalog, landingPoint):
    addLandingPointHash(catalog['hashidInfo'], landingPoint)
    addLandingPointGraph(catalog,catalog['GraphName'], catalog['hashCountryCap'], landingPoint)
    addLPinfo(catalog['hashInfoName'], landingPoint)


def addLandingPointHash(hashidInfo, LandingPoint):
    mp.put(hashidInfo, LandingPoint['landing_point_id'], LandingPoint)
    return None


def addLPinfo(map, lp): 
    name = lp['name'].split(',')[0]
    mp.put(map, name, lp)

def addLandingPointGraph(catalog, graph, countryHash,  landingPoint):
    #Se añade el vertice y se busca la info del Landing Point
    landingPointName = landingPoint['name'].split(',')[0]
    landingPointPos = [float(landingPoint['latitude']), float(landingPoint['longitude'])]
    gr.insertVertex(graph, landingPointName)
    
    #Se revisa la existencia de la capital y se crean las conexiones
    landingPointCount = landingPoint['name'].split(',')[-1].strip()
    countryCapInfo = getCountryCap(countryHash, landingPointCount)
    cond = gr.containsVertex(graph, countryCapInfo['name'])
    if cond:
        addCapitalConnection(graph, landingPointName, countryCapInfo['name'], landingPointPos, countryCapInfo['pos'])


def addCapitalConnection(graph, landingPointName, capitalName, landingPointPos, capitalPos):
    costo = hs.haversine(landingPointPos, capitalPos)
    gr.addEdge(graph, landingPointName, capitalName, costo)
    gr.addEdge(graph, capitalName, landingPointName, costo)

def getCountryCap(countryHash, country):
    pair = mp.get(countryHash, country)
    if pair:
        countryInfo = me.getValue(pair)
        name = countryInfo['CapitalName']
        pos = [float(countryInfo['CapitalLatitude']), float(countryInfo['CapitalLongitude'])]
        retorno = {'name':name, 'pos': pos}
        return retorno
    else:
        return None


def getLandingPointInfo(hashidInfo, LandingPointid):
    pair = mp.get(hashidInfo, LandingPointid)
    retorno = {'name': None, 'pos': None}
    if pair:
        info = me.getValue(pair)
        name = info['name'].split(',')[0]
        pos = [float(info['latitude']), float(info['longitude'])]
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

def getReq1(catalog, landingPoint1, landingPoint2):
    sccSearch = scc.KosarajuSCC(catalog['GraphName'])
    clusterNum = sccSearch['components']
    condicion = scc.stronglyConnected(sccSearch, landingPoint1, landingPoint2)
    retorno = {'clusterNum': clusterNum, 'condicion': condicion}
    return retorno, sccSearch

def Req2(catalog, cA, cB): 
    """
    Retorna un stack con la ruta mínima (en km) entre A y B 
    """
    #Graph
    graph = catalog['GraphName']

    #Capital A
    hA = mp.get(catalog['hashCountryCap'], cA)
    capitalA = me.getValue(hA)['CapitalName']
    #Capital B
    hB = mp.get(catalog['hashCountryCap'], cB)
    capitalB = me.getValue(hB)['CapitalName']
    
    #Recorridos mínimos de A
    pathsA = djk.Dijkstra(graph, capitalA)

    minimum = APathB(pathsA, capitalB)

    return minimum

def APathB (pathsA, capitalB):

    return djk.pathTo(pathsA, capitalB)

def getReq3(catalog):
    mstSearch = pr.PrimMST(catalog['GraphName'])
    peso = pr.weightMST(catalog['GraphName'], mstSearch)
    
    hash= mstSearch['edgeTo']

    vertex = mp.keySet(hash)
    retsize = mp.size(mstSearch['edgeTo'])

    
    mayor = 0 
    stackM = ""
    name=''

    for v in lt.iterator(vertex):

        path = st.newStack()
        edge = mp.get(hash, v)

        value1 = 0
        value2= 0 
        weight = 0
        
        if edge is not None:
            value1 = me.getValue(edge)['vertexA']
            value2 = me.getValue(edge)['vertexB']
            weight = me.getValue(edge)['weight']
        
            path = st.push(path, [value1, value2, weight])


        while value1 != None:
            st.push(path, [value1, value2, weight])
            
            
            edge = mp.get(hash, value1)

            if edge is not None:
                value1 = me.getValue(edge)['vertexA']
                value2 = me.getValue(edge)['vertexB']
                weight = me.getValue(edge)['weight']
            else:
                value1 = None

        size = st.size(path)
        

        if size >= mayor: 
            mayor = size
            name = v
            stackM = path
    return peso, retsize, stackM
        

    """
    peso = pr.weightMST(catalog['GraphName'],mstSearch) #Este es el peso del arbol
    print(peso)
    print(mp.size(mstSearch['edgeTo'])) #Este creo que es el numero de vertices en el mst
    print(mstSearch['edgeTo'])
    print('bazinga bazonga bazinga')
    print(lt.size(mstSearch['mst']))
    print(mstSearch['mst'])
    """
    
    #Falta encontrar como encontrar la rama mas larga
    return None


def Req4_1(catalog,result, first, last):

    struct = result['idscc']
    keys = mp.keySet(struct)

    hash1 = mp.get(catalog['hashInfoName'], first)
    ent1 = me.getValue(hash1)

    land1= mp.get(struct,first)
    valu1= me.getValue(land1)
    
    m = folium.Map(location =[ent1['latitude'], ent1['longitude']], )
    folium.Marker([ent1['latitude'], ent1['longitude']], popup=valu1, icon=folium.Icon(color='green')).add_to(m)

    hash2 = mp.get(catalog['hashInfoName'], last)
    ent2= me.getValue(hash2)

    land2= mp.get(struct,last)
    valu2= me.getValue(land2)

    folium.Marker([ent2['latitude'], ent2['longitude']], popup=valu2, icon=folium.Icon(color='orange')).add_to(m)
    a = [float(ent1['latitude']), float(ent1['longitude'])]
    b =  [float(ent2['latitude']), float(ent2['longitude'])]
    points = [a,b]

    folium.PolyLine(points, color= 'red').add_to(m)

    for e in lt.iterator(keys):

        land = mp.get(struct, e)
        val = me.getValue(land)

        if e != first or e!= last:
            valu = mp.get(catalog['hashInfoName'], e)
            if valu is not None:
                final =me.getValue(valu)

                folium.Marker([final['latitude'], final['longitude']], popup=val).add_to(m)


    m.save(cf.data_dir + '/Req1')



def Req4_2(catalog, result): 

    f = st.pop(result)
    vertexA = f['vertexA']
    valA = mp.get(catalog['hashInfoName'], vertexA)
    finalA =me.getValue(valA)
    vertexB = f['vertexB']
    valB = mp.get(catalog['hashInfoName'], vertexB)
    finalB =me.getValue(valB)

    m = folium.Map(location =[finalA['latitude'], finalA['longitude']])

    for e in lt.iterator(result): 


        
        vertexA = e['vertexA']
        valA = mp.get(catalog['hashInfoName'], vertexA)
        finalA =me.getValue(valA)
        vertexB = e['vertexB']
        valB = mp.get(catalog['hashInfoName'], vertexB)
        finalB =me.getValue(valB)

        a = [float(finalA['latitude']), float(finalA['longitude'])]
        b =  [float(finalB['latitude']), float(finalB['longitude'])]
        points = [a,b]
        
        folium.Marker([finalA['latitude'], finalA['longitude']]).add_to(m)
        folium.Marker([finalB['latitude'], finalB['longitude']]).add_to(m)

        folium.PolyLine(points, color= 'red').add_to(m)

        m.save(cf.data_dir + '/Req2')


def Req4_3(catalog, result): 

    f = st.pop(result)
    vertexA = f[0]
    valA = mp.get(catalog['hashInfoName'], vertexA)
    finalA =me.getValue(valA)
    vertexB = f[1]
    valB = mp.get(catalog['hashInfoName'], vertexB)
    finalB =me.getValue(valB)

    m = folium.Map(location =[finalA['latitude'], finalA['longitude']])

    for e in lt.iterator(result): 


        
        vertexA = e[0]
        valA = mp.get(catalog['hashInfoName'], vertexA)
        finalA =me.getValue(valA)
        vertexB = e[1]
        valB = mp.get(catalog['hashInfoName'], vertexB)
        finalB =me.getValue(valB)

        a = [float(finalA['latitude']), float(finalA['longitude'])]
        b =  [float(finalB['latitude']), float(finalB['longitude'])]
        points = [a,b]
        
        folium.Marker([finalA['latitude'], finalA['longitude']]).add_to(m)
        folium.Marker([finalB['latitude'], finalB['longitude']]).add_to(m)

        folium.PolyLine(points, color= 'blue').add_to(m)

        m.save(cf.data_dir + '/Req3')



            

            






# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento


"""
loc1 = [28.426846, 77.088834] La primera coordenada de la tupla es la latitud, la segunda coordenada es la longitud
loc2 = [28.394231, 77.050308]
a = hs.haversine(loc1, loc2)  Esta función devuelve la distancia en km. Lo que nos funciona ya que todos los requerimientos piden kilometros como unidades
"""
