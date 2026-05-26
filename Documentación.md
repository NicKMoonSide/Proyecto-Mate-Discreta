# Documentacion: Algoritmo de Dijkstra en Python

## Tabla de contenidos

1. [Descripcion general](#descripcion-general)
2. [Requisitos del sistema](#requisitos-del-sistema)
3. [Requisitos funcionales](#requisitos-funcionales)
4. [Requisitos de validacion](#requisitos-de-validacion)
5. [Estructura modular](#estructura-modular)
6. [Modulos detallados](#modulos-detallados)
7. [Flujo de ejecucion](#flujo-de-ejecucion)
8. [Ejemplos de uso](#ejemplos-de-uso)
9. [Limitaciones conocidas](#limitaciones-conocidas)

---

## Descripcion general

Implementacion del algoritmo de Dijkstra para encontrar el camino de menor peso entre dos nodos en un grafo. El programa funciona completamente en consola, sin librerias externas, con programacion modular y validacion exhaustiva de todas las entradas del usuario.

El algoritmo calcula la distancia minima desde un nodo origen hacia un nodo destino elegido por el usuario, y reconstruye el camino exacto recorrido.

---

## Requisitos del sistema

- Python 3.6 o superior
- Sin dependencias externas (no usa `import` de librerias de terceros)
- Ejecucion por consola: `python dijkstra.py`

---

## Requisitos funcionales

### Tipo de grafo

- El usuario elige entre **grafo dirigido (D)** o **grafo no dirigido (ND)**.
- En un grafo **no dirigido**: si se declara `A -> B` con peso 7, el sistema agrega automaticamente `B -> A` con peso 7. El usuario no puede redeclarar esa arista inversa.
- En un grafo **dirigido**: cada arista es de una sola direccion. Si existe `A -> B`, no se permite declarar `B -> A` (no pueden existir dos aristas entre los mismos dos nodos en ninguna direccion).

### Nodos

- El usuario indica cuantos nodos quiere (N >= 1).
- Los nombres se generan automaticamente en orden: `A, B, C, ..., Z, A1, B1, ..., Z1, A2, ...` sin limite.
- El usuario no elige los nombres, el sistema los asigna.

### Conexiones

- Por cada nodo, el usuario ingresa sus conexiones salientes en formato: `(NODO,PESO);(NODO,PESO)`
- Si un nodo no tiene conexiones salientes, se deja la entrada vacia.
- Cada conexion define una arista entre el nodo actual y un nodo destino con un peso numerico.

### Consulta Dijkstra

- El usuario elige un nodo origen y un nodo destino.
- El sistema calcula y muestra el camino de menor peso.
- Si el destino es inalcanzable, se informa explicitamente.
- Si origen == destino, se muestra peso 0.
- Al terminar, el usuario puede hacer una nueva consulta sobre el mismo grafo, construir un nuevo grafo, o salir.

---

## Requisitos de validacion

### Cantidad de nodos

| Entrada                      | Resultado                     |
| ---------------------------- | ----------------------------- |
| Entero positivo `>= 1`       | Aceptado                      |
| Float entero como `3.0`      | Aceptado (convertido a `int`) |
| Float con decimal como `2.5` | Rechazado                     |
| Cero o negativo              | Rechazado                     |
| String de texto              | Rechazado                     |
| Entrada vacia                | Rechazado                     |

### Conexiones - formato

| Situacion                    | Resultado                      |
| ---------------------------- | ------------------------------ |
| `(B,3);(C,9.5)`              | Aceptado                       |
| Sin parentesis               | Rechazado                      |
| Sin coma entre nodo y peso   | Rechazado                      |
| Mas o menos de 2 componentes | Rechazado                      |
| Entrada vacia                | Aceptado (nodo sin conexiones) |

### Conexiones - reglas semanticas

| Situacion                                              | Resultado |
| ------------------------------------------------------ | --------- |
| Nodo destino no existe en el grafo                     | Rechazado |
| Auto-loop: `A -> A`                                    | Rechazado |
| Destino duplicado en la misma linea: `(B,3);(B,7)`     | Rechazado |
| Peso <= 0                                              | Rechazado |
| Peso no numerico                                       | Rechazado |
| Arista ya definida directamente                        | Rechazado |
| Arista inversa ya existe (grafo ND) con diferente peso | Rechazado |
| Arista inversa ya existe (grafo D) en cualquier peso   | Rechazado |

### Nodo origen / destino

| Situacion                          | Resultado                             |
| ---------------------------------- | ------------------------------------- |
| Nombre exacto de un nodo existente | Aceptado                              |
| Nodo inexistente                   | Rechazado (muestra nodos disponibles) |
| Entrada vacia                      | Rechazado                             |

---

## Estructura modular

```
dijkstra.py
│
├── Modulo 1 │ generar_nombres(n)
├── Modulo 2 │ leer_entero_positivo(mensaje)
│            │ leer_opcion(mensaje, opciones)
│            │ leer_nodo_existente(mensaje, nodos)
├── Modulo 3 │ parsear_conexiones(texto, nodo_origen, nodos_validos)
├── Modulo 4 │ construir_grafo(nodos, es_dirigido)
├── Modulo 5 │ dijkstra(grafo, origen)
├── Modulo 6 │ reconstruir_camino(previos, origen, destino)
├── Modulo 7 │ mostrar_resultado(camino, distancia, origen, destino)
└── Modulo 8 │ menu_principal()
```

Cada modulo tiene una responsabilidad unica y no mezcla logica con entrada/salida, salvo los modulos de lectura (2, 4) y presentacion (7, 8) que son los unicos que interactuan con la consola.

---

## Modulos detallados

---

### Modulo 1: `generar_nombres(n)`

**Responsabilidad:** Generar los N nombres unicos de nodos de forma automatica y determinista.

**Parametros:**

- `n` (int): cantidad de nodos a generar.

**Retorna:** Lista de strings con los nombres en orden.

**Funcionamiento interno:**

Usa un contador `i` que empieza en 0 y crece indefinidamente. Para cada valor de `i`:

- La **letra** se obtiene con `i % 26`, que cicla entre las 26 letras del abecedario.
- El **ciclo** se obtiene con `i // 26`, que indica cuantas veces se completo el abecedario.
- Si `ciclo == 0`, el nombre es solo la letra (ej: `A`, `B`).
- Si `ciclo > 0`, el nombre es letra + numero de ciclo (ej: `A1`, `B1`, `A2`).

**Ejemplo de secuencia:**

```
i=0  -> letra=A, ciclo=0 -> "A"
i=1  -> letra=B, ciclo=0 -> "B"
...
i=25 -> letra=Z, ciclo=0 -> "Z"
i=26 -> letra=A, ciclo=1 -> "A1"
i=27 -> letra=B, ciclo=1 -> "B1"
...
i=52 -> letra=A, ciclo=2 -> "A2"
```

Este esquema permite generar infinitos nodos sin colisiones.

---

### Modulo 2: Funciones de lectura validada

Este modulo agrupa tres funciones de proposito general para leer datos del usuario con validacion. Ninguna de ellas contiene logica de negocio; solo garantizan que el dato devuelto sea correcto antes de continuar.

---

#### `leer_entero_positivo(mensaje)`

**Responsabilidad:** Leer un numero entero >= 1 desde consola, repitiendo hasta obtener uno valido.

**Funcionamiento interno:**

1. Muestra el `mensaje` y espera entrada del usuario.
2. Intenta convertir la entrada a `float` (acepta tanto `"3"` como `"3.0"`).
3. Verifica que `float == int(float)` para rechazar decimales reales como `2.5`.
4. Convierte a `int` y verifica que sea >= 1.
5. Si cualquier paso falla, muestra un mensaje de error y repite con `while True`.
6. El bloque `try/except ValueError` captura entradas no numericas como `"abc"` o `""`.

**Por que se usa `float` como paso intermedio:** Permite aceptar entradas como `"3.0"` que tecnicamente son enteros validos escritos como flotantes, sin rechazarlos de forma injusta.

---

#### `leer_opcion(mensaje, opciones)`

**Responsabilidad:** Leer una opcion de un conjunto predefinido, ignorando mayusculas/minusculas.

**Funcionamiento interno:**

1. Convierte la entrada a mayusculas con `.upper()`.
2. Compara contra la lista `opciones` (tambien convertida a mayusculas).
3. Si no coincide, muestra las opciones validas y repite.
4. Entrada vacia lanza `ValueError` capturado por el `except`.

**Uso en el programa:** Captura el tipo de grafo (`D` / `ND`) y las opciones del menu final (`C` / `N` / `S`).

---

#### `leer_nodo_existente(mensaje, nodos)`

**Responsabilidad:** Leer el nombre de un nodo y verificar que exista en el grafo construido.

**Funcionamiento interno:**

1. Convierte la entrada a mayusculas (los nombres de nodos son siempre mayusculas).
2. Verifica que el nombre este en el conjunto `nodos`.
3. Si no existe, muestra la lista completa de nodos disponibles ordenada alfabeticamente.
4. Repite hasta obtener un nodo valido.

**Uso en el programa:** Captura el nodo origen y el nodo destino para ejecutar Dijkstra.

---

### Modulo 3: `parsear_conexiones(texto, nodo_origen, nodos_validos)`

**Responsabilidad:** Convertir la cadena de texto que el usuario ingresa para las conexiones de un nodo en una lista de tuplas `(destino, peso)`, aplicando todas las validaciones de formato y semantica.

**Parametros:**

- `texto` (str): lo que el usuario escribio, ej: `"(B,3);(C,9.5)"`.
- `nodo_origen` (str): el nodo cuyas conexiones se estan definiendo.
- `nodos_validos` (set): conjunto de todos los nodos del grafo.

**Retorna:** Lista de tuplas `[(destino, peso), ...]` o lista vacia si no hay conexiones.

**Lanza:** `ValueError` con mensaje descriptivo ante cualquier error.

**Funcionamiento interno paso a paso:**

1. Si el texto esta vacio, retorna `[]` inmediatamente (nodo sin conexiones salientes, valido).
2. Divide el texto por `;` para separar cada conexion individual.
3. Por cada parte:
   - Verifica que empiece con `(` y termine con `)`.
   - Elimina los parentesis y divide por `,`.
   - Verifica que haya exactamente 2 componentes: nodo y peso.
   - Convierte el nodo a mayusculas.
   - Verifica que el nodo destino exista en `nodos_validos`.
   - Verifica que el nodo destino no sea el mismo que `nodo_origen` (auto-loop).
   - Verifica que el destino no haya aparecido ya en esta misma linea (duplicado).
   - Intenta convertir el peso a `float`; si falla, lanza error.
   - Verifica que el peso sea > 0.
4. Agrega la tupla `(destino, peso)` a la lista resultado.
5. Retorna la lista completa.

**Razon de diseño:** Este modulo es puro (no hace `input` ni `print`). Solo recibe texto y devuelve datos o lanza excepcion. Esto permite que `construir_grafo` maneje el ciclo de reintento y los mensajes al usuario de forma centralizada.

---

### Modulo 4: `construir_grafo(nodos, es_dirigido)`

**Responsabilidad:** Iterar sobre todos los nodos, solicitar sus conexiones, aplicar validaciones de consistencia contra el grafo ya construido, y devolver el grafo completo.

**Parametros:**

- `nodos` (list): lista ordenada de nombres de nodos.
- `es_dirigido` (bool): `True` si el grafo es dirigido, `False` si es no dirigido.

**Retorna:** Diccionario de adyacencia:

```python
{
  'A': {'B': 7.0, 'C': 3.0},
  'B': {'C': 2.0},
  'C': {}
}
```

**Funcionamiento interno:**

1. Inicializa el grafo como un diccionario con cada nodo apuntando a un diccionario vacio.
2. Muestra las reglas de ingreso al usuario una sola vez.
3. Por cada nodo, entra en un `while True` con `try/except` que repite hasta obtener entrada valida.
4. Llama a `parsear_conexiones` para obtener la lista de tuplas.
5. Por cada tupla `(destino, peso)` valida del parser, aplica validaciones adicionales contra el estado actual del grafo:

**Validacion para grafo dirigido:**

- Si ya existe una arista `destino -> nodo_actual` en el grafo, rechaza la nueva arista `nodo_actual -> destino`. Esto impide tener dos aristas entre el mismo par de nodos en cualquier direccion.

**Validacion para grafo no dirigido:**

- Si ya existe `grafo[destino][nodo_actual]` (arista inversa agregada automaticamente), verifica que el peso sea identico. Si difiere, rechaza.
- Si el peso coincide, ignora silenciosamente (ya fue agregada antes).

**Validacion comun:**

- Si `destino` ya esta en `grafo[nodo_actual]`, la arista directa ya fue definida: rechaza.

6. Si todas las validaciones pasan, agrega las aristas al grafo.
7. En grafos no dirigidos, agrega tambien la arista inversa automaticamente.

**Razon de diseño:** Este modulo es el unico que combina entrada de usuario con logica de negocio, porque necesita el estado acumulado del grafo para validar cada nueva arista. No es posible separarlo sin pasar el grafo como parametro mutable adicional.

---

### Modulo 5: `dijkstra(grafo, origen)`

**Responsabilidad:** Ejecutar el algoritmo de Dijkstra puro sobre el grafo y devolver las distancias minimas y el mapa de nodos previos.

**Parametros:**

- `grafo` (dict): diccionario de adyacencia.
- `origen` (str): nodo desde el cual calcular distancias.

**Retorna:**

- `distancias` (dict): `{nodo: distancia_minima_desde_origen}`. Nodos inalcanzables quedan con valor `inf`.
- `previos` (dict): `{nodo: nodo_anterior_en_camino_minimo}`. Permite reconstruir el camino.

**Funcionamiento interno:**

1. Inicializa todas las distancias en `inf` (infinito) y todos los previos en `None`.
2. La distancia del nodo origen se establece en `0`.
3. Mantiene un conjunto `visitados` inicialmente vacio.
4. Bucle principal: mientras queden nodos sin visitar:
   - Busca el nodo no visitado con menor distancia conocida (seleccion minima manual, O(n) por iteracion).
   - Si ninguno tiene distancia < inf, no hay mas nodos alcanzables: termina.
   - Marca ese nodo como visitado.
   - Por cada vecino del nodo actual: calcula `nueva_dist = distancias[actual] + peso`.
   - Si `nueva_dist < distancias[vecino]`, actualiza la distancia y registra el nodo actual como previo del vecino (relajacion de arista).
5. Al terminar el bucle, `distancias` y `previos` estan completamente calculados.

**Complejidad:** O(n²) donde n es el numero de nodos. Se usa busqueda lineal del minimo en lugar de un heap de prioridad (`heapq`) para cumplir el requisito de no usar librerias externas. Para grafos pequenos esto es completamente adecuado.

**Razon de diseño:** Este modulo es completamente puro: no hace `input`, no hace `print`, no modifica el grafo. Recibe datos y devuelve datos. Esto lo hace testeable de forma independiente.

---

### Modulo 6: `reconstruir_camino(previos, origen, destino)`

**Responsabilidad:** A partir del diccionario `previos` generado por Dijkstra, reconstruir la secuencia de nodos que forman el camino minimo de `origen` a `destino`.

**Parametros:**

- `previos` (dict): mapa `{nodo: nodo_anterior}` devuelto por Dijkstra.
- `origen` (str): nodo de partida.
- `destino` (str): nodo de llegada.

**Retorna:** Lista de strings con los nodos en orden, ej: `['A', 'C', 'B']`. Lista vacia si no hay camino.

**Funcionamiento interno:**

1. Comienza desde `destino` y sigue el enlace `previos[actual]` hacia atras hasta llegar a `None`.
2. Va acumulando los nodos en una lista `camino`.
3. Al terminar, invierte la lista con `.reverse()` para obtener el orden origen -> destino.
4. Verifica que el primer elemento de la lista sea el `origen`. Si no lo es, significa que el destino no era alcanzable desde el origen (su previo nunca fue actualizado por Dijkstra), y retorna lista vacia.

**Por que se verifica el primer elemento:** Si un nodo es inalcanzable, su `previos[destino]` es `None` y la lista al revertir solo contiene `[destino]`, cuyo primer elemento no es `origen`. Esta verificacion captura ese caso sin necesidad de revisar la distancia.

**Razon de diseño:** Modulo puro, sin interaccion con consola. Separado de `dijkstra` porque son responsabilidades distintas: calcular distancias vs trazar el camino.

---

### Modulo 7: `mostrar_resultado(camino, distancia, origen, destino)`

**Responsabilidad:** Formatear e imprimir el resultado final de la consulta Dijkstra.

**Parametros:**

- `camino` (list): lista de nodos del camino minimo.
- `distancia` (float): peso total del camino.
- `origen` (str): nodo origen de la consulta.
- `destino` (str): nodo destino de la consulta.

**Casos que maneja:**

| Caso                               | Salida                          |
| ---------------------------------- | ------------------------------- |
| `origen == destino`                | `A \| peso: 0`                  |
| Camino vacio o distancia infinita  | `No existe camino de 'A' a 'D'` |
| Camino encontrado con peso entero  | `A -> B -> C \| peso: 10`       |
| Camino encontrado con peso decimal | `A -> B -> C \| peso: 10.5`     |

**Funcionamiento interno:**

- Usa `" -> ".join(camino)` para construir la cadena del camino.
- Para el peso: si `distancia == int(distancia)`, muestra sin decimales para evitar `10.0` cuando el peso es entero. Si tiene decimales, redondea a 4 cifras para evitar errores de punto flotante como `9.999999999`.

---

### Modulo 8: `menu_principal()`

**Responsabilidad:** Controlar el flujo completo del programa, coordinar la llamada a todos los modulos en orden, y gestionar el menu de repeticion al finalizar cada consulta.

**Funcionamiento interno:**

Usa dos niveles de bucle anidados:

**Bucle externo** (`while continuar_programa`): controla si se construye un nuevo grafo o se termina el programa.

**Bucle interno** (`while continuar_consultas`): sobre el mismo grafo construido, permite hacer multiples consultas origen/destino sin reconstruir el grafo.

**Flujo por iteracion del bucle externo:**

```
1. Leer tipo de grafo (D / ND)
2. Leer cantidad de nodos N
3. Generar nombres de nodos
4. Construir grafo (conexiones)
5. [bucle interno]
   5.1 Leer nodo origen
   5.2 Leer nodo destino
   5.3 Ejecutar dijkstra(grafo, origen)
   5.4 Reconstruir camino
   5.5 Mostrar resultado
   5.6 Menu: C / N / S
       C -> repetir bucle interno
       N -> salir bucle interno, repetir bucle externo
       S -> salir ambos bucles
6. Imprimir "Programa terminado."
```

**Razon de diseño:** Centralizar el flujo en un unico modulo coordinador permite que todos los demas modulos sean puros o casi puros. El menu conoce el orden de las operaciones pero no implementa ninguna de ellas.

---

## Flujo de ejecucion

```
inicio
  |
  v
Elegir tipo de grafo (D / ND)
  |
  v
Ingresar cantidad de nodos N
  |
  v
Generar nombres A, B, C, ..., Z, A1, ...
  |
  v
Por cada nodo:
  Ingresar conexiones con formato (NODO,PESO);(NODO,PESO)
  Validar formato, semantica y consistencia
  Agregar aristas al grafo
  (si ND: agregar arista inversa automaticamente)
  |
  v
Ingresar nodo origen
  |
  v
Ingresar nodo destino
  |
  v
Ejecutar Dijkstra desde origen
  |
  v
Reconstruir camino hasta destino
  |
  v
Mostrar resultado
  |
  v
Menu: (C) Nueva consulta | (N) Nuevo grafo | (S) Salir
  |
  +-- C --> volver a "Ingresar nodo origen"
  +-- N --> volver a "Elegir tipo de grafo"
  +-- S --> fin
```

---

## Ejemplos de uso

### Ejemplo 1: Grafo no dirigido, 3 nodos

```
Tipo de grafo: ND
Cantidad de nodos: 3
Nodos generados: A, B, C

Conexiones de A: (B,4);(C,2)
Conexiones de B: (C,1)
Conexiones de C:

Nodo origen  : A
Nodo destino : B

Resultado: A -> C -> B | peso: 3
```

Explicacion: ir directo A->B cuesta 4, pero ir A->C->B cuesta 2+1=3. Dijkstra encuentra el camino optimo.

### Ejemplo 2: Nodo inalcanzable (grafo dirigido)

```
Tipo de grafo: D
Cantidad de nodos: 3
Nodos generados: A, B, C

Conexiones de A: (B,5)
Conexiones de B:
Conexiones de C: (A,3)

Nodo origen  : A
Nodo destino : C

Resultado: No existe camino de 'A' a 'C'
```

Explicacion: C apunta a A pero A no apunta a C. En grafo dirigido no hay camino de A a C.

### Ejemplo 3: Origen igual a destino

```
Nodo origen  : B
Nodo destino : B

Resultado: B | peso: 0
```

---

## Limitaciones conocidas

- **Complejidad O(n²):** La seleccion del minimo es lineal. Para grafos muy grandes (miles de nodos) seria preferible usar un heap de prioridad, pero esto requeriria `heapq` de la stdlib. Dado el requisito de no usar librerias, se mantiene la implementacion manual.
- **Nombres de nodos:** Los nombres son generados automaticamente. El usuario no puede elegir nombres personalizados como "Ciudad1" o "Router_A".
- **Sin visualizacion grafica:** La salida es exclusivamente por consola.
- **Pesos no negativos:** Dijkstra no funciona correctamente con pesos negativos. El programa rechaza pesos <= 0, lo cual garantiza que el algoritmo produce resultados correctos.
