# Proyecto #3

Este proyecto aborda el procesamiento eficiente de archivos CSV de gran tamaño mediante paralelismo y concurrencia en Python. La implementación se realizó en tres modos de ejecución distintos: secuencial, single-core y multi-core, para comparar su rendimiento en términos de tiempo de carga y uso de memoria.

## Descripción de los Modos de Ejecución

1. **Modo Secuencial**:  
   Cada archivo se procesa de manera individual, cargándolo en memoria antes de pasar al siguiente. Esto permite un control detallado del uso de recursos, pero limita la velocidad de procesamiento.

2. **Modo Single-Core**:  
   Usando `ThreadPoolExecutor`, los archivos se procesan en paralelo, pero limitados a un solo núcleo. Cada archivo se asigna a un hilo que lee en fragmentos, optimizando el uso de memoria. Aunque se mejora la velocidad en comparación con el modo secuencial, la limitación a un solo núcleo reduce la eficiencia en sistemas multicore.

3. **Modo Multi-Core**:  
   Se emplea `ProcessPoolExecutor` para distribuir el procesamiento en varios núcleos. Cada proceso crea hilos adicionales para leer fragmentos del archivo en paralelo, maximizando el rendimiento. Este método muestra la mayor eficiencia al utilizar todos los núcleos disponibles.

## Análisis de Resultados

- En el **modo secuencial**, el procesamiento es lento debido a la carga individual de cada archivo sin paralelismo, con un tiempo total de 6.31 segundos.
- El **modo single-core** mejora el rendimiento mediante la carga paralela de múltiples archivos en un solo núcleo, alcanzando un tiempo total de 6.10 segundos.
- En el **modo multi-core**, el tiempo total se reduce significativamente a 1.29 segundos, aprovechando el uso de todos los núcleos y la carga en fragmentos.

## Conclusiones

- La implementación de paralelismo y concurrencia reduce el tiempo de procesamiento, siendo el multi-core el método más eficiente.
- La lectura en fragmentos permite manejar archivos grandes sin agotar la memoria.
- La detección de codificación es crucial para la correcta lectura de archivos, aunque introduce un leve retraso.
- La elección del modo de ejecución depende de los recursos del sistema y los requisitos específicos de procesamiento.




