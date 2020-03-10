# Ampliación de Inteligencia Artificial 
# Práctica de modelos ocultos de Markov
# Dpto. de C. de la Computación e I.A. (Univ. de Sevilla)
#=====================================================================




#=====================================================================
# Parte I: Representación: modelos ocultos de Markov
#=====================================================================

#---------------------------------------------------------------------
# Ejercicio 1.1
#---------------------------------------------------------------------

# Definir en primer lugar la clase HMM para la representación en
# Python de los modelos ocultos de Markov.

# La clase ha de constar de los siguientes atributos:

# Atributos:
# * eOcultos: Una lista con los estados que definen la variable oculta
#             del modelo.
#             [s_1, ..., s_n]
# * eObservables: Una lista con los estados que definen la variable
#                 observable del modelo.
#                 [v_1, ..., v_m]
# * pi: Un diccionario, cuyas claves son los estados, y cuyos valores
#       son las probabilidades iniciales:
#                pi[s_i] = P(X_1 = s_i)
# * a: Un diccionario cuyas claves son parejas (tuplas) de estados y
#      cuyos valores son las correspondientes probabilidades de la
#      matriz de transición:
#      a[(s_i, s_j)] = P(X_t = s_j | X_{t-1} = s_i)
# * b: Un diccionario cuyas claves son parejas (tuplas) de estado y
#      observable, y cuyos valores son las correspondientes
#      probabilidades de la matriz de observación:
#      b[(s_i,v_j)] = P(E_t = v_j | X_{t-1} = s_i)

# El constructor de la clase ha de recibir los siguientes datos:

# * Una lista con los estados de la variable oculta.
#   [s_1, ..., s_n]
# * Una lista con las correspondiente probabilidades a priori
#   [P(X_1 = s_1), ..., P(X_1 = s_n)]
# * Una lista de listas representando la matriz de transición
#   [[P(X_t = s_1 | X_{t-1} = s_1), ..., P(X_t = s_n | X_{t-1} = s_1)],
#    ...
#    [P(X_t = s_1 | X_{t-1} = s_n), ..., P(X_t = s_n | X_{t-1} = s_n)]]
# * Una lista con los estados de la variable observable.
#   [v_1, ..., v_m]
# * Un lista de listas representando la matriz de observación
#   [[P(E_t = v_1 | X_t = s_1), ..., P(E_t = v_m | X_t = s_1)],
#    ...
#    [P(E_t = v_1 | X_t = s_n), ..., P(E_t = v_m | X_t = s_n)]]






#---------------------------------------------------------------------
# Ejercicio 1.2
#---------------------------------------------------------------------

# Comprobar a partir de los dos ejemplos de modelo oculto de Markov
# vistos en teoría la correcta definición de la clase anterior.




#=====================================================================
# Parte II: Algoritmo de avance
#=====================================================================

# El algoritmo de avance se define como sigue:

# Entrada: un modelo oculto de Markov y una secuencia
#          de observaciones, o_1, ..., o_t, 
# Salida: probabilidades P(X_t = s_i, E_1 = o_1, ..., E_t = o_t), 
#         1 <= i <= n 

# Inicio: alpha(1,si) = b(i)(o1)pi(i) para 1 <= i <= n
# Para k desde 2 a t:
#    Para j desde 1 a n:
#         alpha(k,sj) = b(j)(ok) * sum([a(i,j) * alpha(k-1, si) 
#                                       para 1 <= i <= n]) 
# Devolver los alpha(t, si) para 1 <= i <= n

# Una vez que se tienen los alpha(t,si), se puede calcular tanto 
# P(E_1 = o_1, ..., E_t = o_t) como  
# P(X_t = s_i | E_1 = o_1, ..., E_t = o_t)
# (respectivamente, sumando y normalizando para i=1,...,n).   

#---------------------------------------------------------------------
# Ejercicio 2.1
#---------------------------------------------------------------------

# Definir la función "avance", que a partir de un modelo oculto de
# Markov y una secuencia de observaciones o_1, ..., o_t, calcule tanto
# la probabilidad de la secuencia de observaciones P(E_1 = o_1,...,
# E_t = o_t), como la lista con las probabilidades P(X_t = s_i | E_1 =
# o_1, ...,E_t = o_t), 1 <= i <= n utilizando adecuadamente el
# algoritmo de avance anteriormente descrito.

# Probarlo con los ejemplos vistos en clase. 


#---------------------------------------------------------------------
# Ejercicio 2.2
#---------------------------------------------------------------------

# Definir la función avance_norm que implementa la versión modificada
# del algoritmo de avance, en el que en cada iteración se normalizan
# las probabilidades calculadas. Igual que en el apartado anterior, se
# deben calcular tanto la probabilidad de la secuencia de
# observaciones P(E_1 = o_1,..., E_t = o_t), como la lista con las
# probabilidades P(X_t = s_i | E_1 = o_1, ...,E_t = o_t), 1 <= i <= n.





#---------------------------------------------------------------------
# Ejercicio 2.3
#---------------------------------------------------------------------
    
# Utilizar la función anterior para, en el problema 10 del boletín,
# comprobar la convergencia de la probabilidad de que haya dormido lo
# suficiente la noche anterior para un estudiante muestra todos los
# días los ojos rojos y se duerme en clase,



