# ===== 1. ENTRADAS =====
def pedir_entero(msj):
    while True:
        dato=input(msj).strip()
        if dato=="":
            print("Error: la entrada no puede estar vacía")
            continue
        try:
            dato=int(dato)
            if dato>0:
                return dato
            print("Error: el número debe ser mayor a 0")
        except ValueError:
            print("Error: debe ingresar un número entero válido")

def pedir_tipo_grafo():
    while True:
        print("\nSeleccione el tipo de grafo:")
        print("a) Grafo dirigido")
        print("b) Grafo no dirigido")
        op=input("Opción: ").strip().lower()
        if op=="a":
            return "dirigido"
        if op=="b":
            return "no dirigido"
        print("Error: debe ingresar 'a' o 'b'.")

def pedir_nodo(grafo,msj):
    while True:
        nodo=input(msj).strip()
        if nodo in grafo:
            return nodo
        print("Error: el nodo no existe en el grafo.")

def preguntar_continuar():
    while True:
        op=input("\n¿Desea continuar? (s/n): ").strip().lower()
        if op=="s":
            return True
        if op=="n":
            return False
        print("Error: debe ingresar 's' para sí o 'n' para no.")

# ===== 2. LECTURA DEL GRAFO =====
def leer_conexiones(texto):
    conexiones={}
    texto=texto.strip().replace(" ","")
    if texto=="":
        return conexiones
    if "[" in texto or "]" in texto:
        raise ValueError("no use corchetes, use paréntesis. Ejemplo: (B,7)")
    if not texto.startswith("(") or not texto.endswith(")"):
        raise ValueError("use el formato (Nodo,peso)")
    partes=texto[1:-1].split("),(")
    for parte in partes:
        datos=parte.split(",")
        if len(datos)!=2:
            raise ValueError("use el formato (Nodo,peso)")
        vecino=datos[0].strip()
        if vecino=="":
            raise ValueError("el nodo vecino no puede estar vacío")
        if vecino in conexiones:
            raise ValueError("no se permiten conexiones repetidas")
        try:
            peso=float(datos[1])
        except ValueError:
            raise ValueError("el peso debe ser numérico")
        if peso<=0:
            raise ValueError("el peso debe ser mayor a 0")
        conexiones[vecino]=peso
    return conexiones

def leer_linea(grafo,num):
    linea=input("Nodo "+str(num)+": ").strip()
    if linea=="":
        raise ValueError("la línea no puede estar vacía")
    if ":" not in linea:
        raise ValueError("debe usar dos puntos. Ejemplo: A: (B,7)")
    nodo,texto=linea.split(":",1)
    nodo=nodo.strip()
    if nodo=="":
        raise ValueError("el nombre del nodo no puede estar vacío")
    if nodo in grafo:
        raise ValueError("el nodo ya fue ingresado")
    return nodo,leer_conexiones(texto)

def validar_linea_inmediata(grafo,nodo,conexiones,tipo):
    if nodo in conexiones:
        raise ValueError("no se permiten bucles: "+nodo+" no puede conectarse consigo mismo")
    for vecino,peso in conexiones.items():
        if vecino in grafo and nodo in grafo[vecino] and grafo[vecino][nodo]!=peso:
            raise ValueError("peso inconsistente entre "+nodo+" y "+vecino)
    if tipo=="no dirigido":
        for vecino in conexiones:
            if vecino in grafo and nodo not in grafo[vecino]:
                raise ValueError("falta la conexión inversa previa: "+vecino+" -> "+nodo)
        for anterior,vecinos in grafo.items():
            if nodo in vecinos:
                if anterior not in conexiones:
                    raise ValueError("falta la conexión inversa: "+nodo+" -> "+anterior)
                if conexiones[anterior]!=vecinos[nodo]:
                    raise ValueError("peso inconsistente entre "+anterior+" y "+nodo)

def pedir_grafo(total,tipo):
    while True:
        grafo={}
        print("\nIngrese los nodos del grafo:")
        while len(grafo)<total:
            try:
                nodo,conexiones=leer_linea(grafo,len(grafo)+1)
                validar_linea_inmediata(grafo,nodo,conexiones,tipo)
                grafo[nodo]=conexiones
            except ValueError as e:
                print("Error:",e)
        errores=validar_grafo(grafo,total,tipo)
        if not errores:
            return grafo
        print("\nEl grafo no es válido:")
        for e in errores:
            print("-",e)
        print("\nIngrese nuevamente todo el grafo.")

# ===== 3. VALIDACIÓN GENERAL =====
def validar_grafo(grafo,total,tipo):
    errores=[]
    if len(grafo)!=total:
        errores.append("la cantidad de nodos no coincide con el total declarado")
    for nodo,vecinos in grafo.items():
        for vecino,peso in vecinos.items():
            if vecino==nodo:
                errores.append("no se permiten bucles en el nodo "+nodo)
                continue
            if vecino not in grafo:
                errores.append("el nodo '"+vecino+"' no fue definido")
                continue
            if nodo in grafo[vecino] and grafo[vecino][nodo]!=peso:
                errores.append("peso inconsistente entre "+nodo+" y "+vecino)
            if tipo=="no dirigido" and nodo not in grafo[vecino]:
                errores.append("falta la conexión inversa: "+vecino+" -> "+nodo)
    return errores

# ===== 4. HEAP MANUAL Y DIJKSTRA =====
def subir_heap(heap,i):
    while i>0:
        padre=(i-1)//2
        if heap[padre][0]<=heap[i][0]:
            break
        heap[padre],heap[i]=heap[i],heap[padre]
        i=padre

def bajar_heap(heap,i):
    while True:
        menor=i
        izq=2*i+1
        der=2*i+2
        if izq<len(heap) and heap[izq][0]<heap[menor][0]:
            menor=izq
        if der<len(heap) and heap[der][0]<heap[menor][0]:
            menor=der
        if menor==i:
            break
        heap[i],heap[menor]=heap[menor],heap[i]
        i=menor

def insertar_heap(heap,dato):
    heap.append(dato)
    subir_heap(heap,len(heap)-1)

def extraer_menor(heap):
    menor=heap[0]
    ultimo=heap.pop()
    if heap:
        heap[0]=ultimo
        bajar_heap(heap,0)
    return menor

def dijkstra(grafo,origen,destino):
    dist={nodo:float("inf") for nodo in grafo}
    ant={nodo:None for nodo in grafo}
    visitados={}
    heap=[]
    dist[origen]=0
    insertar_heap(heap,(0,origen))
    while heap:
        distancia_actual,actual=extraer_menor(heap)
        if actual in visitados:
            continue
        visitados[actual]=True
        if actual==destino:
            break
        for vecino,peso in grafo[actual].items():
            if vecino in visitados:
                continue
            nueva=distancia_actual+peso
            if nueva<dist[vecino]:
                dist[vecino]=nueva
                ant[vecino]=actual
                insertar_heap(heap,(nueva,vecino))
    if dist[destino]==float("inf"):
        return [],float("inf")
    camino=[]
    actual=destino
    while actual is not None:
        camino.append(actual)
        actual=ant[actual]
    camino.reverse()
    return camino,dist[destino]

# ===== 5. PROGRAMA PRINCIPAL =====
def main():
    print("Escriba cada nodo así: A: (B,7), (C,6)")
    print("Si un nodo no tiene conexiones, escriba su nombre seguido de dos puntos. Ejemplo: D:")
    while True:
        tipo=pedir_tipo_grafo()
        total=pedir_entero("Ingrese el número total de nodos: ")
        grafo=pedir_grafo(total,tipo)
        print("\nTipo de grafo:",tipo)
        print("Nodos disponibles:",", ".join(grafo))
        origen=pedir_nodo(grafo,"Ingrese el nodo origen: ")
        destino=pedir_nodo(grafo,"Ingrese el nodo destino: ")
        camino,peso=dijkstra(grafo,origen,destino)
        print("\nResultado:")
        if not camino:
            print("No existe ruta entre los nodos indicados.")
        else:
            if peso==int(peso):
                peso=int(peso)
            print("Camino:"," -> ".join(camino))
            print("Peso total:",peso)
        if not preguntar_continuar():
            print("Programa finalizado.")
            break

main()
