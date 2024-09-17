package Trabajos;

import java.awt.Point;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.ConcurrentHashMap;

public class Semaforo {
    private final ConcurrentHashMap<Point, ReentrantLock> semaforos; // <Coordenada, Ocupado>
    private final ConcurrentHashMap<Point, Boolean> posiciones; // true: ocupado, false: libre
    private final ConcurrentHashMap<Point, Condition> condiciones;

    public Semaforo() {
        semaforos = new ConcurrentHashMap<>();
        posiciones = new ConcurrentHashMap<>();
        condiciones = new ConcurrentHashMap<>();
        inicializarSemaforos();
    }

    private void inicializarSemaforos() {

        // Posiciones de los semaforos (x: avenue, y: street): 46 semaforos
        int[][] coordenadas = {
                {19, 3}, {19, 8}, {11, 8}, {11, 2}, {2, 2}, {2, 18}, {6, 18}, {9, 18},
                {9, 14}, {3, 14}, {3, 9}, {6, 9}, {10, 9}, {17, 9}, {17, 10}, {15, 10},
                {15, 11}, {11, 11}, {11, 15}, {15, 15}, {15, 13}, {17, 13}, {17, 16},
                {12, 16}, {12, 17}, {18, 17}, {18, 12}, {18, 9}, {19, 9}, {19, 18},
                {10, 10}, {7, 10}, {6, 10}, {6, 6}, {8, 6}, {10, 6}, {10, 18}, {7, 12},
                {17, 18}, {17, 19}, {1, 19}, {1, 1}, {19, 1}, {19, 2}, {16, 2}, {6, 16}
        };

        // Inicializamos todos los semaforos
        for (int[] coordenada : coordenadas) {
            Point point = new Point(coordenada[0], coordenada[1]);
            ReentrantLock lock = new ReentrantLock();

            semaforos.put(point, lock);
            posiciones.put(point, false); // Inicialmente libre
            condiciones.put(point, lock.newCondition()); // Crear condicion para cada semaforo
        }

        System.out.println(semaforos.size());
    }

    public void actualizarPosicion(Point posicion, boolean ocupado){
        System.out.println("Estoy actualizando posicion" + posicion + " a " + ocupado);
        posiciones.put(posicion, ocupado);
    }

    public boolean esPuntoOcupado(Point posicion){
        System.out.println("Preguntando si el punto " + posicion + " esta ocupado");
        return posiciones.getOrDefault(posicion, false); // Retorna true si el punto esta ocupado
    }

    public boolean esSemaforo(Point posicion) {
        System.out.println("El punto " + posicion + " es semaforo? " + semaforos.containsKey(posicion));
        return semaforos.containsKey(posicion);
    }

    // Este metodo intenta obtener un bloqueo para el semaforo en posicion
    public boolean intentarOcuparSemaforo(Point posicion) {
        ReentrantLock lock = semaforos.get(posicion);
        if (lock != null) {
            try{
                // Si el semaforo esta libre devuelve true
                return lock.tryLock();
            } catch (Exception e) {
                Thread.currentThread().interrupt();
            }
        }
        // Si no esta libre devuelve false (aqui el bloqueo no se pudo obtener)
        return false;
    }

    public void liberarSemaforo(Point posicion) {
        ReentrantLock lock = semaforos.get(posicion);
        if (lock != null && lock.isHeldByCurrentThread()) {
            lock.unlock();
        }
    }

    public void esperar(Point posicion) throws InterruptedException {
        ReentrantLock lock = semaforos.get(posicion);

        // Si es un semaforo
        if (lock != null) {
            lock.lock();
            try {
                while(esPuntoOcupado(posicion)) {
                    condiciones.get(posicion).await();
                }
            } finally {
                lock.unlock();
            }
        } else {
            // Si la posicion no tiene semaforo, simplemente esperar si esta ocupada
            synchronized (posiciones) {
                System.out.println("Entre a synchronized");
                while (esPuntoOcupado(posicion)) {
                    posiciones.wait();
                }
            }
        }
    }

    // Esto notifica a los hilos de que esta condicion se ha resuelto
    public void notificar(Point posicion) {
        ReentrantLock lock = semaforos.get(posicion);
        if (lock != null) {
            lock.lock();
            try {
                condiciones.get(posicion).signalAll(); // Notificar a los que esperan
            } finally {
                lock.unlock();
            }
        } else {
            // Notificar a los robots que esperen en posiciones sin semaforo
            synchronized (posiciones) {
                posiciones.notify();
            }
        }
    }
}