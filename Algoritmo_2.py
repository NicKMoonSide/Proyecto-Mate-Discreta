# ===== 1. ENTRADAS =====                          # Sección de funciones para pedir datos al usuario
def pedir_entero(msj):                             # Función que pide un número entero positivo
    while True:                                    # Repite hasta ingresar un valor válido
        dato=input(msj).strip()                    # Lee el dato y elimina espacios
        if dato=="":                               # Verifica si está vacío
            print("Error: la entrada no puede estar vacía") # Mensaje de error
            continue                               # Vuelve a pedir el dato
        try:                                       # Intenta convertir a entero
            dato=int(dato)                         # Convierte texto a entero
            if dato>0:                             # Verifica que sea mayor a 0
                return dato                        # Retorna el valor válido
            print("Error: el número debe ser mayor a 0") # Error si no es positivo
        except ValueError:                         # Captura error de conversión
            print("Error: debe ingresar un número entero válido") # Mensaje de error

def pedir_tipo_grafo():                            # Función para elegir el tipo de grafo
    while True:                                    # Repite hasta elegir correctamente
        print("\nSeleccione el tipo de grafo:")    # Muestra mensaje
        print("a) Grafo dirigido")                 # Opción grafo dirigido
        print("b) Grafo no dirigido")              # Opción grafo no dirigido
        op=input("Opción: ").strip().lower()       # Lee opción y la convierte a minúscula
        if op=="a":                                # Si elige a
            return "dirigido"                      # Retorna tipo dirigido
        if op=="b":                                # Si elige b
            return "no dirigido"                   # Retorna tipo no dirigido
        print("Error: debe ingresar 'a' o 'b'.")  # Error si ingresa otra opción

def pedir_nodo(grafo,msj):                         # Función para pedir un nodo existente
    while True:                                    # Repite hasta ingresar nodo válido
        nodo=input(msj).strip()                    # Lee el nodo
        if nodo in grafo:                          # Verifica si existe en el grafo
            return nodo                            # Retorna nodo válido
        print("Error: el nodo no existe en el grafo.") # Error si no existe

def preguntar_continuar():                         # Función para preguntar si desea continuar
    while True:                                    # Repite hasta respuesta válida
        op=input("\n¿Desea continuar? (s/n): ").strip().lower() # Lee respuesta
        if op=="s":                                # Si responde sí
            return True                            # Retorna verdadero
        if op=="n":                                # Si responde no
            return False                           # Retorna falso
        print("Error: debe ingresar 's' para sí o 'n' para no.") # Error de opción

# ===== 2. LECTURA DEL GRAFO =====                 # Sección de lectura y construcción del grafo
def leer_conexiones(texto):                        # Función para procesar conexiones
    conexiones={}                                  # Diccionario vacío de conexiones
    texto=texto.strip().replace(" ","")            # Elimina espacios
    if texto=="":                                  # Verifica si no hay conexiones
        return conexiones                          # Retorna diccionario vacío
    if "[" in texto or "]" in texto:               # Verifica uso incorrecto de corchetes
        raise ValueError("no use corchetes, use paréntesis. Ejemplo: (B,7)") # Error
    if not texto.startswith("(") or not texto.endswith(")"): # Verifica formato correcto
        raise ValueError("use el formato (Nodo,peso)") # Error de formato
    partes=texto[1:-1].split("),(")                # Divide las conexiones
    for parte in partes:                           # Recorre conexiones
        datos=parte.split(",")                     # Divide nodo y peso
        if len(datos)!=2:                          # Verifica formato válido
            raise ValueError("use el formato (Nodo,peso)") # Error de formato
        vecino=datos[0].strip()                    # Obtiene nodo vecino
        if vecino=="":                             # Verifica vecino vacío
            raise ValueError("el nodo vecino no puede estar vacío") # Error
        if vecino in conexiones:                   # Verifica conexiones repetidas
            raise ValueError("no se permiten conexiones repetidas") # Error
        try:                                       # Intenta convertir peso
            peso=float(datos[1])                   # Convierte peso a decimal
        except ValueError:                         # Si falla conversión
            raise ValueError("el peso debe ser numérico") # Error
        if peso<=0:                                # Verifica peso positivo
            raise ValueError("el peso debe ser mayor a 0") # Error
        conexiones[vecino]=peso                    # Guarda vecino y peso
    return conexiones                              # Retorna conexiones procesadas

def leer_linea(grafo,num):                         # Función para leer un nodo completo
    linea=input("Nodo "+str(num)+": ").strip()     # Lee línea ingresada
    if linea=="":                                  # Verifica línea vacía
        raise ValueError("la línea no puede estar vacía") # Error
    if ":" not in linea:                           # Verifica uso de :
        raise ValueError("debe usar dos puntos. Ejemplo: A: (B,7)") # Error
    nodo,texto=linea.split(":",1)                  # Divide nodo y conexiones
    nodo=nodo.strip()                              # Elimina espacios del nodo
    if nodo=="":                                   # Verifica nodo vacío
        raise ValueError("el nombre del nodo no puede estar vacío") # Error
    if nodo in grafo:                              # Verifica nodo repetido
        raise ValueError("el nodo ya fue ingresado") # Error
    return nodo,leer_conexiones(texto)             # Retorna nodo y conexiones

def validar_linea_inmediata(grafo,nodo,conexiones,tipo): # Función que valida conexiones
    if nodo in conexiones:                         # Verifica bucles
        raise ValueError("no se permiten bucles: "+nodo+" no puede conectarse consigo mismo") # Error
    for vecino,peso in conexiones.items():         # Recorre conexiones
        if vecino in grafo and nodo in grafo[vecino] and grafo[vecino][nodo]!=peso:
            raise ValueError("peso inconsistente entre "+nodo+" y "+vecino) # Error de peso
    if tipo=="no dirigido":                        # Validaciones exclusivas de grafos no dirigidos
        for vecino in conexiones:                  # Recorre vecinos
            if vecino in grafo and nodo not in grafo[vecino]:
                raise ValueError("falta la conexión inversa previa: "+vecino+" -> "+nodo) # Error
        for anterior,vecinos in grafo.items():     # Recorre grafo
            if nodo in vecinos:                    # Verifica conexión inversa
                if anterior not in conexiones:
                    raise ValueError("falta la conexión inversa: "+nodo+" -> "+anterior) # Error
                if conexiones[anterior]!=vecinos[nodo]:
                    raise ValueError("peso inconsistente entre "+anterior+" y "+nodo) # Error

def pedir_grafo(total,tipo):                       # Función para construir el grafo
    while True:                                    # Repite hasta crear un grafo válido
        grafo={}                                   # Inicializa grafo vacío
        print("\nIngrese los nodos del grafo:")    # Mensaje de ingreso
        while len(grafo)<total:                    # Mientras falten nodos
            try:                                   # Intenta leer nodo
                nodo,conexiones=leer_linea(grafo,len(grafo)+1) # Lee línea
                validar_linea_inmediata(grafo,nodo,conexiones,tipo) # Valida línea
                grafo[nodo]=conexiones             # Guarda nodo y conexiones
            except ValueError as e:                # Captura errores
                print("Error:",e)                  # Muestra error
        errores=validar_grafo(grafo,total,tipo)    # Valida el grafo completo
        if not errores:                            # Si no hay errores
            return grafo                           # Retorna grafo válido
        print("\nEl grafo no es válido:")          # Mensaje de error
        for e in errores:                          # Recorre errores
            print("-",e)                           # Muestra cada error
        print("\nIngrese nuevamente todo el grafo.") # Solicita nuevo ingreso

# ===== 3. VALIDACIÓN GENERAL =====                # Sección de validaciones generales
def validar_grafo(grafo,total,tipo):               # Función de validación total
    errores=[]                                     # Lista de errores
    if len(grafo)!=total:                          # Verifica cantidad de nodos
        errores.append("la cantidad de nodos no coincide con el total declarado") # Error
    for nodo,vecinos in grafo.items():             # Recorre nodos
        for vecino,peso in vecinos.items():        # Recorre conexiones
            if vecino==nodo:                       # Verifica bucles
                errores.append("no se permiten bucles en el nodo "+nodo) # Error
                continue                           # Continúa al siguiente
            if vecino not in grafo:                # Verifica vecino existente
                errores.append("el nodo '"+vecino+"' no fue definido") # Error
                continue                           # Continúa al siguiente
            if nodo in grafo[vecino] and grafo[vecino][nodo]!=peso:
                errores.append("peso inconsistente entre "+nodo+" y "+vecino) # Error
            if tipo=="no dirigido" and nodo not in grafo[vecino]:
                errores.append("falta la conexión inversa: "+vecino+" -> "+nodo) # Error
    return errores                                 # Retorna lista de errores

# ===== 4. HEAP MANUAL Y DIJKSTRA =====            # Sección de heap y algoritmo Dijkstra
def subir_heap(heap,i):                            # Función para ordenar heap hacia arriba
    while i>0:                                     # Mientras no sea raíz
        padre=(i-1)//2                             # Calcula índice del padre
        if heap[padre][0]<=heap[i][0]:             # Verifica orden
            break                                  # Sale si ya está ordenado
        heap[padre],heap[i]=heap[i],heap[padre]   # Intercambia posiciones
        i=padre                                    # Actualiza índice

def bajar_heap(heap,i):                            # Función para ordenar heap hacia abajo
    while True:                                    # Repite hasta ordenar
        menor=i                                    # Asume menor actual
        izq=2*i+1                                  # Índice hijo izquierdo
        der=2*i+2                                  # Índice hijo derecho
        if izq<len(heap) and heap[izq][0]<heap[menor][0]:
            menor=izq                              # Actualiza menor
        if der<len(heap) and heap[der][0]<heap[menor][0]:
            menor=der                              # Actualiza menor
        if menor==i:                               # Si ya está ordenado
            break                                  # Sale del ciclo
        heap[i],heap[menor]=heap[menor],heap[i]   # Intercambia nodos
        i=menor                                    # Actualiza posición

def insertar_heap(heap,dato):                      # Función para insertar en heap
    heap.append(dato)                              # Agrega dato al final
    subir_heap(heap,len(heap)-1)                   # Reordena heap

def extraer_menor(heap):                           # Función para extraer el menor
    menor=heap[0]                                  # Guarda el menor
    ultimo=heap.pop()                              # Extrae último elemento
    if heap:                                       # Si heap no está vacío
        heap[0]=ultimo                             # Coloca último en raíz
        bajar_heap(heap,0)                         # Reordena heap
    return menor                                   # Retorna menor elemento

def dijkstra(grafo,origen,destino):                # Algoritmo de Dijkstra
    dist={nodo:float("inf") for nodo in grafo}     # Inicializa distancias infinitas
    ant={nodo:None for nodo in grafo}              # Guarda nodos anteriores
    visitados={}                                   # Diccionario de visitados
    heap=[]                                        # Cola de prioridad
    dist[origen]=0                                 # Distancia inicial en origen
    insertar_heap(heap,(0,origen))                 # Inserta origen en heap
    while heap:                                    # Mientras heap tenga elementos
        distancia_actual,actual=extraer_menor(heap) # Extrae menor distancia
        if actual in visitados:                    # Verifica si ya fue visitado
            continue                               # Continúa al siguiente
        visitados[actual]=True                     # Marca como visitado
        if actual==destino:                        # Verifica si llegó al destino
            break                                  # Finaliza búsqueda
        for vecino,peso in grafo[actual].items():  # Recorre vecinos
            if vecino in visitados:                # Si ya fue visitado
                continue                           # Continúa
            nueva=distancia_actual+peso            # Calcula nueva distancia
            if nueva<dist[vecino]:                 # Verifica si es menor
                dist[vecino]=nueva                 # Actualiza distancia
                ant[vecino]=actual                 # Guarda nodo anterior
                insertar_heap(heap,(nueva,vecino)) # Inserta en heap
    if dist[destino]==float("inf"):                # Si no existe ruta
        return [],float("inf")                     # Retorna vacío e infinito
    camino=[]                                      # Lista del camino
    actual=destino                                 # Empieza desde destino
    while actual is not None:                      # Mientras existan nodos
        camino.append(actual)                      # Agrega nodo al camino
        actual=ant[actual]                         # Retrocede al nodo anterior
    camino.reverse()                               # Invierte el camino
    return camino,dist[destino]                    # Retorna camino y peso total

# ===== 5. PROGRAMA PRINCIPAL =====                # Sección principal del programa
def main():                                        # Función principal
    print("Escriba cada nodo así: A: (B,7), (C,6)") # Instrucción de formato
    print("Si un nodo no tiene conexiones, escriba su nombre seguido de dos puntos. Ejemplo: D:") # Instrucción
    while True:                                    # Repite programa
        tipo=pedir_tipo_grafo()                    # Pide tipo de grafo
        total=pedir_entero("Ingrese el número total de nodos: ") # Pide cantidad de nodos
        grafo=pedir_grafo(total,tipo)              # Construye el grafo
        print("\nTipo de grafo:",tipo)             # Muestra tipo
        print("Nodos disponibles:",", ".join(grafo)) # Muestra nodos
        origen=pedir_nodo(grafo,"Ingrese el nodo origen: ") # Pide origen
        destino=pedir_nodo(grafo,"Ingrese el nodo destino: ") # Pide destino
        camino,peso=dijkstra(grafo,origen,destino) # Ejecuta Dijkstra
        print("\nResultado:")                      # Muestra resultado
        if not camino:                             # Si no existe camino
            print("No existe ruta entre los nodos indicados.") # Mensaje
        else:                                      # Si existe camino
            if peso==int(peso):                    # Verifica si es entero
                peso=int(peso)                     # Convierte a entero
            print("Camino:"," -> ".join(camino))   # Muestra camino
            print("Peso total:",peso)              # Muestra peso total
        if not preguntar_continuar():              # Pregunta si continúa
            print("Programa finalizado.")          
            break                                  # Sale del programa

main()