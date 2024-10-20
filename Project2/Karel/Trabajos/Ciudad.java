package Trabajos;

import kareltherobot.*;
import java.awt.Color;

public class Ciudad implements Directions {
    public static void main(String[] args) {

        // Leer el mapa del mundo
        World.readWorld("Mundo.kwld");
        World.setVisible(true);
        World.showSpeedControl(true, true);

        // Crear la instancia de semáforo que manejará las 44 intersecciones
        Semaforo semaforo = new Semaforo();

        // Instanciar los robots conductores
        Conductor[] robots = new Conductor[8];

        // Ubicar e inicializar el hilo de cada robot en el parqueadero
        for (int i = 0; i < 8; i++) {
            robots[i] = new Conductor(3, 16, East, 0, Color.blue, semaforo);
            new Thread(robots[i]).start();
        }
    }
}