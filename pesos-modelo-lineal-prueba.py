#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# AMPLIACIÓN DE INTELIGENCIA ARTIFICAL


# EJERCICIO PARA EL JUEVES 16-04-2020 (voluntario, recomendado para seguir mejor 
# la clase)

# Usando los datos del fichero csv que se acompaña, en el que la última columna 
# es el dato a predecir, a partir de los datos de las diez primeras columnas.

# Decidir cuál de estos cinco vectores de pesos que se listan a continuación es mejor, 
# atendiendo al error cuadrático que cometen sobre los 90 primeros ejemplos del 
# conjunto de entrenamiento.

# Comprobar también si el mejor vector de pesos con respecto a esos 90 ejemplos
# es también el mejor con respecto a los diez últimos.  

import csv, random


w1=[-1.29534026,  1.23835128,  0.12877138, -2.96549057, -0.35841744,
    2.82746578,  2.21482984, -1.65336872, -0.47153383, -0.44702348,
   -3.3547648 ]

w2=[ 3.89328892,  1.35129463, -2.53506133, -2.04672724,  1.45909327,
            3.23755072, -0.15481467,  0.09800942,  2.73737855,  4.53587465,
            -0.0633372 ]


w3=[-2.44018926,  0.99262032, -1.3226565 , -2.07167792,  2.2708178 ,
            3.11581296,  1.76699122,  1.25716116,  1.04054152, -0.60208891,
            -1.01754336]

w4=[ 1.61374819, -2.08690754,  1.58248754,  2.95886602, -0.31980219,
            2.31724431, -2.31581768, -2.79049173,  1.43366351, -1.12239852,
            -1.333636  ]
 
w5=[ 3.75038563, -1.05615946, -1.46526707,  2.11298963, -0.5708379 ,
             1.55773606, 1.11062204,  2.65842872,  3.13673974, -1.91793153,
            -1.83749571]

#Resuelto con python
def lee_datos(fichero):
    with open(fichero,newline="") as f:
        lectordatos = csv.reader(f,delimiter=',',quoting=csv.QUOTE_NONNUMERIC)
        datos,valores = [],[]
        for fila in lectordatos:
            datos.append([1]+fila[:-1])
            valores.append(fila[-1])
    return datos,valores

datos,valores = lee_datos("datos-aia-prueba.csv")

X_train = datos[:90]
y_train = valores[:90]
X_test = datos[90:]
y_test = valores[90:]

def combinacion_lineal(w,x):
    return sum(wi*xi for wi,xi in zip(w,x))

def error_cuadratico_medio(X,y,w):
    return sum((yj-combinacion_lineal(w,Xj))**2 for Xj,yj in zip(X,y))/len(X)

print("Set de entrenamiento")
print(error_cuadratico_medio(X_train,y_train,w1))
print(error_cuadratico_medio(X_train,y_train,w2))
print(error_cuadratico_medio(X_train,y_train,w3))
print(error_cuadratico_medio(X_train,y_train,w4))
print(error_cuadratico_medio(X_train,y_train,w5))
print(len(X_train))
print("\nSet de test")
print(error_cuadratico_medio(X_test,y_test,w1))
print(error_cuadratico_medio(X_test,y_test,w2))
print(error_cuadratico_medio(X_test,y_test,w3))
print(error_cuadratico_medio(X_test,y_test,w4))
print(error_cuadratico_medio(X_test,y_test,w5))

#Descenso estocástico por el gradiente
def aprende_pesos(train,valor_train,rango_inicial,n_epochs,tasa):
    n_atributos = len(train[0])
    #Si tenemos un set de entrenaiento con x columnas, el vector de pesos tiene que tener x+1
    w = [random.uniform(-rango_inicial,rango_inicial) for _ in range(n_atributos)]  
    indices = list(range(len(train)))
    #epochs = pasadas completas al set de entrenamiento
    for n in range(n_epochs):
        #Reorganizamos los índices. Li hacemos para escapar de los óptimos locales
        random.shuffle(indices)
        #w = [wi + tasa*xi*e for xi,wi in zip(Xj, w)]
        for j in indices:
            x = train[j]
            y_esperado = valor_train[j]
            y_predict = combinacion_lineal(w,x)
            for i in range(n_atributos):
                w[i]+=tasa*(y_esperado-y_predict)*x[i]
            #print("Pesos {}".format(w))
            #print("Error cuadrático: {}".format(error_cuadratico_medio(X_train,y_train,w)))
    return w    

print(aprende_pesos(X_train,y_train,4,20,0.01))