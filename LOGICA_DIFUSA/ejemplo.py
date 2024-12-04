# Logica Difusa velocidad de un abanico dependiendo de la temperatura

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definir las variables difusas
temperatura = ctrl.Antecedent(np.arange(0, 41, 1), 'temperatura')  # 0 a 40 °C
velocidad = ctrl.Consequent(np.arange(0, 101, 1), 'velocidad')     # 0 a 100 %

# Definir los conjuntos difusos para la temperatura
temperatura['fría'] = fuzz.trapmf(temperatura.universe, [0, 0, 10, 20])
temperatura['templada'] = fuzz.trimf(temperatura.universe, [10, 20, 30])
temperatura['caliente'] = fuzz.trapmf(temperatura.universe, [20, 30, 40, 40])

# Definir los conjuntos difusos para la velocidad
velocidad['baja'] = fuzz.trapmf(velocidad.universe, [0, 0, 30, 50])
velocidad['media'] = fuzz.trimf(velocidad.universe, [30, 50, 70])
velocidad['alta'] = fuzz.trapmf(velocidad.universe, [50, 70, 100, 100])

# Visualizar las funciones de membresía
temperatura.view()
velocidad.view()

# Mostrar las gráficas
plt.show()

# Graficar las funciones de membresía de temperatura
x = np.arange(0, 41, 1)
fria = fuzz.trapmf(x, [0, 0, 10, 20])
templada = fuzz.trimf(x, [10, 20, 30])
caliente = fuzz.trapmf(x, [20, 30, 40, 40])

plt.figure(figsize=(10, 6))
plt.plot(x, fria, label='Fría', color='blue')
plt.plot(x, templada, label='Templada', color='green')
plt.plot(x, caliente, label='Caliente', color='red')
plt.title('Funciones de Membresía para la Temperatura')
plt.xlabel('Temperatura (°C)')
plt.ylabel('Grado de Pertenencia')
plt.legend()
plt.grid()
plt.show()

# Definir las reglas difusas
reglas = [
    ctrl.Rule(temperatura['fría'], velocidad['baja']),
    ctrl.Rule(temperatura['templada'], velocidad['media']),
    ctrl.Rule(temperatura['caliente'], velocidad['alta']),
]

# Crear el sistema de control
controlador_ventilador = ctrl.ControlSystem(reglas)
simulador = ctrl.ControlSystemSimulation(controlador_ventilador)

# Simular con una temperatura específica
simulador.input['temperatura'] = 20 # Cambia este valor para probar otras temperaturas
simulador.compute()

# Mostrar el resultado
print(f"Temperatura: 25°C -> Velocidad del ventilador: {simulador.output['velocidad']:.2f}%")

# Visualizar el resultado
velocidad.view(sim=simulador)

plt.show()