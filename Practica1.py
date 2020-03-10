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
#print(psr_n4.restricciones)
# {(1, 2): <function <lambda> at ...>,
#  (1, 3): <function <lambda> at ...>,
#  (1, 4): <function <lambda> at ...>,
#  (2, 3): <function <lambda> at ...>,
#  (3, 4): <function <lambda> at ...>,
#  (2, 4): <function <lambda> at ...>}
# >>> psr_n4.vecinos
# {1: [2, 3, 4], 2: [1, 3, 4], 3: [1, 2, 4], 4: [1, 2, 3]}
#print(psr_n4.restricciones[(1,4)](2,3))
# True
#print(psr_n4.restricciones[(1,4)](4,1))
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

def psr_backtracking(psr):

    def consistente(var,val,asig):
        for x in asig:
            if(var,x) in psr.restricciones:
                if not psr.restricciones[(var,x)](val,asig[x]):
                    return False
            elif (x,var) in psr.restricciones[(x,var)](asig[x],val):
                if not psr.restricciones[(x,var)](asig[x],val):
                    return False
        return True

    def psr_backtracking_rec(asig,resto):
        if resto == []:
            return asig
        else:
            var = resto[0]
            nuevo_resto = resto[1:]
            dom_var = psr.dominios[var]
            for val in dom_var:
                if consistente(var,val,asig):
                    asig[var] = val
                    result = psr_backtracking_rec(asig,nuevo_resto)
                    if result:
                        return result
                    del asig[var]
            return None

    return psr_backtracking_rec(dict(),psr.variables)

#print(psr_backtracking(n_reinas(4)))

def argmin_dict_rnd(dic,fn):
    """Devuelve la clave de un diccionario dic, cuyo valor asociado en el
    diccionario es el menor valor de fn de todas las claves.
    Deshace empates aleatoriamente."""

    lista_claves_min = list()
    minimo = float("infinity")
    for (x,v) in dic.items():
        val = fn(v)
        if val < minimo:
            minimo = val
            lista_claves_min = [x]
        elif fn(v) == minimo:
            lista_claves_min.append(x)
    return random.choice(lista_claves_min)

def argmin_dict_max_restr(dic,restr,fn):
    lista_claves_min = list()
    minimo = float("infinity")
    for (x,v) in dic.items():
        val = fn(v)
        if val < minimo:
            minimo = val
            lista_claves_min = [x]
        elif fn(v) == minimo:
            lista_claves_min.append(x)
    if len(lista_claves_min) > 1:
        minimo = float("-inf")
        n_apariciones = dict()
        for var in lista_claves_min:
            contador = 0
            for (x,y) in restr:
                if x == var or y == var:
                    contador +=1
            n_apariciones[var] = contador
        for (k,v) in n_apariciones.items():
            if v > minimo:
                minimo= v
                minima_clave = k
    return minima_clave

def mrv(doms):
    return argmin_dict_rnd(doms,len)

def mrv2(doms,restr):
    return argmin_dict_max_restr(doms,restr,len)

def algun_dominio_vacio(doms):
    return any((not d for d in doms.values()))

def forward_checking(psr,var,val,doms):
    ndoms = dict()
    for x in doms:
        if (var,x) in psr.restricciones:
            ndoms[x] = [v for v in doms[x]
                        if psr.restricciones[(var,x)](val,v)]
        elif (x,var) in psr.restricciones:
            ndoms[x] = [v for v in doms[x]
                        if psr.restricciones[(x,var)](v,val)]
        else:
            ndoms[x] = doms[x][:]
    return ndoms

def psr_backtracking_fc_mrv(psr):
    """Backtracking para problemas de satisfacción de restricciones, usando
    forward checking y mrv (con desempate aleatorio) para seleccionar la
    siguiente variable a asignar. Como orden para recorrer los valores de la
    variable seleccionada, se tomará el orden en el que se dan en el
    dominio"""

    def psr_backtracking_fc_mrv_rec(asig,doms):
        if len(asig) == len(psr.variables):
            return asig
        elif algun_dominio_vacio(doms):
            return None
        else:
            var = mrv(doms)
            dom_var = doms[var]
            del doms[var]
            for val in dom_var:
                asig[var] = val
                doms_fc = forward_checking(psr,var,val,doms)
                result = psr_backtracking_fc_mrv_rec(asig,doms_fc)
                if result is not None:
                    return result
            del asig[var]
            return None

    return psr_backtracking_fc_mrv_rec(dict(),copy.deepcopy(psr.dominios))#copy.deepcopy guarda una copia de la variable

#print(psr_backtracking_fc_mrv(coloreado_mapa(mapa_andalucia,colores_disp)))

# ===================================================================
# Parte II: Algoritmo de consistencia de arcos AC3
# ===================================================================

#   En esta parte vamos a definir el algoritmo de consistencia de arcos
# AC3 que, dado un problema de satisfacción de restricciones,
# devuelve una representación equivalente que cumple la propiedad de
# ser arco consistente (y que usualmente tiene dominios más
# reducidos.)

#   Dado un PSR, un arco es una restricción cualquiera del problema,
# asociada con una de las variables implicadas en la misma, a la que
# llamaremos variable distinguida.





# ===================================================================
# Ejercicio 2
# ===================================================================

#   Definir una función restriccion_arco que, dado un PSR, la
# variable distinguida de un arco y la variable asociada; devuelva
# una función que, dado un elemento del dominio de la variable
# distinguida y otro de la variable asociada, determine si verifican
# la restricción asociada al arco.

# Ejemplos:

# >>> restriccion_arco(psr_n4, 1, 2)
# <function n_reinas.<locals>.n_reinas_restriccion.<locals>.<lambda>
# at 0x7fdfa13d30d0>
# >>> restriccion_arco(psr_n4, 1, 2)(1, 4)
# True
# >>> restriccion_arco(psr_n4, 1, 2)(3, 2)
# False
def restriccion_arco(psr,x,y):

    if (x,y) in psr.restricciones:
        return psr.restricciones[(x,y)]
    else:
        return lambda u,v: psr.restricciones[(y,x)](u,v) #Me permite comprobar la restriccion con los argumentos
                                                         #en el orden en el que están en el arco

# ===================================================================
# Ejercicio 3
# ===================================================================

#   Definir un método arcos para la clase PSR que construya un
# conjunto con todos los arcos asociados al conjunto de restricciones
# del problema. Utilizaremos las tuplas para representar a los
# arcos. El primer elemento será la variable distinguida y el segundo
# la variable asociada.

def arcos(psr):
    return {(x,y) for x in psr.variables for y in psr.vecinos[x]} #También se puede recorrer las restricciones
# Ejemplo:

#psr_n4 = n_reinas(4)
#arcos_n4 = arcos(psr_n4)
#print(arcos_n4)
# [(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (3, 4), (4, 3),
#  (2, 4), (4, 2), (1, 4), (4, 1)]
# >>> psr_n4.restriccion_arco(1, 2)(4, 1)
# True
# >>> psr_n4.restriccion_arco(1, 2)(2, 3)
# False

# ===================================================================
# Ejercicio 4
# ===================================================================

#   Definir la función AC3(psr,doms) que, recibiendo como entrada una
# instancia de la clase PSR y diccionario doms que a cada variable
# del problema le asigna un dominio, aplica el algoritmo de
# consistencia de arcos AC3 a los dominios recibidos (ver tema 1).

# NOTA: La función AC3 debe actualizar los dominios de forma
# destructiva (es decir, después de ejecutar la llamada "AC3(psr,
# doms)", en el diccionario doms debe quedar actualizados.

        
def AC3(psr,doms):
    cola = arcos(psr)
    while cola:
        (x,y) = cola.pop()
        func = restriccion_arco(psr, x,y)
        dom_nuevo = []
        modificado = False
        for vx in doms[x]:
            if any(func(vx,vy) for vy in doms[y]):
                dom_nuevo.append(vx)
            else:
                modificado = True
        if modificado:
            doms[x] = dom_nuevo
            cola.update({(z,x) for z in psr.vecinos[x] if z != y}) #Y son las variables que no cumplen la restriccion 
    
# Ejemplos:

#psr_n4=n_reinas(4)
#dominios = {1:[2,4],2:[1,2,3,4],3:[1,2,3,4],4:[1,2,3,4]}
#print(AC3(psr_n4, dominios))
# >>> dominios
# {1: [2, 4], 2: [1, 4], 3: [1, 3], 4: [1, 3, 4]}

# >>> dominios = {1:[1],2:[1,2,3,4],3:[1,2,3,4],4:[1,2,3,4]}
# >>> AC3(psr_n4,dominios)
# >>> dominios
# {1: [], 2: [], 3: [], 4: []}

# >>> dominios = {1:[1,2,3,4],2:[3,4],3:[1,4],4:[1,2,3,4]}
# >>> AC3(psr_n4,dominios)
# >>> dominios
# {1: [2], 2: [4], 3: [1], 4: [3]}







# ===================================================================
# Parte III: Algoritmo de búsqueda AC3
# ===================================================================


# ===================================================================
# Ejercicio 5
# ===================================================================


# Definir una función parte_dominio(doms), que a partir de un diccionario doms
# en el que cada variable del problema tiene asignado un dominio de posibles
# valores (como los que obtiene el algoritmo AC-3 anterior), devuelve dos
# diccionarios obtenidos partiendo en dos el primero de los dominios que no
# sea unitario.   

# Nota: Supondremos que el diccionario doms que se recibe no tiene dominios
# vacíos y que al menos uno de los dominios no es unitario. El método para
# partir en dos el dominio se deja a libre elección (basta con que sea una
# partición en dos). 

def parte_dominios(doms):
    doms_copia = doms.copy()
    doms_copia_2 = doms.copy()
    for x in doms:
        if len(doms[x]) > 1:
            doms_copia[x] = [doms[x][0]]
            doms_copia_2[x] = doms[x][1:]
        return doms_copia,doms_copia_2
 

# Ejemplo:

dom4 = doms4_1={1: [2, 4], 2: [1, 4], 3: [1, 3], 4: [1, 3, 4]}
res = parte_dominios(dom4)
print(res)


# ({1: [2], 2: [1, 4], 3: [1, 3], 4: [1, 3, 4]}, {1: [4], 2: [1, 4], 3: [1, 3], 4: [1, 3, 4]})







# ===================================================================
# Ejercicio 6
# ===================================================================

# Definir la función búsqueda_AC3(psr), que recibiendo como entrada un psr
# (tal y como se define en el ejercicio 1), aplica el algoritmo de búsqueda
# AC-3 tal y como se define en el tema 2
def todos_dominios_unitarios(doms):
    return all(len(d) == 1 for d in doms.values())

def ningun_dominio_vacio(doms):
    return all(doms.values())

def busqueda_AC3(psr):
    abiertos = [psr.dominios.copy()]
    while abiertos:
        actual = abiertos.pop()
        AC3(psr,actual)
        if ningun_dominio_vacio(actual):
            if todos_dominios_unitarios(actual):
                return {var:dom[0] for var,dom in actual.items()}
            else:
                abiertos.extend(parte_dominios(actual)) #extend concatena 2 listas
    else:
        print("No hay solución")


# Ejemplos:

psr_nreinas4=n_reinas(4)
print(busqueda_AC3(psr_nreinas4))
# {1: 3, 2: 1, 3: 4, 4: 2}
psr_nreinas3=n_reinas(3)
print(busqueda_AC3(psr_nreinas3))
# No hay solución






# ===================================================================
# Ejercicio 7
# ===================================================================



#   En este ejercicio no se pide ninguna función. Tan sólo comprobar el
# algoritmo resolviendo diversas instancias del problema de las 
# n_reinas. Para visualizar las soluciones, puede ser útil la siguiente
# función:

def dibuja_tablero_n_reinas(asig):

    def cadena_fila(i,asig):
        cadena="|"
        for j in range (1,n+1):
            if asig[i]==j:
                cadena += "X|"
            else:
                cadena += " |"
        return cadena

    n=len(asig)
    print("+"+"-"*(2*n-1)+"+")
    for i in range(1,n):
        print(cadena_fila(i,asig))
        print("|"+"-"*(2*n-1)+"|")
    print(cadena_fila(n,asig))
    print("+"+"-"*(2*n-1)+"+")

# Ejemplos:


print(dibuja_tablero_n_reinas(busqueda_AC3(n_reinas(4))))
# +-------+
# | | |X| |
# |-------|
# |X| | | |
# |-------|
# | | | |X|
# |-------|
# | |X| | |
# +-------+

# >>> dibuja_tablero_n_reinas(busqueda_AC3(n_reinas(6)))
# +-----------+
# | | | | |X| |
# |-----------|
# | | |X| | | |
# |-----------|
# |X| | | | | |
# |-----------|
# | | | | | |X|
# |-----------|
# | | | |X| | |
# |-----------|
# | |X| | | | |
# +-----------+

# >>> dibuja_tablero_n_reinas(busqueda_AC3(n_reinas(8)))
# +---------------+
# | | | | | | | |X|
# |---------------|
# | | | |X| | | | |
# |---------------|
# |X| | | | | | | |
# |---------------|
# | | |X| | | | | |
# |---------------|
# | | | | | |X| | |
# |---------------|
# | |X| | | | | | |
# |---------------|
# | | | | | | |X| |
# |---------------|
# | | | | |X| | | |
# +---------------+

# >>> dibuja_tablero_n_reinas(busqueda_AC3(n_reinas(14)))
# +---------------------------+
# | | | | | | | | | | | | | |X|
# |---------------------------|
# | | | | | | | | | | | |X| | |
# |---------------------------|
# | | | | | | | | | |X| | | | |
# |---------------------------|
# | | | | | | | |X| | | | | | |
# |---------------------------|
# | | |X| | | | | | | | | | | |
# |---------------------------|
# | | | | |X| | | | | | | | | |
# |---------------------------|
# | |X| | | | | | | | | | | | |
# |---------------------------|
# | | | | | | | | | | |X| | | |
# |---------------------------|
# |X| | | | | | | | | | | | | |
# |---------------------------|
# | | | | | |X| | | | | | | | |
# |---------------------------|
# | | | | | | | | | | | | |X| |
# |---------------------------|
# | | | | | | | | |X| | | | | |
# |---------------------------|
# | | | | | | |X| | | | | | | |
# |---------------------------|
# | | | |X| | | | | | | | | | |
# +---------------------------+