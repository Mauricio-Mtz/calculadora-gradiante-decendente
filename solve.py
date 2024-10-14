import sys
import json
from fractions import Fraction

# Función auxiliar para convertir entrada a fracción o decimal
def parse_input(value):
    try:
        return Fraction(value)
    except ValueError:
        return float(value)

# Leer los argumentos de m, b, o
m, b, o = map(parse_input, sys.argv[1:4])

# Leer las coordenadas restantes
coordinates = []
for i in range(4, len(sys.argv), 2):
    x = parse_input(sys.argv[i])
    y = parse_input(sys.argv[i + 1])
    coordinates.append((x, y))

# Guardar los pasos en una lista
steps = []
sumM = []
sumB = []
stepsEquationM = []
stepsEquationB = []
stepsEquationM2 = []
stepsEquationB2 = []
resultOp = []
epsilon = 0.0001  # Umbral para determinar convergencia
max_iterations = 10  # Máximo número de iteraciones para evitar loops infinitos
iteration = 0

try:
    steps.append(f"m inicial = {m}")
    steps.append(f"b inicial = {b}")
    steps.append(f"o (learning rate) = {o}")

    while True:
        resM = 0
        resB = 0
        sumM.clear()
        sumB.clear()
        
        # Descomponer y formatear las coordenadas
        for idx, (x, y) in enumerate(coordinates):
            
            
            # Calcular delta
            delta = y - (x * m + b)
            
            # Sumar a resM y resB
            resM += x * delta  # Suma de todos los coeficientes en base a M
            resB += delta  # Suma de todos los coeficientes en base a B
            
            # Almacenar resultados intermedios
            sumM.append(f"({x} * [{y} - ({x} * {m} + {b})]) ")
            sumB.append(f"[{y} - ({x} * {m} + {b})] ")
            
        # Calcular gradientes
        gradM = (-2 / len(coordinates)) * resM
        gradB = (-2 / len(coordinates)) * resB

        stepsEquationM.append(f"ΣM = {', '.join(sumM)}")
        stepsEquationB.append(f"ΣB = {', '.join(sumB)}")
        # Almacenar ecuaciones actuales
        stepsEquationM.append(f"dJ/dm = -2/{len(coordinates)} ΣM ( {resM} ) = {gradM}")
        stepsEquationB.append(f"dJ/db = -2/{len(coordinates)} ΣB ( {resB} ) = {gradB}")
        
        # Actualizar m y b
        new_m = m - (o * gradM)
        new_b = b - (o * gradB)

        # Verificar convergencia (si la diferencia es menor que el umbral epsilon)
        if abs(new_m - m) < epsilon and abs(new_b - b) < epsilon:
            break

        # Actualizar los valores de m y b para la siguiente iteración
        m, b = new_m, new_b

        # Almacenar los nuevos valores
        stepsEquationM.append(f"nueva m = {m}")
        stepsEquationB.append(f"nueva b = {b}")

        stepsEquationM.append("***************************************************************")
        stepsEquationB.append("***************************************************************")
        
        iteration += 1
        if iteration >= max_iterations:
            steps.append("Se alcanzó el máximo número de iteraciones.")
            break

    # Almacenar resultados finales
    resultOp.append(f"m final = {m}, b final = {b}")

    # Crear un diccionario con el resultado y los pasos
    result = {
        'data': steps,
        'm': stepsEquationM,
        'b': stepsEquationB,
        'mFinal': m,
        'bFinal': b,
        'iterations': iteration
    }
    
    # Devolver los resultados y los pasos como JSON
    print(json.dumps(result))

except ValueError as e:
    steps.append(str(e))
    result = {
        'data': steps,
    }
    print(json.dumps(result))
