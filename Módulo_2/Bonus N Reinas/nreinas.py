import random
import time

def calcular_colisiones(s):
 
    n = len(s)
    colisiones = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Condición de ataque diagonal: |s[i] - s[j]| == |i - j|
            if abs(s[i] - s[j]) == (j - i):
                colisiones += 1
    return colisiones

def resolver_n_reinas_tabu(n, max_iteraciones=1000, tenencia_tabu=10):
    inicio_tiempo = time.perf_counter()
    
    # Generar solución inicial con permutacion aleatoria
    s_actual = list(range(n))
    random.shuffle(s_actual)
    
    # Inicialización de variables
    s_mejor = list(s_actual)
    colisiones_s_mejor = calcular_colisiones(s_mejor)
    colisiones_s_actual = colisiones_s_mejor
    lista_tabu = []
    iteracion = 0
    movimientos_realizados = 0
    
    # Bucle principal de optimización
    while colisiones_s_actual > 0 and iteracion < max_iteraciones:
        mejor_vecino = None
        colisiones_mejor_vecino = float('inf')
        movimiento_elegido = None
        
        # Generar y evaluar el vecindario completo N(s_actual) mediante swaps
        for i in range(n):
            for j in range(i + 1, n):
                # Generar vecino aplicando Swap entre columnas(i, j)
                s_vecino = list(s_actual)
                s_vecino[i], s_vecino[j] = s_vecino[j], s_vecino[i]
                
                colisiones_vecino = calcular_colisiones(s_vecino)
                movimiento = (s_actual[i], s_actual[j]) # Atributo del movimiento
                movimiento_inverso = (s_actual[j], s_actual[i])
                
                es_tabu = (movimiento in lista_tabu) or (movimiento_inverso in lista_tabu)
                
                if not es_tabu or colisiones_vecino < colisiones_s_mejor:
                    if colisiones_vecino < colisiones_mejor_vecino:
                        colisiones_mejor_vecino = colisiones_vecino
                        mejor_vecino = s_vecino
                        movimiento_elegido = movimiento

        # Si no hay movimientos válidos posibles
        if mejor_vecino is None:
            break
            
        #Transición al mejor vecino seleccionado
        s_actual = mejor_vecino
        colisiones_s_actual = colisiones_mejor_vecino
        movimientos_realizados += 1
        
        # Actualizar Lista Tabú
        lista_tabu.append(movimiento_elegido)
        if len(lista_tabu) > tenencia_tabu:
            lista_tabu.pop(0) # FIFO
            
        # Actualizar mejor solución global si aplica
        if colisiones_s_actual < colisiones_s_mejor:
            s_mejor = list(s_actual)
            colisiones_s_mejor = colisiones_s_actual
            
        iteracion += 1

    fin_tiempo = time.perf_counter()
    tiempo_ejecucion = fin_tiempo - inicio_tiempo

    return {
        "s_mejor": s_mejor,
        "colisiones": colisiones_s_mejor,
        "iteraciones": iteracion,
        "movimientos": movimientos_realizados,
        "tiempo_segundos": tiempo_ejecucion
    }

def imprimir_tablero(s):
    n = len(s)
    print("\n--- Tablero Resultante ---")
    for fila in range(n):
        linea = ""
        for col in range(n):
            if s[col] == fila:
                linea += " Q "
            else:
                linea += " . "
        print(linea)


# EJECUCIÓN DEL ALGORITMO

if __name__ == "__main__":
    N = 8  # Tamaño del tablero
    MAX_ITER = 1000
    TENENCIA_TABU = 3

    print(f"Resolviendo {N}-Reinas con Búsqueda Tabú...")
    resultado = resolver_n_reinas_tabu(n=N, max_iteraciones=MAX_ITER, tenencia_tabu=TENENCIA_TABU)

    # Métricas e información final
    print("\n=== MÉTRICAS DE EJECUCIÓN ===")
    print(f"Solución encontrada: {resultado['s_mejor']}")
    print(f"Colisiones restantes: {resultado['colisiones']} (0 = Éxito total)")
    print(f"Iteraciones ejecutadas: {resultado['iteraciones']}")
    print(f"Movimientos realizados: {resultado['movimientos']}")
    print(f"Tiempo de ejecución: {resultado['tiempo_segundos'] * 1000:.3f} ms ({resultado['tiempo_segundos']:.6f} s)")

    if resultado['colisiones'] == 0:
        imprimir_tablero(resultado['s_mejor'])
    else:
        print("\nNo se encontró una solución óptima en el límite de iteraciones.")