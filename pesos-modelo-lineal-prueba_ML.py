#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:47:08 2020

@author: jruiz
"""

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

#Creo un DataFrame
df = pd.read_csv('datos-aia-prueba.csv', header=None)

#Creo el y_train
y_train = df.iloc[:90,-1]
y_test = df.iloc[90:,-1]

#Elimino la última columna
df = df.drop(columns=[10])

#Creo el set de entrenamiento y el de test
X_train = df.iloc[:90]
X_test = df.iloc[90:] 



#def f_err_cuad (w, x):
#     return (x[-1] - (w[0] + np.dot(np.array(w[1:]), np.array(x[:-1]))))**2




