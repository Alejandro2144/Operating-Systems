# Proyecto #3

## Diferencias entre los tipos de procesamiento

### Procesamiento secuencial

*Tiempo de ejecución:* Este es el más lento de los tres métodos, especialmente para muchos archivos o archivos muy grandes
*Uso de memoria:* Debería ser el más bajo ya que procesa un archivo a la vez
*Ventajas:* Es sencillo de implementar y técnicamente puede ser predecible en términos de uso de recursos
*Desventajas:* No aprovecha los recursos de multiprocesamiento de la máquina

### Procesamiento paralelo en un solo núcleo

*Tiempo de ejecución:* Cada archivo se procesa más lento que el secuencial pero como se procesan en paralelo el programa demora menos
*Uso de memoria:* Es mayor que el secuencial ya que mantiene múltiples archivos en la memoria simultáneamente
*Ventajas:* Es mas eficiente al manejar las esperas de I/O lo que le permite procesar otros archivos mientras espera
*Desventajas:* Esta limitado por la capacidad de un solo núcleo

### Procesamiento paralelo en múltiples núcleos

*Tiempo de ejecución:* Es el más rápido especialmente en máquinas que tienen multiples nucleos
*Uso de memoria:* Es, potencialmente, el más alto ya que cada nucleo puede estar procesando un archivo diferente simultáneamente
*Ventajas:* Aprovecha al máximo los recursos de procesamiento de la máquina
*Desventajas:* Es más complejo de implementar y puede generar problemas de concurrencia

## Diferencias esperadas:

### Tiempo de ejecución:

Secuencial > Paralelo en un núcleo > Paralelo en múltiples núcleos
La mejora será más notable cuanto mayor sea el número de archivos y la cantidad de datos a procesar
Para conjuntos de datos pequeños, la diferencia puede ser menos significativa debido al overhead de crear y gestionar múltiples procesos

### Uso de memoria:

Secuencial < Paralelo en un núcleo < Paralelo en múltiples núcleos
El uso de memoria en los métodos paralelos dependerá del número de archivos procesados simultáneamente y del tamaño de los chunks

### Escalabilidad:

El método paralelo en múltiples núcleos debería escalar mejor con el aumento del número de núcleos disponibles
El método paralelo en un solo núcleo puede mostrar mejoras significativas sobre el secuencial para operaciones con mucha I/O, pero tendrá un límite de mejora

### Eficiencia del CPU:

El método paralelo en múltiples núcleos debería mostrar la mayor utilización del CPU
El método secuencial mostrará la menor utilización del CPU, especialmente en sistemas multinúcleo

## Diferencias obtenidas:

### Máquina: MacBook Pro, Apple M1, 8 GB de RAM, MacOS: Sonoma 14.3

*Tiempo de ejecución del programa:* 
    - Secuencial: 5.37 segundos
    - Un Solo Núcleo: 1.44 segundos
    - Multiples Núcleos: 1.76 segundos

*Uso promedio de memoria:*  
    - Secuencial: 92.87 MB
    - Un Solo Núcleo: 48.42 MB
    - Multiples Núcleos: 141.81 MB

*Duración media por archivo:* 
    - Secuencial: 536.41 ms
    - Un Solo Núcleo: 1024.43 ms
    - Multiples Núcleos: 908.33 ms

### Comparación de diferencias esperadas vs diferencias obtenidas:

*Tiempo de ejecución del programa:* Secuencial > Múltiples Núcleos > Un Solo Núcleo

Esto quiere decir que el tiempo de ejecución del programa en secuencial fue más lento que en múltiples núcleos y más lento que en un solo núcleo.
Lo esperado era que la ejecución del programa en un solo núcleo fuera más lenta que en múltiples núcleos.

*Uso promedio de memoria:* Un Solo Núcleo < Secuencial < Múltiples Núcleos

Esto quiere decir que el uso promedio de memoria del programa en un solo núcleo fue mucho menor que en secuencial y que en múltiples núcleos.
Lo esperado era que el uso promedio de memoria del programa en secuencial fuera menor que en un solo núcleo.





