"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("**********Bienvenido**********")
    print("1- Iniciar el catalogo")
    print("2- Cargar información al catalogo")
    print("3- (Requerimiento 1) Encontrar la cantidad de clusteres en la red " + 
          "y comprobar si dos landing points pertenecen al mismo cluster")
    print("4- (Requerimiento 2) Encontrar la ruta minima para enviar información entre dos paises")
    print("5- (Requerimiento 3) Identificar la red de expansión minima")
    print("0- Salir de la aplicación")
    print("*******************************")
    
catalog = None

def loadInfo(tuple): 
    print('Total of landing points: '+ str(tuple[1]))
    print('Total of connections between landing points: '+ str(tuple[2]))
    print('Total of countries: ' + str(tuple[0]))
    
    first = lt.firstElement(catalog['FirstPoint'])
    print('First Landing point:')
    print('Name: ' + first['name'] +' Id: ' + str(first['id']) + ' Latitude: ' + first['latitude'] +' Longitude: ' +first['longitude'])
    last = lt.lastElement(catalog['LastCountry'])
    print('Last country:')
    print ('Name: ' + last['country'] +' Population: ' + str(last['population']) + ' Internet users: ' + str(last['internet_users']))


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')
    if int(inputs[0]) == 1:
        print("Iniciando el catalogo ....")
        #Se inicia el catalogo
        catalog = controller.initCatalog()
        print("El catalogo se ha iniciado con exito\n")

    elif int(inputs[0]) == 2:
        print("Cargando información al catalogo ....")
        #Se carga información al catalogo
        test = controller.loadData(catalog)
        result = loadInfo(test)

        print("Se ha cargado la información con exito")
        #printCargaDatos(catalog)

    elif int(inputs[0]) == 3:
        print("Introduzca el nombre de los dos landing points")
        LandingPoint1 = input("Nombre del primer Landing Point:\n>")
        LandingPoint2 = input("Nombre del segundo Landing Point:\n>")
        print("Cargando información ....")
        #Req1 = getReq1(catalog, LandingPoint1, LandingPoint2)
        #printReq1(Req1)

    elif int(inputs[0]) == 4:
        print("Introduzca el nombre de dos paises. El primero es el pais de origen del cable")
        paisA = input("Nombre del pais de origen:\n>")
        paisB = input("Nombre del pais destino:\n")
        print("Cargando información ....")
        #Req2 = getReq2(catalog, paisA, paisB)
        #printReq2(Req2)

    elif int(inputs[0]) == 5:
        print("Cargando información ....")
        #Req3 = getReq3(catalog)
        #printReq3(Req3)
    else:
        sys.exit(0)
sys.exit(0)
