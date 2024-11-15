# -*- coding: utf-8 -*-
"""Trab.Caxeiro_Viajante.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TRtadM3wp54BQrySYrjdZxQQBH_Efza_

# Bibliotecas
"""

!pip install ortools

import geopandas as gpd
import pandas as pd
import folium
import numpy as np
from math import radians, sin, cos, sqrt, atan2
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

"""# Carregamento e manipulação do arquivo"""

# Carrega o arquivo geojson
gdf = gpd.read_file('/content/geojs-35-mun.json')

# Calcula o centróide de cada município
gdf['centroid'] = gdf['geometry'].centroid

# Extrai as coordenadas dos centróides
coordenadas = gdf[['name', 'centroid']]
coordenadas['latitude'] = coordenadas['centroid'].apply(lambda point: point.y)
coordenadas['longitude'] = coordenadas['centroid'].apply(lambda point: point.x)
coordenadas.drop('centroid', axis=1, inplace=True)

"""# Coordenadas de todas as cidades do Estado de SP"""

coordenadas

"""# Resolução do Problema"""

# Cria um dicionário com os dados das cidades
cities_data = {city: (lat, lon) for city, (lat, lon) in zip(coordenadas['name'], zip(coordenadas['latitude'], coordenadas['longitude']))}

# Função para calcular a distância Haversine entre duas cidades
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Raio da Terra em km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Criação da matriz de distâncias usando Haversine
def create_distance_matrix(cities):
    city_names = list(cities.keys())
    n = len(city_names)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = haversine(cities[city_names[i]][0], cities[city_names[i]][1], cities[city_names[j]][0], cities[city_names[j]][1])
    return distance_matrix

# Função principal para resolver o TSP
def solve_tsp(cities):
    distance_matrix = create_distance_matrix(cities)
    city_names = list(cities.keys())
    capital_index = city_names.index("São Paulo")
    manager = pywrapcp.RoutingIndexManager(len(city_names), 1, capital_index)  # Definindo São Paulo como ponto inicial e final

    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distance_matrix[from_node][to_node])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        route = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        return route, distance_matrix
    else:
        return None, None

# Calcula a distância total da rota
def calculate_total_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    return total_distance

# Estima o tempo de viagem dado uma velocidade média
def estimate_travel_time(total_distance, average_speed_kmh):
    return total_distance / average_speed_kmh

# Executa a solução do TSP
route, distance_matrix = solve_tsp(cities_data)

if route:
    city_names = list(cities_data.keys())
    named_route = [city_names[index] for index in route]

    print("Rota encontrada:")
    for city in named_route:
        print(city)

    total_distance = calculate_total_distance(route, distance_matrix)
    print(f"Distância total: {total_distance:.2f} km")

    # Estimando o tempo de viagem com uma velocidade média de 60 km/h
    average_speed_kmh = 60
    total_time_hours = estimate_travel_time(total_distance, average_speed_kmh)
    print(f"Tempo estimado de viagem: {total_time_hours:.2f} horas")
else:
    print("Não foi possível encontrar uma rota.")

"""# Criação do Mapa"""

# Criar o mapa de São Paulo
maps = folium.Map(location=[-23.5505, -46.6333], zoom_start=8)

# Adicionar marcadores das cidades
for city, coords in cities_data.items():
    if city == "São Paulo":
        folium.Marker(location=coords, popup=city, icon=folium.Icon(color='green')).add_to(maps)  # Destacar São Paulo em verde
    else:
        folium.Marker(location=coords, popup=city).add_to(maps)

# Adicionar a rota no mapa
coords_route = [cities_data[city] for city in named_route]
folium.PolyLine(locations=coords_route, color='blue').add_to(maps)

# Exibir o mapa
maps

"""# Somente o desenho da rota"""

# Criar o mapa de São Paulo - rota
rota = folium.Map(location=[-23.5505, -46.6333], zoom_start=8)

# Adicionar a rota no mapa
coords_route = [cities_data[city] for city in named_route]
folium.PolyLine(locations=coords_route, color='blue').add_to(rota)

# Destacar São Paulo em verde
folium.Marker(location=cities_data["São Paulo"], popup="São Paulo", icon=folium.Icon(color='green')).add_to(rota)

# Exibir o mapa - rota
rota