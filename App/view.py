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
import threading
from DISClib.ADT import stack
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gr
assert cf

sys.setrecursionlimit(2**20)

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

def result2(stackPath, cA, cB ): 

    minPath = 0
    first = lt.firstElement(stackPath)['vertexA']
    last = lt.lastElement(stackPath)['vertexB']

    for e in lt.iterator(stackPath):
        origin = e['vertexA']
        destin = e['vertexB']
        weight = e['weight']

        print('Desde: ' + origin +' Hasta: ' + destin + ' // Con una distancia de: ' + str(weight))
        
        minPath += weight
    
    print('\nTamaño de la ruta entre: ' + cA + ' (' + first +')'+ ' y ' + cB + ' (' + last +')' +' es de: ' + str(minPath) +' km.\n')



def printReq1(Req1, landingPoint1, landingPoint2):
    print('***** Resultados del Requerimiento 1 *****')
    print('Cantidad de clusteres dentro de la red: ' + str(Req1['clusterNum']))
    if Req1['condicion']:
        print(str(landingPoint1) + ' y ' + str(landingPoint2) + ' pertenecen al mismo cluster')
    else:
        print(str(landingPoint1) + ' y ' + str(landingPoint2) + ' NO pertenecen al mismo cluster')
    print('**************************************')


def printReq3(Req3):
    print('El costo total en distancia en km de la red de expansión minima es de: ' + str(Req3[0]))
    print('El numero de landing Points conectados a la red de expansion minima es de: ' + str(Req3[1]))
    for entry in lt.iterator(Req3[2]):
        print('Recorrido desde ' + str(entry[0]) + ' hasta ' + str(entry[1]))
    print('arcos en la rama es de: ' + str(lt.size(Req3[2])))


"""
Menu principal
"""


def thread_cycle():
    

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
            tuple = controller.loadData(catalog)
            print('Total of landing points: '+ str(tuple[1]))
            print('Total of connections between landing point2s: '+ str(tuple[2]))
            print('Total of countries: ' + str(tuple[0]))
            
            first = lt.firstElement(catalog['FirstPoint'])
            print('First Landing point:')
            print('Name: ' + first['name'] +' Id: ' + str(first['id']) + ' Latitude: ' + first['latitude'] +' Longitude: ' +first['longitude'])
            last = lt.lastElement(catalog['LastCountry'])
            print('Last country:')
            print ('Name: ' + last['country'] +' Population: ' + str(last['population']) + ' Internet users: ' + str(last['internet_users']))
            print("Se ha cargado la información con exito")

        elif int(inputs[0]) == 3:
            print("Introduzca el nombre de los dos landing points")
            LandingPoint1 = input("Nombre del primer Landing Point:\n>")
            LandingPoint2 = input("Nombre del segundo Landing Point:\n>")
            print("Cargando información ....")
            Req1 = controller.getReq1(catalog, LandingPoint1, LandingPoint2)
            print(Req1)
            printReq1(Req1[0], LandingPoint1, LandingPoint2)
            print('\n')
            print("Tiempo [ms]: ", f"{Req1[1]:.3f}", "    ||  ", "Memoria [kB]: ", f"{Req1[2]:.3f}")
            print('\n')

        elif int(inputs[0]) == 4:
            print("Introduzca el nombre de dos paises. El primero es el pais de origen del cable")
            paisA = input("Nombre del pais de origen:\n>")
            paisB = input("Nombre del pais destino:\n")
            print("Cargando información ...\n")

            Req2 = controller.Req2(catalog, paisA, paisB)
            result2(Req2[0], paisA, paisB)
            print("Tiempo [ms]: ", f"{Req2[1]:.3f}", "    ||  ", "Memoria [kB]: ", f"{Req2[2]:.3f}")

            Req4 = controller.Req4(catalog, Req2, 2)

        elif int(inputs[0]) == 5:
            print("Cargando información ....")
            Req3 = controller.getReq3(catalog)
            printReq3(Req3[0])
            print("Tiempo [ms]: ", f"{Req3[1]:.3f}", "    ||  ", "Memoria [kB]: ", f"{Req3[2]:.3f}")
        else:
            sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
