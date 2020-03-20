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
# * estados: Una lista con los estados que definen la variable oculta
#             del modelo.
#             [s_1, ..., s_n]
# * Observables: Una lista con los estados que definen la variable
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
class HMM:
    
    def __init__(self,estados,matriz_inicial,matriz_transicion,observables,matriz_observacion):
        """Constructor MHH"""
        self.estados = estados
        self.observables = observables
        self.pi = dict(zip(estados, matriz_inicial)) #pi = probabilidades inicial
        self.a = {(si,sj):p for si,l in zip(estados,matriz_transicion) for sj,p in zip(estados,l)}
        self.b = {(si,vj):p for si,l in zip(estados,matriz_observacion) for vj,p in zip(observables,l)}


#---------------------------------------------------------------------
# Ejercicio 1.2
#---------------------------------------------------------------------

# Comprobar a partir de los dos ejemplos de modelo oculto de Markov
# vistos en teoría la correcta definición de la clase anterior.

ej1_hmm = HMM(["c","f"], #estados
              [0.8,0.2], #probabilidades iniciales
              [[0.7,0.3],[0.4,0.6]], #a
              [1,2,3], #percepciones
              [[0.2,0.4,0.4],[0.5,0.4,0.1]]) #b

ej2_hmm = HMM(["l","no l"], #estados
              [0.5,0.5], #probabilidades iniciales
              [[0.7,0.3],[0.3,0.7]], #a
              ["u","no u"], #percepciones
              [[0.9,0.1],[0.2,0.8]]) #b

print(ej1_hmm.a)
print(ej2_hmm.b)
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

def avance(hmm,observaciones):
    alpha_list = [hmm.b[(e,observaciones[0])]*hmm.pi[e] for e in hmm.estados]
    for o in observaciones[1:]:
        alpha_list = [hmm.b[(e,o)] * sum(alpha * hmm.a[(e1,e)] for alpha,e1 in zip(alpha_list,hmm.estados)) 
        for e in hmm.estados]
    p_seq_obs = sum(alpha_list) 
    alpha_list_n = [alpha / p_seq_obs for alpha in alpha_list] #Normalizar
    return p_seq_obs,alpha_list_n

#Otra opcion es que normalizar en cada paso. Al final es lo mismo debido a la proporción
#Si lo hago al final, es lo mismo ya que la alfa que obtengo es el producto de las alfas
#Inverso del alfa me da la probabilidad

print(avance(ej1_hmm,[3,1,3,2]))
print(avance(ej2_hmm,["u","u","no u"]))

#---------------------------------------------------------------------
# Ejercicio 2.2
#---------------------------------------------------------------------

# Definir la función avance_norm que implementa la versión modificada
# del algoritmo de avance, en el que en cada iteración se normalizan
# las probabilidades calculadas. Igual que en el apartado anterior, se
# deben calcular tanto la probabilidad de la secuencia de
# observaciones P(E_1 = o_1,..., E_t = o_t), como la lista con las
# probabilidades P(X_t = s_i | E_1 = o_1, ...,E_t = o_t), 1 <= i <= n.

def avance_norm(hmm,observaciones):
    alpha_list = [hmm.b[(e,observaciones[0])]*hmm.pi[e] for e in hmm.estados]
    for o in observaciones[1:]:
        alpha_list = [hmm.b[(e,o)] * sum(alpha * hmm.a[(e1,e)] for alpha,e1 in zip(alpha_list,hmm.estados)) 
        for e in hmm.estados]
        p_seq_obs = sum(alpha_list) 
        alpha_list_n = [alpha / p_seq_obs for alpha in alpha_list] #Normalizar
    return p_seq_obs,alpha_list_n


print(avance_norm(ej1_hmm,[3,1,3,2]))
print(avance_norm(ej2_hmm,["u","u","no u"]))

#---------------------------------------------------------------------
# Ejercicio 2.3
#---------------------------------------------------------------------
    
# Utilizar la función anterior para, en el problema 10 del boletín,
# comprobar la convergencia de la probabilidad de que haya dormido lo
# suficiente la noche anterior para un estudiante muestra todos los
# días los ojos rojos y se duerme en clase,

#COMPLETAR

ej10_hmm = HMM(["d","n d"],
               [0.6,0.4],
               [[0.8,0.2],[0.2,0.8]],
               ["ojos rojos","duerme clase"],
               [[0.2,0.7],[0.1,0.3]])


#=====================================================================
# Parte III: Algoritmo de Viterbi
#=====================================================================

# El algoritmo de Viterbi se define como sigue:

# Viterbi es como avance pero donde hay un sumatorio hay un maximo

# Entrada: un modelo oculto de Markov y una secuencia
#          de observaciones, o_1, ..., o_t, 
# Salida: La secuencia de estados más probable, dadas las
#         observaciones. 

# Este algoritmo está explicado en el tema 4 de teoría:

# Inicio: nu(1,si) = b(i)(o1)pi(i) para 1 <= i <= n
#         pr(1,si) = null
# Para k desde 2 a t:
#    Para j desde 1 a n:
#         nu(k,sj) = b(j)(ok) * max([a(i,j) * nu(k-1, si) 
#                                    para 1 <= i <= n]) 
#         pr(k,sj) = argmax([a(i,j) * nu(k-1, si) para 1 <= i <= n])
# Hacer s = argmax([nu(t,si) para 1 <= i <= n])
# Devolver la secuencia de estados que lleva hasta s

#---------------------------------------------------------------------
# Ejercicio 3.1
#---------------------------------------------------------------------

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
    list_estados = []
    if nu_list[0][0] > nu_list[0][1]:
        list_estados.append(estados[0])
    else:
        list_estados.append(estados[1])
    for nu in range(1,len(nu_list)):
        if nu_list[nu][0] > nu_list[nu][1]:
            list_estados.append(pr_list[nu-1][0])
        else:
            list_estados.append(pr_list[nu-1][1])
    return list_estados

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
#---------------------------------------------------------------------
# Ejercicio 3.2
#---------------------------------------------------------------------

# Utilizar los ejemplos vistos en la teoría para comprobar la correcta
# definición de la función anterior.






