#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ==========================================================
# Ampliación de Inteligencia Artificial. Tercer curso.
# Grado en Ingeniería Informática - Tecnologías Informáticas
# Curso 2019-20
# Ejercicio de programación
# ===========================================================

# -----------------------------------------------------------
# NOMBRE: JESUS MANUEL
# APELLIDOS: SANCHEZ ALANIS
# -----------------------------------------------------------



# Escribir el código Python de las funciones que se piden en el
# espacio que se indica en cada ejercicio.

# IMPORTANTE: NO CAMBIAR EL NOMBRE NI A ESTE ARCHIVO NI A LAS FUNCIONES QUE SE
# PIDEN (aquellas funciones con un nombre distinto al que se pide en el
# ejercicio NO se corregirán).

# ESTE ENTREGABLE SUPONE 1.25 PUNTOS DE LA NOTA TOTAL

# *****************************************************************************
# HONESTIDAD ACADÉMICA Y COPIAS: la realización de los ejercicios es un
# trabajo personal, por lo que deben completarse por cada estudiante de manera
# individual.  La discusión con los compañeros y el intercambio de información
# DE CARÁCTER GENERAL con los compañeros se permite, pero NO AL NIVEL DE
# CÓDIGO. Igualmente el remitir código de terceros, obtenido a través
# de la red o cualquier otro medio, se considerará plagio.

# Cualquier plagio o compartición de código que se detecte significará
# automáticamente la calificación de CERO EN LA ASIGNATURA para TODOS los
# alumnos involucrados, independientemente de otras medidas de carácter
# DISCIPLINARIO que se pudieran tomar. Por tanto a estos alumnos NO se les
# conservará, para futuras convocatorias, ninguna nota que hubiesen obtenido
# hasta el momento.
# *****************************************************************************

import random, math

# Lo que sigue es la implementación de la clase HMM vista en la práctica 2,
# que representa de manera genérica un modelo oculto de Markov.

class HMM(object):
    """Clase para definir un modelo oculto de Markov"""

    def __init__(self,estados,mat_ini,mat_trans,observables,mat_obs):
        """El constructor de la clase recibe una lista con los estados, otra
        lista con los observables, un diccionario representado la matriz de
        probabilidades de transición, otro diccionario con la matriz de
        probabilidades de observación, y otro con las probabilidades de
        inicio. Supondremos (no lo comprobamos) que las matrices son 
        coherentes respecto de la  lista de estados y de observables."""
        
        self.estados=estados
        self.observables=observables
        self.a={(si,sj):ptrans
                for (si,l) in zip(estados,mat_trans)
                for (sj,ptrans) in zip(estados,l)}
        self.b={(si,vj):pobs
                for (si,l) in zip(estados,mat_obs)
                for (vj,pobs) in zip(observables,l)}
        self.pi=dict(zip(estados,mat_ini))

# Las variables ej1_hmm y ej2_hmm son objetos de la clase HMM, representando
# respectivamente los ejemplos de modelo oculto de Markov que se dan en las
# diapositivas:

ej1_hmm=HMM(["c","f"],
            [0.8,0.2],
            [[0.7,0.3],[0.4,0.6]],
            [1,2,3],   
            [[0.2,0.4,0.4],[0.5,0.4,0.1]])

          

ej2_hmm=HMM(["l","no l"],
            [0.5,0.5],
            [[0.7, 0.3], [0.3,0.7]],
            ["u","no u"],   
            [[0.9,0.1],[0.2,0.8]])

print(ej1_hmm.b[('c',ej1_hmm.observables[0])])

# ========================================================
# Ejercicio 1
# ========================================================

# El algoritmo de Viterbi se define como sigue:

# Entrada: un modelo oculto de Markov y una secuencia
#          de observaciones, o_1, ..., o_t, 
# Salida: La secuencia de estados más probable, dadas las
#         observaciones. 

# Este algoritmo está explicado en el tema 2 de teoría:

# Inicio: nu(1,si) = b(i)(o1)pi(i) para 1 <= i <= n
#         pr(1,si) = null
# Para k desde 2 a t:
#    Para j desde 1 a n:
#         nu(k,sj) = b(j)(ok) * max([a(i,j) * nu(k-1, si) 
#                                    para 1 <= i <= n]) 
#         pr(k,sj) = argmax([a(i,j) * nu(k-1, si) para 1 <= i <= n])
# Hacer s = argmax([nu(t,si) para 1 <= i <= n])
# Devolver la secuencia de estados que lleva hasta s, usando para ello los
#         punteros almacenados en pr.  


# Se pide: 

# Implementar la función viterbi que use el algoritmo anterior a
# partir de un modelo oculto de Markov y una lista de observaciones,
# calcule la lista: [s_1, ..., s_t] con la sucesión de estados más
# probables usando adecuadamente el algoritmo de Viterbi.

def arg_max(list,estados):
    list_estados = []
    if list[0][0] > list[0][1]:
        list_estados.append(estados[0])
    else:
        list_estados.append(estados[1])
    if list[1][0] > list[1][1]:
        list_estados.append(estados[0])
    else: 
        list_estados.append(estados[1])
    return list_estados

def arg_max_nu(nu_list, pr_list,estados):
    secuencia = []
    for i in range(1,len(nu_list)):
        if nu_list[i][0] > nu_list[i][1]:
            secuencia.append(pr_list[i-1][0])
        else:
            secuencia.append(pr_list[i-1][1])
    if nu_list[-1][0] > nu_list[-1][1]:
        secuencia.append(estados[0])
    else:
        secuencia.append(estados[1])
    return secuencia


def viterbi(hmm,observaciones):
    nu_list = [hmm.b[(e,observaciones[0])]*hmm.pi[e] for e in hmm.estados]
    nu_list_list = [nu_list]
    pr_list = []
    for o in observaciones[1:]:
        pr = [[nu*hmm.a[(e1,e)] for (e1,nu) in zip(hmm.estados,nu_list)] for e in hmm.estados]
        pr_list.append(arg_max(pr,hmm.estados))
        #pr_list = [item for l in pr_list for item in l]
        nu_list = [hmm.b[(e,o)] * max(nu * hmm.a[(e1,e)] for (nu,e1) in zip(nu_list,hmm.estados)) for e in hmm.estados]
        nu_list_list.append(nu_list)
    s = arg_max_nu(nu_list_list,pr_list,hmm.estados)
    return s

print(viterbi(ej1_hmm,[3,1,3,2]))
print(viterbi(ej2_hmm,["u","u","no u"]))

# Ejemplos:


viterbi(ej1_hmm,[3,1,3,2])
# ['c', 'c', 'c', 'c']

# >>> viterbi(ej2_hmm,["u","u","no u"])
# ['l', 'l', 'no l']



# INDICACIÓN: Como ayuda, se proporciona la siguiente función viterbi_pre, que sería una
# versión preliminar de la función que se pide. Esta función preliminar sólo
# calcula los valores nu_k del algoritmo, pero hay que modificarla para
# incluir la "infraestructura" necesaria y poder obtener la secuencia de
# estados más probable.

def viterbi_pre(hmm,observaciones):
        """Versión pre-Viterbi que calcula los nu_k"""
        nu_list=[hmm.b[(e,observaciones[0])]*hmm.pi[e] for e in hmm.estados]
        for o in observaciones[1:]:

            nu_list=[hmm.b[(e,o)]*max(hmm.a[(e1,e)]*nu for (e1,nu) in zip(hmm.estados,nu_list)) 
            for e in hmm.estados]
        return nu_list


# ========================================================
# Ejercicio 2
# ========================================================


# Se pide ahora definir un algoritmo de muestreo para modelos ocultos de
# Markov. Es decir una función muestreo_hmm(hmm,n), que recibiendo un modelo
# oculto de Markov y un número natural n, genera una secuencia de $n$ estados
# y la correspondiente secuencia de $n$ observaciones, siguiendo las
# probabilidades  del modelo. 

# Explicamos a continuación con más detalle este algoritmo de muestreo,
# ilustrándolo con un ejemplo, suponiendo que el modelo oculto de Markov es el
# primer ejemplo que se usa en las diapositivas (el de los helados).

#   El problema es generar una secuencia de estados, con las correspondientes
# observaciones, siguiendo las probabilidades del modelo. Supondremos que
# disponemos de un generador de números aleatorios entre 0 y 1, con
# probabilidad uniforme (es decir, el random de python). Vamos a generar una
# secuencia de 3 estados y la correspondiente secuencia de 3 observaciones.

#   El primer estado ha de ser generado siguiendo el vector de probabilidades
# iniciales. En este caso pi_1=P(c)=0.8 y pi_2=P(f)=0.2. Supongamos que
# al generar un número aleatorio, obtenemos $0.65$. Esto significa que el
# primer estado en nuestra secuencia es $c$.

#   Ahora tenemos que generar la observación correspondiente, y para ello
# usamos las probabilidades de la matriz de observaciones. Puesto que el estado
# actual es c, las probabilidades de generar cada observable son: b_1(1) =
# P(1|c) = 0.2, b_1(2) = P(2|c) = 0.4 y b_1(3) = P(3|c) = 0.4. Si
# obtenemos aleatoriamente el número 0.53, eso significa que la observación
# correspondiente es 2, ya que es la primera de las observaciones cuya
# probabilidad acumulada (0.2+0.4) supera a 0.53.

#   Generamos ahora el siguiente estado. Para ello usamos las probabilidades
# de la matriz de transición. Como el estado actual es c, las probabilidades de
# que cada estado sea generado a continuación son: a_11 = P(c|c) = 0.7 y
# a_12 = P(f|c) = 0.3. Si aleatoriamente obtenemos el número 0.82,
# significa que hemos obtenido f como siguiente estado.

#   Para la siguientes observaciones y estados, procedemos de la misma
# manera. Por ejemplo, si el siguiente número aleatorio que obtenemos es
# 0.29, la observación correspondiente es 1. Si a continuación obtenemos
# los números aleatorios 0.41 y 0.12, el estado siguiente es f y la
# observación sería 1. En resumen, hemos generado la secuencia de estados
# [c,f,f] con la correspondiente secuencia de observaciones [2,1,1].

def cal_e(dic):
    n_random = random.random()
    dif_min = float("infinity")
    for (x,v) in dic.items():
        dif = abs((n_random - v))
        if dif < dif_min:
            dif_min = dif
            estado = x
    return estado

def cal_o(hmm,estado):
    observables = hmm.observables
    n_random = random.random()
    prob = 0
    for i in range(0,len(observables)):
        prob += hmm.b[(estado,observables[i])]
        if prob >= n_random:
            observable = observables[i]
            break
    return observable

def estado_siguiente(hmm,estado):
    n_random = random.random()
    estados = hmm.estados
    prob = 0
    for i in range(0,len(estados)):
        prob += hmm.a[(estado,estados[i])]
        if prob >= n_random:
            sig_estado = estados[i]
            break
    return sig_estado

def muestreo_hmm(hmm,n):
    sec_estados = []
    sec_observaciones = []
    for i in range(n):
        if i == 0:
            sec_estados.append(cal_e(hmm.pi))    
        else:
            sec_estados.append(estado_siguiente(hmm,sec_estados[-1]))
            sec_observaciones.append(cal_o(hmm,sec_estados[-1]))
    return [sec_estados,sec_observaciones]



# Ejemplos (téngase en cuenta que la salida está sujeta a aleatoriedad):


print(muestreo_hmm(ej1_hmm,10))
# [['c', 'c', 'f', 'f', 'c', 'c', 'c', 'c', 'c', 'c'],
#  [2, 1, 1, 1, 3, 2, 1, 2, 3, 1]]

print(muestreo_hmm(ej1_hmm,10))
# [['c', 'c', 'f', 'f', 'f', 'f', 'c', 'c', 'c', 'c'],
#  [1, 1, 1, 1, 3, 1, 2, 3, 2, 3]]


print(muestreo_hmm(ej2_hmm,7))
# [['l', 'l', 'l', 'l', 'no l', 'l', 'l'],
#  ['u', 'u', 'u', 'u', 'no u', 'u', 'u']]

print(muestreo_hmm(ej2_hmm,7))
# [['no l', 'no l', 'no l', 'no l', 'no l', 'no l', 'l'],
#  ['no u', 'no u', 'u', 'no u', 'no u', 'no u', 'u']]


# ========================================================
# Ejercicio 3
# ========================================================

# Vamos ahora a aplicar las dos funciones anteriores para experimentar sobre
# un problema simple de localización de robots que se mueve en una cuadrícula.
# Esta aplicación está descrita en la sección 15.3.2 del libro "Artificial
# Intelligence: A Modern Approach (3rd edition)" de S. Russell y P. Norvig.

# Supongamos que tenemos la siguiente lista de strings, que representa una
# cuadrícula bidimensional, sobre la que se desplaza un robot:

#     ["ooooxoooooxoooxo",
#      "xxooxoxxoxoxoxxx",
#      "xoooxoxxoooooxxo",
#      "ooxoooxooooxoooo"]

# Aquí la "x" representa una casilla bloquedada, y la "o" representa una
# casilla libre en la que puede estar el robot. 

#   El robot puede iniciar su movimiento en cualquiera de las casillas libres,
# con igual probabilidad. En cada instante, el robot se mueve de la casilla en
# la que está a una contigua: al norte, al sur, al este o al oeste, siempre que
# dicha casilla no esté bloqueda. El movimiento del robot está sujeto a
# incertidumbre, pero sabemos que se puede mover con igual probabilidad a cada
# casilla vecina no bloquedada.

#   Desgraciadamente, el robot no nos comunica en qué casilla se encuentra en
# cada instante de tiempo, ni nosotros podemos observarlo. Lo único que el
# robot puede observar en cada casilla son las direcciones hacia las que
# existen obstáculos (es decir, casillas bloqueadas o paredes). Por ejemplo, una
# observación "NS" representa que el robot ha detectado que desde la casilla
# en la que está, al norte y al sur no pueda transitar, pero que sí puede
# hacerlo a las casillas que están al este y al oeste.

#   Para acabar de complicar la cosa, los sensores de obstáculos que tiene el
# robot no son perfectos, y están sujetos a una probabilidad de error.
# Supondremos que hay una probabilidad epsilon de que la detección de
# obstáculo en una dirección sea errónea (y por tanto, hay una probabilidad
# 1-epsilon de que sea correcta). Supondremos también que los errores en
# cada una de las cuatro direcciones son independientes entre sí. Esto nos
# permite calcular la probabilidad de las observaciones dados los estados, como
# ilustramos a continuación.

#   Por ejemplo, supongamos que X y E son, respectivamente, las variables
# aleatorias que indican la casilla en la que está el robot y la observación
# que realiza el robot. Supongamos también que c es una casilla que hacia el
# norte y el este tiene obstáculos, y que tiene casillas transitables al sur y
# al oeste. Si por ejemplo el robot informara que existen obstáculos al sur y
# al este, la probabilidad de esto sería 

#     P(E=SE|X=c) = (epsilon)^2 * (1-epsilon)^2 

# (ya que habría errado en dos direcciones, norte y sur, y acertado en otras
# dos, este y oeste). 

# Por el contrario, la probabilidad de que en ese mismo estado el robot
# informara de obstáculos al norte, sur y este, sería 

#     P(E=NSE|X=c) = epsilon * (1-epsilon)^3 

# (ya que habría errado en una dirección y acertado en tres).




# Se pide:

# Definir una clase Robot, subclase de HMM, cuyo constructor reciba una lista
# de strings del estilo de la del ejemplo anterior, y un error epsilon, generando a
# partir de la misma un objeto de la clase HMM. Importante: se pide hacerlo de 
# manera genérica, no solo para la cuadrícula del ejemplo. 

# Aplicar el algoritmo de Viterbi a varias secuencias de observaciones del robot,
# para estimar las correspondientes secuencias de casillas más probables por
# las que ha pasado el robot, en la cuadrícula del ejemplo.

# Hacer lo mismo para alguna otra cuadrícula, distinta de la del ejemplo. 

# NOTAS: 

# - Representar los estados por pares de coordenadas, en el que la (0,0) sería
#   la casilla de arriba a la izquierda. 
# - Las observaciones las representamos por una tupla (i1,i2,i3,i4), en el que 
#   sus elementos son 0 ó 1, donde 0 indica que no se ha detectado obstáculo, 
#   y 1, indica que sí, respectivamente en  el N,S, E y O (en ese orden). 
#   Por ejemplo (1,1,0,0) indica que se detecta obstáculo en el N y en el S.
#   y (0,0,1,0) indica que se detecta obstáculo solo en el E.    
# - Por simplificar, supondremos que no hay casillas aisladas. 

class Robot(HMM):
    def __init__(self,estados,error):
#lambda x: True if x % 2 == 0 else False

        def distancia(x1,y1,x2,y2):
            if math.sqrt((x2-x1)**2 + (y2-y1)**2) == 1:
                return (1/2)
            else:
                return 0

        self.estados = [(i,j) for i in range(0,len(estados)) for j in range(0,len(estados[i]))]
        self.observables = [(i1,i2,i3,i4) for i1 in range(0,2) for i2 in range(0,2) for i3 in range(0,2) for i4 in range(0,2)]
        self.pi = {(i,j):(1/(len(self.estados)-1)) for i in range(0,len(estados)) for j in range(0,len(estados[i]))} 
        self.a = {((i1,j1),(i2,j2)):(distancia(i1,j1,i2,j2)) for i1 in range(0,len(estados)) for j1 in range(0,len(estados)) 
                                        for i2 in range(0,len(estados)) for j2 in range(0,len(estados))} #Falta mirar los vecinos
        self.b = {}
# Ejemplo de HMM generado para una cuadrícula básica:
    
cuadr0=["ooo",
        "oxo",
        "ooo"]

robot0=Robot(cuadr0,0.1)

print(robot0.estados)
# [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]

print(robot0.observables)

#[(0, 0, 0, 0),(0, 0, 0, 1),(0, 0, 1, 0),(0, 0, 1, 1),(0, 1, 0, 0),
# (0, 1, 0, 1),(0, 1, 1, 0),(0, 1, 1, 1),(1, 0, 0, 0),(1, 0, 0, 1),
# (1, 0, 1, 0),(1, 0, 1, 1),(1, 1, 0, 0),(1, 1, 0, 1),(1, 1, 1, 0),
# (1, 1, 1, 1)]

print(robot0.pi)
# {(0, 0): 0.125, (0, 1): 0.125, (0, 2): 0.125, (1, 0): 0.125,
#  (1, 2): 0.125, (2, 0): 0.125, (2, 1): 0.125, (2, 2): 0.125}


print(robot0.a)
 
#{((0, 0), (0, 0)): 0, ((0, 0), (0, 1)): 0.5, ((0, 0), (0, 2)): 0,
# ((0, 0), (1, 0)): 0.5,((0, 0), (1, 2)): 0, ((0, 0), (2, 0)): 0,
# ((0, 0), (2, 1)): 0, ((0, 0), (2, 2)): 0,
# ((0, 1), (0, 0)): 0.5, ((0, 1), (0, 1)): 0, ((0, 1), (0, 2)): 0.5,
# ((0, 1), (1, 0)): 0, ((0, 1), (1, 2)): 0, ((0, 1), (2, 0)): 0,
# ((0, 1), (2, 1)): 0, ((0, 1), (2, 2)): 0,
# ((0, 2), (0, 0)): 0, ((0, 2), (0, 1)): 0.5,
# ... Continúa .....

# >>> robot0.b
#{((0, 0), (0, 0, 0, 0)): 0.008100000000000001,
# ((0, 0), (0, 0, 0, 1)): 0.07290000000000002,
# ((0, 0), (0, 0, 1, 0)): 0.0009000000000000002,
# ((0, 0), (0, 0, 1, 1)): 0.008100000000000001,
#  ... Continúa ....



# -----------

# Ejemplo de uso de Viterbi en la cuadrícula del ejemplo

cuadr_rn=     ["ooooxoooooxoooxo",
               "xxooxoxxoxoxoxxx",
               "xoooxoxxoooooxxo",
               "ooxoooxooooxoooo"]

robot_rn=Robot(cuadr_rn,0.15)

# Secuencia de 7 observaciones:
seq_rn1=[(1, 1, 0, 0), (0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 0, 1),
         (1, 1, 0, 0),(0, 1, 1, 0),(1, 1, 0, 0)]

# Usando Viterbi, estimamos las casillas por las que ha pasado:

viterbi(robot_rn,seq_rn1)
# [(3, 14), (3, 13), (3, 12), (3, 13), (3, 14), (3, 15), (3, 14)]







# ========================================================
# Ejercicio 4
# ========================================================

# Realizar experimentos para ver cómo de buenas son las secuencias que se
# obtienen con el algoritmo de Viterbi que se ha implementado. Para ello, una
# manera podría ser la siguiente: generar una secuencia de estados y la
# correspondiente secuencia de observaciones usando el algoritmo de
# muestreo. La secuencia de observaciones obtenida se puede usar como entrada
# al algoritmo de Viterbi y comparar la secuencia obtenida con la secuencia de
# estados real que ha generado las observaciones. Se pide ejecutar con varios
# ejemplos y comprobar cómo de ajustados son los resultados obtenidos. Para
# medir el grado de coincidencia entre las dos secuencias de estados, calcular
# la proporción de estados coincidentes, respecto del total de estados de la
# secuencia.


# Por ejemplo:

# Función que calcula el porcentaje de coincidencias:
def compara_secuencias(seq1,seq2):
    return sum(x==y for x,y in zip(seq1,seq2))/len(seq1)


# Generamos una secuencia de 20 estados y observaciones
# >>> seq_e,seq_o=muestreo_hmm(rn_hmm,20)

# >>> seq_o 
# [(0, 0, 1, 1), (0, 1, 1, 0), (1, 1, 0, 0),....]

# >>> seq_e
# [(2, 5),(3, 5), (3, 4), (3, 3), (3, 4), ....]
 
# >>> seq_estimada=viterbi(rn_hmm,seq_o)

# >>> seq_estimada
# [(2, 5),(3, 5),(3, 4),(3, 3),(3, 4),(3, 5),...]
 
# Vemos, cuántas coincidencias hay, proporcinalmente al total de estados de la 
# secuencia:
    
# >>> compara_secuencias(seq_e,seq_estimada)
# 0.95

# -----------------------------------

# Para mecanizar esta experimentación, definir una función

#     experimento_hmm_robot(cuadrícula,epsilon,n,m) 

# que genera el HMM correspondiente a la cuadrícula y al epsilon, y realiza 
# m experimentos, como se ha descrito:
    
# - generar en cada uno de ellos una secuencia de n observaciones y estados 
#  (con muestreo_hmm)
# - con la secuencia de observaciones, llamar a viterbi para estimar la 
#   secuencia de estados más probable
# - calcular qué proporción de coincidencias hay entre la secuencia de estados real 
#   y la que ha estimado viterbi 
# Y devuelvela media de los m experimentos. 

# Experimentar al menos con la cuadrícula del ejemplo y con varios valores de
# n, con varios valores de epsilon y con un m suficientemente grande para que 
# la media devuelta sea significativa del rendimiento del algoritmo. 




