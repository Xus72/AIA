# AIA
# Problemas de Satisfacción de Restricciones
# Dpto. de C. de la Computación e I.A. (Univ. de Sevilla)
# ===================================================================

# En esta práctica vamos a programar el algoritmo de backtracking
# combinado con consistencia de arcos AC3 y la heurística MRV.

import random, copy


# ===================================================================
# Representación de problemas de satisfacción de restricciones
# ===================================================================

#   Definimos la clase PSR que servirá para representar problemas de
# satisfacción de restricciones.

# La clase tiene cuatro atributos:
# - variables: una lista con las variables del problema.
# - dominios: un diccionario que asocia a cada variable su dominio,
#      una lista con los valores posibles.
# - restricciones: un diccionario que asigna a cada tupla de
#      variables la restricción que relaciona a esas variables.
# - vecinos: un diccionario que asigna a cada variables una lista con
#      las variables con las que tiene una restricción asociada.

# El constructor de la clase recibe los valores de los atributos
# "dominios" y "restricciones". Los otros dos atributos se definen a
# partir de éstos valores.

# NOTA IMPORTANTE: Supondremos en adelante que todas las
# restricciones son binarias y que existe a lo sumo una restricción
# por cada par de variables.

class PSR:
    """Clase que describe un problema de satisfacción de
    restricciones, con los siguientes atributos:
       variables     Lista de las variables del problema
       dominios      Diccionario que asigna a cada variable su dominio
                     (una lista con los valores posibles)
       restricciones Diccionario que asocia a cada tupla de variables
                     involucrada en una restricción, una función que,
                     dados valores de los dominios de esas variables,
                     determina si cumplen o no la restricción.
                     IMPORTANTE: Supondremos que para cada combinación
                     de variables hay a lo sumo una restricción (por
                     ejemplo, si hubiera dos restricciones binarias
                     sobre el mismo par de variables, consideraríamos
                     la conjunción de ambas).
                     También supondremos que todas las restricciones
                     son binarias
        vecinos      Diccionario que representa el grafo del PSR,
                     asociando a cada variable, una lista de las
                     variables con las que comparte restricción.

    El constructor recibe los valores de los atributos dominios y
    restricciones; los otros dos atributos serán calculados al
    construir la instancia."""

    def __init__(self, dominios, restricciones):
        """Constructor de PSRs."""

        self.dominios = dominios
        self.restricciones = restricciones
        self.variables = list(dominios.keys())

        vecinos = {v: [] for v in self.variables}
        for v1, v2 in restricciones:
            vecinos[v1].append(v2)
            vecinos[v2].append(v1)
        self.vecinos = vecinos


# ===================================================================
# Ejercicio 1
# ===================================================================

#   Definir una función n_reinas(n), que recibiendo como entrada un
# número natural n, devuelva una instancia de la clase PSR,
# correspondiente al problema de las n-reinas.

# Ejemplos:

def n_reinas(n):
    def n_reinas_restr(i,j):
        return (lambda x,y : x != y and abs(i-j) != abs(x-y)) #x e y es el valor de las variables i,j
    dom = {i: [j for j in range(1,n+1)] for i in range(1,n+1)}
    restr = dict()
    for i in range(1,n):
        for j in range(i+1,n+1):
            restr[(i,j)] = n_reinas_restr(i,j)
    return PSR(dom, restr)

#psr_n4 = n_reinas(4)
#psr_n4.variables
# [1, 2, 3, 4]
#psr_n4.dominios
# {1: [1, 2, 3, 4], 2: [1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [1, 2, 3, 4]}
#psr_n4.restricciones
# {(1, 2): <function <lambda> at ...>,
#  (1, 3): <function <lambda> at ...>,
#  (1, 4): <function <lambda> at ...>,
#  (2, 3): <function <lambda> at ...>,
#  (3, 4): <function <lambda> at ...>,
#  (2, 4): <function <lambda> at ...>}
# >>> psr_n4.vecinos
# {1: [2, 3, 4], 2: [1, 3, 4], 3: [1, 2, 4], 4: [1, 2, 3]}
# >>> psr_n4.restricciones[(1,4)](2,3)
# True
# >>> psr_n4.restricciones[(1,4)](4,1)
# False

# Definir funcion coloreado_mapa(mapa,colores) devolviendo un PSR correspondiente a colorear el mapa con esos colores

mapa_andalucia = {"Huelva":["Cadiz","Sevilla"], "Sevilla":["Cadiz","Córdoba","Huelva","Málaga"],"Cadiz":["Málaga","Sevilla","Huelva"],
                  "Córdoba": ["Jaén","Granada","Málaga","Sevilla"],"Málaga":["Cadiz","Sevilla","Córdoba","Granada"],"Jaén":["Córdoba","Granada"],
                  "Granada":["Córdoba","Jaén","Almería","Málaga"],"Almería":["Granada"]}

colores_disp = ["azul", "rojo", "verde"]

def coloreado_mapa(mapa,colores):
    dom = {i:colores for i in mapa}
    restr = dict()
    for i in mapa:
        for j in mapa[i]:
            if(j,i) not in restr:
                restr[(i,j)] = (lambda x,y: x!=y)
    return PSR(dom,restr)

res = coloreado_mapa(mapa_andalucia,colores_disp)
print("Dominios\n")
print(res.dominios)
print("\nRestricciones\n")
print(res.restricciones)
print("\nVecinos\n")
print(res.vecinos)
