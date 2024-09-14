package Trabajos;

import java.util.HashMap;
import java.awt.Point;
import java.util.concurrent.locks.ReentrantLock;

public class Semaforo {
    private final HashMap<Point, Boolean> semaforos; // <Coordenada, Ocupado>
    private HashMap<Boolean, Point> posiciones; // <EnSemaforo, Coordenada>

    public Semaforo() {
        semaforos = new HashMap<>();
        posiciones = new HashMap<>();
        inicializarSemaforos();
    }

    private void inicializarSemaforos() {

        // Posiciones de los semaforos
        int[][] coordenadas = {
                {19, 3}, {19, 8}, {11, 8}, {11, 2}, {2, 2}, {2, 18}, {6, 18}, {9, 18},
                {9, 14}, {3, 14}, {3, 9}, {6, 9}, {10, 9}, {17, 9}, {17, 10}, {15, 10},
                {15, 11}, {11, 11}, {11, 15}, {15, 15}, {15, 13}, {17, 13}, {17, 16},
                {12, 16}, {12, 17}, {18, 17}, {18, 12}, {18, 9}, {19, 9}, {19, 18},
                {10, 10}, {7, 10}, {6, 10}, {6, 6}, {8, 6}, {10, 6}, {10, 18},
                {17, 18}, {17, 19}, {1, 19}, {1, 1}, {19, 1}, {19, 2}, {16, 2}
        };

        // Inicializamos todos los semaforos como libres
        for (int[] coordenada : coordenadas) {
            semaforos.put(new Point(coordenada[0], coordenada[1]), false);
        }
    }

    public void actualizarPosiciones(Point posicion) {
        // Aqui hay que actualizar la posicion del robot y poner en true si la posicion a la que llego es semaforo
    }
}