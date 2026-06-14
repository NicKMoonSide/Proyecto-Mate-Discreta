# ────────────────────────────────────────────────────────────
# MODULO 1: GENERADOR DE NOMBRES DE NODOS
# ────────────────────────────────────────────────────────────

def generar_nombres(n):
    """
    Genera n nombres unicos de nodos en orden:
    A, B, ..., Z, A1, B1, ..., Z1, A2, ...
    """
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nombres = []
    i = 0
    
    while len(nombres) < n:
        letra = letras[i % 26]
        ciclo = i // 26
        
        # Construir nombre basado en el ciclo
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
def leer_entero_positivo(mensaje):
    """
    Lee un numero entero >= 1 desde consola.
    Acepta floats enteros como 3.0 (los convierte).
    Rechaza: negativos, cero, strings, floats con decimal.
    """
    while True:
        try:
            entrada = input(mensaje).strip()
            if not entrada:
                raise ValueError
            valor = float(entrada)
            if valor != int(valor):
                # Float con decimal real, ej: 2.5
                print("  [!] Solo se permiten numeros enteros positivos (>= 1).")
                continue
            valor = int(valor)
            if valor < 1:
                print("  [!] El numero debe ser >= 1.")
                continue
            return valor
        except ValueError:
            print("  [!] Entrada invalida. Ingresa un numero entero positivo.")

def leer_opcion(mensaje, opciones):
    """
    Lee una opcion de una lista de strings validos (case-insensitive).
    Devuelve la opcion en mayusculas.
    """
    while True:
        try:
            entrada = input(mensaje).strip().upper()
            if not entrada:
                raise ValueError
            
            # Verificar si la opcion es valida
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
    Lee un nombre de nodo y valida que exista en el conjunto.
    """
    while True:
        try:
            entrada = input(mensaje).strip().upper()
            if not entrada:
                raise ValueError
            if entrada not in nodos:
                print(f"  [!] El nodo '{entrada}' no existe. Nodos disponibles: {', '.join(sorted(nodos))}")
                continue
            return entrada
        except ValueError:
            print("  [!] No ingresaste nada.")


# ────────────────────────────────────────────────────────────
# MODULO 3: PARSER Y VALIDADOR DE CONEXIONES
# ────────────────────────────────────────────────────────────

def parsear_conexiones(texto, nodo_origen, nodos_validos):
    """
    Parsea una cadena de conexiones con formato: (B,3);(C,9.5)
    Devuelve lista de tuplas (destino, peso) si todo es valido.
    Lanza ValueError con mensaje descriptivo si hay error.

    Reglas:
    - Formato: (NODO,PESO) separados por ;
    - NODO debe existir en nodos_validos
    - NODO no puede ser el mismo nodo_origen o bucle 
    - PESO debe ser float o int positivo (> 0)
    - No se permiten destinos duplicados en la misma entrada
    """
    texto = texto.strip()

    # Entrada vacia = sin conexiones
    if texto == "":
        return []

    conexiones = []
    destinos_vistos = set()

    # Dividir por ; para obtener cada par (NODO,PESO)
    partes = texto.split(";")

    for parte in partes:
        parte = parte.strip()

        # Validar que tenga parentesis
        if not (parte.startswith("(") and parte.endswith(")")):
            raise ValueError(f"Formato incorrecto en '{parte}'. Usa (NODO,PESO)")

        # Quitar parentesis
        interior = parte[1:-1].strip()

        # Dividir por coma
        componentes = interior.split(",")
        if len(componentes) != 2:
            raise ValueError(f"Se esperaba (NODO,PESO) pero se recibio '{parte}'")

        destino = componentes[0].strip().upper()
        peso_str = componentes[1].strip()

        # Validar nodo destino
        if destino not in nodos_validos:
            raise ValueError(f"El nodo '{destino}' no existe en el grafo")

        # Validar auto-loop
        if destino == nodo_origen:
            raise ValueError(f"Auto-loop no permitido: '{nodo_origen}' no puede conectarse a si mismo")

        # Validar destino duplicado en esta entrada
        if destino in destinos_vistos:
            raise ValueError(f"El destino '{destino}' aparece mas de una vez desde '{nodo_origen}'")
        destinos_vistos.add(destino)

        # Validar peso
        try:
            peso = float(peso_str)
        except ValueError:
            raise ValueError(f"Peso invalido '{peso_str}'. Debe ser un numero positivo")

        if peso <= 0:
            raise ValueError(f"El peso debe ser > 0, se recibio '{peso}'")

        conexiones.append((destino, peso))

    return conexiones


# ────────────────────────────────────────────────────────────
# MODULO 4A: VALIDACION DE ARISTAS
# ────────────────────────────────────────────────────────────

def validar_arista(grafo, nodo_origen, destino, peso, es_dirigido):
    """
    Valida si una arista puede agregarse al grafo.
    
    Dirigido: permite A:(B,3) luego B:(A,3) si peso igual.
             rechaza B:(A,5) si A:(B,3) existe con peso diferente.
    No dirigido: rechaza B:(A,3) si A:(B,3) existe (redundancia, ya se agrego automaticamente).
    """
    # Verificar arista directa (siempre rechazar si existe)
    if destino in grafo[nodo_origen]:
        raise ValueError(f"La conexion {nodo_origen}->{destino} ya fue definida")
    
    # Grafo dirigido: permitir arista inversa si peso igual
    if es_dirigido:
        if nodo_origen in grafo.get(destino, {}):
            peso_existente = grafo[destino][nodo_origen]
            if peso_existente != peso:
                raise ValueError(
                    f"La arista {destino}->{nodo_origen} existe con peso {peso_existente}. "
                    f"No puedes definir {nodo_origen}->{destino} con peso {peso} (diferente)"
                )
            # Mismo peso: permitir
            return True
    
    # Grafo no dirigido: rechazar redundancia
    else:
        if destino in grafo and nodo_origen in grafo[destino]:
            raise ValueError(
                f"La arista {destino}->{nodo_origen} ya existe (agregada automaticamente). "
                f"No redefinir {nodo_origen}->{destino} (redundancia en no dirigido)"
            )
    
    return True


def agregar_arista(grafo, nodo_origen, destino, peso, es_dirigido):
    """
    Agrega una arista al grafo.
    En grafo no dirigido, agrega automaticamente la inversa.
    """
    grafo[nodo_origen][destino] = peso
    if not es_dirigido:
        grafo[destino][nodo_origen] = peso


# ────────────────────────────────────────────────────────────
# MODULO 4: CONSTRUCCION DEL GRAFO
# ────────────────────────────────────────────────────────────

def construir_grafo(nodos, es_dirigido):
    """
    Solicita al usuario las conexiones de cada nodo.
    Construye y devuelve el grafo como diccionario:
      { 'A': {'B': 7.0, 'C': 3.0}, 'B': {}, ... }
    """
    # Inicializar grafo vacio
    grafo = {}
    for nodo in nodos:
        grafo[nodo] = {}
    
    conjunto_nodos = set(nodos)

    print("\n  Reglas para ingresar conexiones:")
    print("  - Formato : (NODO,PESO);(NODO,PESO)")
    print("  - Ejemplo : (B,3);(C,9.5)")
    print("  - TODO nodo DEBE tener al menos una conexion (no se permiten nodos nulos)")
    print("  - No se permiten auto-loops como (A,5)")
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
                
                # Rechazar nodos sin conexiones (nodos nulos)
                if texto == "":
                    print(f"  [!] El nodo '{nodo}' debe tener al menos una conexion. Intenta de nuevo.")
                    continue
                
                conexiones = parsear_conexiones(texto, nodo, conjunto_nodos)

                # Validar todas las conexiones
                for destino, peso in conexiones:
                    validar_arista(grafo, nodo, destino, peso, es_dirigido)

                # Si todo valido, agregar al grafo
                for destino, peso in conexiones:
                    agregar_arista(grafo, nodo, destino, peso, es_dirigido)

                break  # Conexiones validas, pasar al siguiente nodo

            except ValueError as e:
                print(f"  [!] {e}. Intenta de nuevo.")

    return grafo


# ────────────────────────────────────────────────────────────
# MODULO 5A: FUNCIONES AUXILIARES PARA DIJKSTRA
# ────────────────────────────────────────────────────────────

def inicializar_dijkstra(nodos, origen):
    """
    Inicializa las estructuras de datos para Dijkstra.
    Retorna distancias, previos, visitados.
    """
    # Inicializar diccionario de distancias
    distancias = {}
    for nodo in nodos:
        distancias[nodo] = float('inf')
    
    # Inicializar diccionario de previos
    previos = {}
    for nodo in nodos:
        previos[nodo] = None
    
    # Inicializar conjunto de visitados
    visitados = set()
    
    # La distancia del origen es 0
    distancias[origen] = 0
    
    return distancias, previos, visitados


def buscar_nodo_minimo(nodos, distancias, visitados):
    """
    Busca el nodo no visitado con menor distancia.
    Retorna el nodo o None si no hay nodos alcanzables.
    """
    nodo_minimo = None
    distancia_minima = float('inf')
    
    for nodo in nodos:
        if nodo not in visitados and distancias[nodo] < distancia_minima:
            distancia_minima = distancias[nodo]
            nodo_minimo = nodo
    
    return nodo_minimo


def actualizar_distancias_vecinos(nodo_actual, grafo, distancias, previos):
    """
    Actualiza las distancias de los nodos vecinos del nodo actual.
    Si encuentra un camino mas corto a un vecino, actualiza su distancia y previo.
    """
    # Iterar sobre todos los vecinos del nodo actual
    for vecino, peso in grafo[nodo_actual].items():
        # Calcular la nueva distancia si vamos a traves del nodo actual
        nueva_dist = distancias[nodo_actual] + peso
        
        # Si esta nueva distancia es mejor que la que teniamos, actualizamos
        if nueva_dist < distancias[vecino]:
            distancias[vecino] = nueva_dist
            previos[vecino] = nodo_actual


# ────────────────────────────────────────────────────────────
# MODULO 5: ALGORITMO DE DIJKSTRA
# ────────────────────────────────────────────────────────────

def dijkstra(grafo, origen):
    """
    Ejecuta Dijkstra desde el nodo origen sobre el grafo.
    Devuelve:
      - distancias: dict {nodo: distancia_minima}
      - previos:    dict {nodo: nodo_anterior}  para reconstruir camino
    """
    nodos = list(grafo.keys())
    distancias, previos, visitados = inicializar_dijkstra(nodos, origen)

    # Procesar nodos hasta que no haya mas alcanzables
    while len(visitados) < len(nodos):
        # Buscar nodo no visitado con menor distancia
        nodo_actual = buscar_nodo_minimo(nodos, distancias, visitados)
        
        # Si no hay nodo alcanzable, terminar
        if nodo_actual is None:
            break

        # Marcar como visitado
        visitados.add(nodo_actual)
        
        # Actualizar distancias de los vecinos
        actualizar_distancias_vecinos(nodo_actual, grafo, distancias, previos)

    return distancias, previos


# ────────────────────────────────────────────────────────────
# MODULO 6: RECONSTRUCCION DEL CAMINO
# ────────────────────────────────────────────────────────────

def reconstruir_camino(previos, origen, destino):
    """
    Reconstruye la lista de nodos del camino minimo
    desde origen hasta destino usando el dict de previos.
    Devuelve lista vacia si no hay camino.
    """
    camino = []
    actual = destino

    # Va iterando los valores del diccionario previo y guardando en una lista
    while actual is not None:
        camino.append(actual)
        actual = previos[actual]

    camino.reverse()

    # Verificar que el camino realmente llega desde el origen
    if camino[0] != origen:
        return []

    return camino


# ────────────────────────────────────────────────────────────
# MODULO 7A: IMPRIMIR MATRIZ DE ADYACENCIA
# ────────────────────────────────────────────────────────────

def imprimir_matriz_adyacencia(grafo):
    """
    Imprime la matriz de adyacencia del grafo en formato tabular.
    Muestra pesos de aristas, 0 si no hay conexion.
    """
    nodos = sorted(grafo.keys())
    ancho_celda = 6
    
    print("\n  MATRIZ DE ADYACENCIA\n")
    
    # Encabezado
    print("  " + " " * 4, end="")
    for nodo in nodos:
        print(f"{nodo:^{ancho_celda}}", end="")
    print()
    
    # Linea separadora
    print("  " + "┌" + "┬".join(["─" * ancho_celda for _ in nodos]) + "┐")
    
    # Filas
    for nodo_origen in nodos:
        print(f"  {nodo_origen} │", end="")
        for nodo_destino in nodos:
            if nodo_destino in grafo[nodo_origen]:
                peso = grafo[nodo_origen][nodo_destino]
                if peso == int(peso):
                    valor = str(int(peso))
                else:
                    valor = f"{peso:.1f}"
            else:
                valor = "0"
            print(f"{valor:^{ancho_celda}}", end="")
        print("│")
    
    # Linea final
    print("  " + "└" + "┴".join(["─" * ancho_celda for _ in nodos]) + "┘")


# ────────────────────────────────────────────────────────────
# MODULO 7: MOSTRAR RESULTADO
# ────────────────────────────────────────────────────────────

def mostrar_resultado(camino, distancia, origen, destino):
    """
    Imprime el resultado del camino minimo.
    """
    print()
    if origen == destino:
        print(f"  Resultado: {origen} con peso: 0")
        return

    if not camino or distancia == float('inf'):
        print(f"  Resultado: No existe camino de '{origen}' a '{destino}'")
        return

    camino_str = " -> ".join(camino)
    print(f"  Camino minimo de '{origen}' a '{destino}': {camino_str} con peso: {distancia}" )




# ────────────────────────────────────────────────────────────
# MODULO 8: MENU PRINCIPAL
# ────────────────────────────────────────────────────────────

def menu_principal():
    """
    Punto de entrada del programa.
    Controla el flujo completo y el menu de repeticion.
    """
    print("=" * 50)
    print("        ALGORITMO DE DIJKSTRA")
    print("=" * 50)

    continuar_programa = True

    while continuar_programa:

        # ── Paso 1: Tipo de grafo ──────────────────────────
        tipo = leer_opcion(
            "\nTipo de grafo (D = Dirigido, ND = No dirigido): ",
            ["D", "ND"]
        )
        es_dirigido = (tipo == "D")

        # ── Paso 2: Cantidad de nodos ──────────────────────
        n = leer_entero_positivo("Cantidad de nodos: ")

        # ── Paso 3: Generar nombres ────────────────────────
        nodos = generar_nombres(n)
        print(f"\nNodos generados: {', '.join(nodos)}")

        # ── Paso 4: Ingresar conexiones ────────────────────
        print("\nIngresa las conexiones para cada nodo:")
        grafo = construir_grafo(nodos, es_dirigido)

        # ── Paso 5: Mostrar matriz de adyacencia ────────────
        imprimir_matriz_adyacencia(grafo)

        # ── Paso 6: Bucle origen/destino ───────────────────
        continuar_consultas = True

        while continuar_consultas:
            print()
            origen  = leer_nodo_existente("Nodo origen  : ", set(nodos))
            destino = leer_nodo_existente("Nodo destino : ", set(nodos))

            # Ejecutar Dijkstra
            distancias, previos = dijkstra(grafo, origen)

            # Reconstruir y mostrar
            if origen == destino:
                mostrar_resultado([], 0, origen, destino)
            else:
                camino = reconstruir_camino(previos, origen, destino)
                mostrar_resultado(camino, distancias[destino], origen, destino)

            # Preguntar que hacer despues
            print()
            opcion = leer_opcion(
                "Opciones: (C) = Nueva consulta mismo grafo | (N) = Nuevo grafo | (S) = Salir : ",
                ["C", "N", "S"]
            )

            if opcion == "C":
                continuar_consultas = True
            elif opcion == "N":
                continuar_consultas = False
                continuar_programa  = True
            elif opcion == "S":
                continuar_consultas = False
                continuar_programa  = False

    print("\nPrograma terminado.")


# ────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    menu_principal()