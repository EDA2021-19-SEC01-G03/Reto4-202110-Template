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
    loadCountries(catalog)
    loadLandingPoints(catalog)
    loadConnections(catalog)
    
    return retorno


def loadConnections(catalog):
    connectionsfile = cf.data_dir + 'connections.csv'
    input_file = csv.DictReader(open(connectionsfile, encoding="utf-8"), delimiter=',')
    n = 0
    for entry in input_file:
        n += 1


def loadCountries(catalog):
    countriesfile = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(countriesfile, encoding="utf-8"), delimiter=',')
    n = 0
    for entry in input_file:
        model.addCountry(catalog, entry)


def loadLandingPoints(catalog):
    landingPointsfile = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(landingPointsfile, encoding="utf-8"), delimiter=',')
    n = 0
    for entry in input_file:
        model.addLandingPoint(catalog, entry)


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
