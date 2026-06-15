# ────────────────────────────────────────────────────────────
# MODULO 1: GENERADOR DE NOMBRES DE NODOS
# ────────────────────────────────────────────────────────────

def generar_nombres(n):
    """
    Genera n nombres unicos de nodos: A, B, ..., Z, A1, B1, ..., Z1, A2, ...
    """
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nombres = []
    i = 0
    
    while len(nombres) < n:
        letra = letras[i % 26]
        ciclo = i // 26
        
        if ciclo == 0:
            nombre = letra
        else:
            nombre = letra + str(ciclo)
        
        nombres.append(nombre)
        i = i + 1
    
    return nombres


# ────────────────────────────────────────────────────────────
# MODULO 2: VALIDACION DE ENTRADAS GENERALES
# ────────────────────────────────────────────────────────────

def leer_entero_positivo(mensaje, minimo=2):
    """
    Lee entero >= minimo. Acepta floats enteros como 3.0.
    Rechaza: negativos, < minimo, strings, floats con decimal.
    """
    while True:
        try:
            entrada = input(mensaje).strip()
            if not entrada:
                raise ValueError
            valor = float(entrada)
            if valor != int(valor):
                print("  [!] Solo se permiten numeros enteros positivos.")
                continue
            valor = int(valor)
            if valor < minimo:
                print(f"  [!] El numero debe ser >= {minimo}.")
                continue
            return valor
        except ValueError:
            print(f"  [!] Entrada invalida. Ingresa entero >= {minimo}.")


def leer_opcion(mensaje, opciones):
    """
    Lee opcion de lista (case-insensitive). Devuelve en mayusculas.
    """
    while True:
        try:
            entrada = input(mensaje).strip().upper()
            if not entrada:
                raise ValueError
            
            es_valida = False
            for opcion in opciones:
                if entrada == opcion.upper():
                    es_valida = True
                    break
            
            if not es_valida:
                print(f"  [!] Opcion invalida. Elige entre: {', '.join(opciones)}")
                continue
            
            return entrada
            
        except ValueError:
            print("  [!] No ingresaste nada.")


def leer_nodo_existente(mensaje, nodos):
    """
    Lee nombre de nodo y valida que exista.
    """
    while True:
        try:
            entrada = input(mensaje).strip().upper()
            if not entrada:
                raise ValueError
            if entrada not in nodos:
                print(f"  [!] El nodo '{entrada}' no existe. Disponibles: {', '.join(sorted(nodos))}")
                continue
            return entrada
        except ValueError:
            print("  [!] No ingresaste nada.")


# ────────────────────────────────────────────────────────────
# MODULO 3: PARSER DE CONEXIONES
# ────────────────────────────────────────────────────────────

def parsear_conexiones(texto, nodo_origen, nodos_validos):
    """
    Parsea formato (B,3);(C,9.5). Devuelve lista [(destino, peso), ...].
    """
    texto = texto.strip()

    if texto == "":
        return []

    conexiones = []
    destinos_vistos = set()
    partes = texto.split(";")

    for parte in partes:
        parte = parte.strip()

        if not (parte.startswith("(") and parte.endswith(")")):
            raise ValueError(f"Formato incorrecto en '{parte}'. Usa (NODO,PESO)")

        interior = parte[1:-1].strip()
        componentes = interior.split(",")
        
        if len(componentes) != 2:
            raise ValueError(f"Se esperaba (NODO,PESO) pero se recibio '{parte}'")

        destino = componentes[0].strip().upper()
        peso_str = componentes[1].strip()

        if destino not in nodos_validos:
            raise ValueError(f"El nodo '{destino}' no existe")

        if destino == nodo_origen:
            raise ValueError(f"Auto-loop no permitido: {nodo_origen} no puede conectarse a si mismo")

        if destino in destinos_vistos:
            raise ValueError(f"El destino '{destino}' aparece mas de una vez")
        destinos_vistos.add(destino)

        try:
            peso = float(peso_str)
        except ValueError:
            raise ValueError(f"Peso invalido '{peso_str}'. Debe ser numero positivo")

        if peso <= 0:
            raise ValueError(f"El peso debe ser > 0, se recibio '{peso}'")

        conexiones.append((destino, peso))

    return conexiones


# ────────────────────────────────────────────────────────────
# MODULO 4A: VALIDACION DE ARISTAS
# ────────────────────────────────────────────────────────────

def validar_arista_matriz(matriz, indice_origen, indice_destino, peso, es_dirigido):
    """
    Valida si arista puede agregarse a la matriz.
    Dirigido: permite A→B y B→A si peso igual, rechaza si diferente.
    No dirigido: permite ingresar inversa si existe con mismo peso (no la agrega de nuevo).
    """
    # Verificar arista directa
    if matriz[indice_origen][indice_destino] != 0:
        raise ValueError(f"La conexion ya fue definida")
    
    # Grafo dirigido
    if es_dirigido:
        if matriz[indice_destino][indice_origen] != 0:
            peso_existente = matriz[indice_destino][indice_origen]
            if peso_existente != peso:
                raise ValueError(
                    f"La arista inversa existe con peso {peso_existente}. "
                    f"No puedes definir con peso {peso} (diferente)"
                )
    
    # Grafo no dirigido: permitir si inversa existe con mismo peso
    else:
        if matriz[indice_destino][indice_origen] != 0:
            peso_existente = matriz[indice_destino][indice_origen]
            if peso_existente != peso:
                raise ValueError(
                    f"La arista inversa existe con peso {peso_existente}. "
                    f"No puedes definir con peso {peso} (diferente)"
                )
            # Mismo peso: permitir (no se agregara de nuevo en agregar_arista_matriz)
    
    return True


def agregar_arista_matriz(matriz, indice_origen, indice_destino, peso, es_dirigido):
    """
    Agrega arista a la matriz solo si no existe.
    En no dirigido, agrega inversa solo si no existe.
    """
    # Agregar si no existe
    if matriz[indice_origen][indice_destino] == 0:
        matriz[indice_origen][indice_destino] = peso
    
    if not es_dirigido:
        # Agregar inversa solo si no existe
        if matriz[indice_destino][indice_origen] == 0:
            matriz[indice_destino][indice_origen] = peso


# ────────────────────────────────────────────────────────────
# MODULO 4: CONSTRUCCION DEL GRAFO (MATRIZ)
# ────────────────────────────────────────────────────────────

def construir_grafo_matriz(nodos, es_dirigido):
    """
    Solicita conexiones de cada nodo. Construye matriz de adyacencia.
    0 = sin conexion, valor numerico = peso de arista.
    """
    n = len(nodos)
    
    # Crear matriz nxn con ceros (sin conexiones)
    matriz = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(0)
        matriz.append(fila)
    
    # Mapeo nodo → indice
    nodo_a_indice = {}
    for i in range(n):
        nodo_a_indice[nodos[i]] = i
    
    conjunto_nodos = set(nodos)

    print("\n  Reglas para ingresar conexiones:")
    print("  - Formato : (NODO,PESO);(NODO,PESO)")
    print("  - Ejemplo : (B,3);(C,9.5)")
    print("  - TODO nodo DEBE tener al menos una conexion (no se permiten nodos nulos)")
    print("  - No se permiten auto-loops")
    print("  - Los pesos deben ser numeros positivos (> 0)")
    
    if es_dirigido:
        print("  - Grafo DIRIGIDO: A:(B,3) y luego B:(A,3) permitido si peso igual")
        print("  - Pero A:(B,3) y B:(A,5) NO permitido (pesos diferentes)\n")
    else:
        print("  - Grafo NO dirigido: A:(B,3) agrega B->A:3 automaticamente")
        print("  - No puedes luego ingresar B:(A,3) (redundancia)\n")

    for nodo in nodos:
        while True:
            try:
                texto = input(f"  Conexiones de {nodo}: ").strip()
                indice_nodo = nodo_a_indice[nodo]
                
                # Rechazar nodos sin conexiones solo si no tienen aristas inversas
                if texto == "":
                    tiene_inversas = False
                    for i in range(n):
                        if matriz[i][indice_nodo] != 0:
                            tiene_inversas = True
                            break
                    
                    if tiene_inversas:
                        break  # Permitir entrada vacía (tiene aristas apuntando a él)
                    
                    print(f"  [!] El nodo '{nodo}' debe tener al menos una conexion. Intenta de nuevo.")
                    continue
                
                conexiones = parsear_conexiones(texto, nodo, conjunto_nodos)
                indice_origen = nodo_a_indice[nodo]

                # Validar todas las conexiones
                for destino, peso in conexiones:
                    indice_destino = nodo_a_indice[destino]
                    validar_arista_matriz(matriz, indice_origen, indice_destino, peso, es_dirigido)

                # Agregar al grafo
                for destino, peso in conexiones:
                    indice_destino = nodo_a_indice[destino]
                    agregar_arista_matriz(matriz, indice_origen, indice_destino, peso, es_dirigido)

                break

            except ValueError as e:
                print(f"  [!] {e}. Intenta de nuevo.")

    return matriz, nodo_a_indice


# ────────────────────────────────────────────────────────────
# MODULO 5A: FUNCIONES AUXILIARES PARA DIJKSTRA
# ────────────────────────────────────────────────────────────

def inicializar_dijkstra(n, indice_origen):
    """
    Inicializa estructuras para Dijkstra.
    """
    distancias = []
    for i in range(n):
        distancias.append(float('inf'))
    
    previos = []
    for i in range(n):
        previos.append(None)
    
    visitados = set()
    distancias[indice_origen] = 0
    
    return distancias, previos, visitados


def buscar_nodo_minimo(n, distancias, visitados):
    """
    Busca nodo no visitado con menor distancia.
    """
    nodo_minimo = None
    distancia_minima = float('inf')
    
    for i in range(n):
        if i not in visitados and distancias[i] < distancia_minima:
            distancia_minima = distancias[i]
            nodo_minimo = i
    
    return nodo_minimo


def actualizar_distancias_vecinos(indice_actual, matriz, distancias, previos, n):
    """
    Actualiza distancias de vecinos del nodo actual.
    """
    for j in range(n):
        if matriz[indice_actual][j] != 0:  # Hay arista
            peso = matriz[indice_actual][j]
            nueva_dist = distancias[indice_actual] + peso
            if nueva_dist < distancias[j]:
                distancias[j] = nueva_dist
                previos[j] = indice_actual


# ────────────────────────────────────────────────────────────
# MODULO 5: ALGORITMO DE DIJKSTRA
# ────────────────────────────────────────────────────────────

def dijkstra(matriz, indice_origen):
    """
    Ejecuta Dijkstra desde indice_origen sobre matriz.
    Devuelve distancias y previos.
    """
    n = len(matriz)
    distancias, previos, visitados = inicializar_dijkstra(n, indice_origen)

    while len(visitados) < n:
        nodo_actual = buscar_nodo_minimo(n, distancias, visitados)
        
        if nodo_actual is None:
            break

        visitados.add(nodo_actual)
        actualizar_distancias_vecinos(nodo_actual, matriz, distancias, previos, n)

    return distancias, previos


# ────────────────────────────────────────────────────────────
# MODULO 6: RECONSTRUCCION DEL CAMINO
# ────────────────────────────────────────────────────────────

def reconstruir_camino(previos, indice_origen, indice_destino):
    """
    Reconstruye camino usando previos (con indices).
    """
    camino = []
    actual = indice_destino

    while actual is not None:
        camino.append(actual)
        actual = previos[actual]

    camino.reverse()

    if camino[0] != indice_origen:
        return []

    return camino


# ────────────────────────────────────────────────────────────
# MODULO 7A: IMPRIMIR MATRIZ DE ADYACENCIA
# ────────────────────────────────────────────────────────────

def imprimir_matriz_adyacencia(matriz, nodos):
    """
    Imprime matriz de adyacencia. 0 = sin conexion, numero = peso.
    """
    n = len(nodos)
    ancho_celda = 6
    
    print("\n  MATRIZ DE ADYACENCIA\n")
    
    # Encabezado
    print("  " + " " * 4, end="")
    for nodo in nodos:
        print(f"{nodo:^{ancho_celda}}", end="")
    print()
    
    # Linea separadora
    print("  " + "┌" + "┬".join(["─" * ancho_celda for _ in range(n)]) + "┐")
    
    # Filas
    for i in range(n):
        print(f"  {nodos[i]} │", end="")
        for j in range(n):
            peso = matriz[i][j]
            if peso == 0:
                valor = "0"
            elif peso == int(peso):
                valor = str(int(peso))
            else:
                valor = f"{peso:.1f}"
            print(f"{valor:^{ancho_celda}}", end="")
        print("│")
    
    # Linea final
    print("  " + "└" + "┴".join(["─" * ancho_celda for _ in range(n)]) + "┘")


# ────────────────────────────────────────────────────────────
# MODULO 7: MOSTRAR RESULTADO
# ────────────────────────────────────────────────────────────

def mostrar_resultado(camino_indices, distancia, nodos, indice_origen, indice_destino):
    """
    Imprime resultado del camino minimo (convierte indices a nombres).
    """
    print()
    if indice_origen == indice_destino:
        print(f"  Resultado: {nodos[indice_origen]} con peso: 0")
        return

    if not camino_indices or distancia == float('inf'):
        print(f"  Resultado: No existe camino de '{nodos[indice_origen]}' a '{nodos[indice_destino]}'")
        return

    # Convertir indices a nombres
    camino_nombres = []
    for indice in camino_indices:
        camino_nombres.append(nodos[indice])
    
    camino_str = " -> ".join(camino_nombres)
    
    if distancia == int(distancia):
        peso_str = str(int(distancia))
    else:
        peso_str = f"{distancia:.2f}"
    
    print(f"  Camino minimo: {camino_str} con peso: {peso_str}")


# ────────────────────────────────────────────────────────────
# MODULO 8: MENU PRINCIPAL
# ────────────────────────────────────────────────────────────

def menu_principal():
    """
    Punto de entrada. Controla flujo completo.
    """
    print("=" * 50)
    print("        ALGORITMO DE DIJKSTRA (MATRICES)")
    print("=" * 50)

    continuar_programa = True

    while continuar_programa:

        # Paso 1: Tipo de grafo
        tipo = leer_opcion(
            "\nTipo de grafo (D = Dirigido, ND = No dirigido): ",
            ["D", "ND"]
        )
        es_dirigido = (tipo == "D")

        # Paso 2: Cantidad de nodos
        n = leer_entero_positivo("Cantidad de nodos: ", minimo=2)

        # Paso 3: Generar nombres
        nodos = generar_nombres(n)
        print(f"\nNodos generados: {', '.join(nodos)}")

        # Paso 4: Ingresar conexiones
        print("\nIngresa las conexiones para cada nodo:")
        matriz, nodo_a_indice = construir_grafo_matriz(nodos, es_dirigido)

        # Paso 5: Mostrar matriz
        imprimir_matriz_adyacencia(matriz, nodos)

        # Paso 6: Bucle origen/destino
        continuar_consultas = True

        while continuar_consultas:
            print()
            origen = leer_nodo_existente("Nodo origen  : ", set(nodos))
            destino = leer_nodo_existente("Nodo destino : ", set(nodos))

            indice_origen = nodo_a_indice[origen]
            indice_destino = nodo_a_indice[destino]

            # Ejecutar Dijkstra
            distancias, previos = dijkstra(matriz, indice_origen)

            # Reconstruir y mostrar
            if indice_origen == indice_destino:
                mostrar_resultado([], 0, nodos, indice_origen, indice_destino)
            else:
                camino = reconstruir_camino(previos, indice_origen, indice_destino)
                mostrar_resultado(camino, distancias[indice_destino], nodos, indice_origen, indice_destino)

            # Menu
            print()
            opcion = leer_opcion(
                "Opciones: (C) = Nueva consulta | (N) = Nuevo grafo | (S) = Salir : ",
                ["C", "N", "S"]
            )

            if opcion == "C":
                continuar_consultas = True
            elif opcion == "N":
                continuar_consultas = False
                continuar_programa = True
            elif opcion == "S":
                continuar_consultas = False
                continuar_programa = False

    print("\nPrograma terminado.")


# ────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    menu_principal()