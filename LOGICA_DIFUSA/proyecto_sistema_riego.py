#  Sistema de Riego Automatizado Basado en Lógica Difusa

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definir las variables difusas
temperatura_aire = ctrl.Antecedent(np.arange(0, 46, 1), 'temperatura_aire')  # 0 a 45 °C
humedad_suelo = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad_suelo')  # 0 a 100 %
tipo_cultivo = ctrl.Antecedent(np.arange(0, 3, 1), 'tipo_cultivo')  # 0: hortaliza, 1: cereales, 2: flores
cantidad_agua = ctrl.Consequent(np.arange(0, 13, 1), 'cantidad_agua')  # 0 a 12 litros/m²/día

# Funciones de membresía

# Conjuntos difusos para temperatura_aire
temperatura_aire['baja'] = fuzz.trapmf(temperatura_aire.universe, [0, 0, 10, 20])
temperatura_aire['media'] = fuzz.trimf(temperatura_aire.universe, [10, 20, 30])
temperatura_aire['alta'] = fuzz.trapmf(temperatura_aire.universe, [20, 30, 45, 45])

# Conjuntos difusos para humedad_suelo
humedad_suelo['seca'] = fuzz.trapmf(humedad_suelo.universe, [0, 0, 30, 50])
humedad_suelo['humeda'] = fuzz.trimf(humedad_suelo.universe, [30, 55, 80])
humedad_suelo['saturada'] = fuzz.trapmf(humedad_suelo.universe, [55, 80, 100, 100])

# Conjuntos difusos para tipo_cultivo
tipo_cultivo['hortaliza'] = fuzz.trimf(tipo_cultivo.universe, [0, 0, 0])
tipo_cultivo['cereales'] = fuzz.trimf(tipo_cultivo.universe, [1, 1, 1])
tipo_cultivo['flores'] = fuzz.trimf(tipo_cultivo.universe, [2, 2, 2])

# Conjuntos difusos para cantidad_agua
cantidad_agua['baja'] = fuzz.trapmf(cantidad_agua.universe, [0, 0, 3, 6])
cantidad_agua['media'] = fuzz.trimf(cantidad_agua.universe, [3, 6, 9])
cantidad_agua['alta'] = fuzz.trapmf(cantidad_agua.universe, [6, 9, 12, 12])

# Visualizar las funciones de membresía
temperatura_aire.view()
humedad_suelo.view()
tipo_cultivo.view()
cantidad_agua.view()

plt.show()

# Reglas de inferencia
reglas = [
    ctrl.Rule(temperatura_aire['baja'] & humedad_suelo['seca'], cantidad_agua['alta']),
    ctrl.Rule(temperatura_aire['baja'] & humedad_suelo['humeda'], cantidad_agua['baja']),
    ctrl.Rule(temperatura_aire['baja'] & humedad_suelo['saturada'], cantidad_agua['baja']),
    ctrl.Rule(temperatura_aire['media'] & humedad_suelo['seca'], cantidad_agua['alta']),
    ctrl.Rule(temperatura_aire['media'] & humedad_suelo['humeda'], cantidad_agua['media']),
    ctrl.Rule(temperatura_aire['media'] & humedad_suelo['saturada'], cantidad_agua['baja']),
    ctrl.Rule(temperatura_aire['alta'] & humedad_suelo['seca'], cantidad_agua['alta']),
    ctrl.Rule(temperatura_aire['alta'] & humedad_suelo['humeda'], cantidad_agua['media']),
    ctrl.Rule(temperatura_aire['alta'] & humedad_suelo['saturada'], cantidad_agua['media']),
    
    ctrl.Rule(temperatura_aire['media'] & humedad_suelo['humeda'] & tipo_cultivo['hortaliza'], cantidad_agua['media']),
    ctrl.Rule(temperatura_aire['alta'] & humedad_suelo['humeda'] & tipo_cultivo['cereales'], cantidad_agua['media']),
    ctrl.Rule(temperatura_aire['media'] & humedad_suelo['seca'] & tipo_cultivo['flores'], cantidad_agua['alta']),
    ctrl.Rule(temperatura_aire['alta'] & humedad_suelo['seca'] & tipo_cultivo['flores'], cantidad_agua['alta']),
    ctrl.Rule(temperatura_aire['baja'] & humedad_suelo['humeda'] & tipo_cultivo['hortaliza'], cantidad_agua['baja']),
    ctrl.Rule(temperatura_aire['media'] & humedad_suelo['seca'] & tipo_cultivo['cereales'], cantidad_agua['alta']),
]

# Crear el sistema de control
sistema_riego = ctrl.ControlSystem(reglas)
simulador = ctrl.ControlSystemSimulation(sistema_riego)

# Menu para ingresar los valores de entrada
print("Sistema de Riego Automatizado Basado en Lógica Difusa")
print("=================Valores de Entrada==================")
temperatura = float(input("Temperatura del aire (0-45 °C): "))
humedad = float(input("Humedad del suelo (0-100 %): "))
cultivo = int(input("Tipo de cultivo (0: hortaliza, 1: cereales, 2: flores): "))

simulador.input['temperatura_aire'] = temperatura
simulador.input['humedad_suelo'] = humedad
simulador.input['tipo_cultivo'] = cultivo

# Calcular la cantidad de agua
simulador.compute()

# Defuzzificar el resultado y mostrar la cantidad de agua recomendada
cantidad_agua_recomendada = simulador.output['cantidad_agua']
print(f"La cantidad de agua recomendada es: {cantidad_agua_recomendada:.2f} litros/m²/día")

# Graficar la salida de la inferencia (cantidad de agua)
fig, ax = plt.subplots(figsize=(10, 6))

# Interpolar la membresía para todo el universo de la cantidad de agua
baja = fuzz.interp_membership(cantidad_agua.universe, cantidad_agua['baja'].mf, cantidad_agua.universe)
media= fuzz.interp_membership(cantidad_agua.universe, cantidad_agua['media'].mf, cantidad_agua.universe)
alta = fuzz.interp_membership(cantidad_agua.universe, cantidad_agua['alta'].mf, cantidad_agua.universe)

# Graficar las funciones de membresía
ax.plot(cantidad_agua.universe, baja, label='Baja', color='blue')
ax.plot(cantidad_agua.universe, media, label='Media', color='orange')
ax.plot(cantidad_agua.universe, alta, label='Alta', color='green')

# Marca el valor de la cantidad de agua recomendada
ax.plot(cantidad_agua_recomendada, 0, 'ro', label=f'Recomendación: {cantidad_agua_recomendada:.2f} L/m²/día')

ax.set_title('Cantidad de Agua Recomendada')
ax.set_xlabel('Cantidad de Agua (litros/m²/día)')
ax.set_ylabel('Grado de Membresía')
ax.legend()

plt.show()