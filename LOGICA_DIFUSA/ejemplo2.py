# Logica difusa para evaluar si un estudiante aprueba una materia basado en su promedio de calificaciones 
# y su nivel de participación en clase.

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import matplotlib.pyplot as plt

# Crear un dataset ficticio
data = {
    'Promedio': [60, 75, 80, 50, 90, 45, 70],
    'Participación': [40, 80, 70, 30, 90, 20, 60]
}
df = pd.DataFrame(data)

promedio = ctrl.Antecedent(np.arange(0, 101, 1), 'promedio')  # 0 a 100
participacion = ctrl.Antecedent(np.arange(0, 101, 1), 'participacion')  # 0 a 100
probabilidad_aprobacion = ctrl.Consequent(np.arange(0, 101, 1), 'probabilidad_aprobacion')  # 0% a 100%

# Conjuntos difusos para promedio
promedio['bajo'] = fuzz.trapmf(promedio.universe, [0, 0, 50, 70])
promedio['medio'] = fuzz.trimf(promedio.universe, [50, 70, 85])
promedio['alto'] = fuzz.trapmf(promedio.universe, [70, 85, 100, 100])

# Conjuntos difusos para participación
participacion['baja'] = fuzz.trapmf(participacion.universe, [0, 0, 30, 50])
participacion['media'] = fuzz.trimf(participacion.universe, [30, 50, 70])
participacion['alta'] = fuzz.trapmf(participacion.universe, [60, 80, 100, 100])

# Conjuntos difusos para probabilidad de aprobación
probabilidad_aprobacion['baja'] = fuzz.trapmf(probabilidad_aprobacion.universe, [0, 0, 30, 50])
probabilidad_aprobacion['media'] = fuzz.trimf(probabilidad_aprobacion.universe, [30, 50, 70])
probabilidad_aprobacion['alta'] = fuzz.trapmf(probabilidad_aprobacion.universe, [60, 80, 100, 100])

promedio.view()
plt.show()

participacion.view()
plt.show()

probabilidad_aprobacion.view()
plt.show()

rule1 = ctrl.Rule(promedio['bajo'] & participacion['baja'], probabilidad_aprobacion['baja'])
rule2 = ctrl.Rule(promedio['medio'] & participacion['media'], probabilidad_aprobacion['media'])
rule3 = ctrl.Rule(promedio['alto'] & participacion['alta'], probabilidad_aprobacion['alta'])
rule4 = ctrl.Rule(promedio['medio'] & participacion['alta'], probabilidad_aprobacion['alta'])
rule5 = ctrl.Rule(promedio['bajo'] & participacion['alta'], probabilidad_aprobacion['media'])

aprobacion_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
aprobacion_sim = ctrl.ControlSystemSimulation(aprobacion_ctrl)

# Crear una nueva columna para los resultados
resultados = []

for index, row in df.iterrows():
    # Proporcionar los valores del dataset como entrada al sistema difuso
    aprobacion_sim.input['promedio'] = row['Promedio']
    aprobacion_sim.input['participacion'] = row['Participación']

    # Calcular el resultado
    aprobacion_sim.compute()
    resultado = aprobacion_sim.output['probabilidad_aprobacion']
    resultados.append(resultado)

# Agregar los resultados al DataFrame
df['Probabilidad_Aprobacion'] = resultados

plt.figure(figsize=(8, 6))
plt.bar(df.index, df['Probabilidad_Aprobacion'], color='lightblue', label='Probabilidad de Aprobación')
plt.xticks(df.index, [f"Estudiante {i+1}" for i in df.index], rotation=45)
plt.xlabel("Estudiantes")
plt.ylabel("Probabilidad de Aprobación (%)")
plt.title("Resultados de Probabilidad de Aprobación")
plt.legend()
plt.show()