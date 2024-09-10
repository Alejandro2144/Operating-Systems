package Trabajos;

import kareltherobot.*;
import java.awt.Color;

public class Ciudad implements Directions {
    public static void main(String[] args) {

        // Leer el mapa
        World.readWorld("Mundo.kwld");
        World.setVisible(true);
        World.showSpeedControl(true, true);

        // Crear las instancias de los robots
        Conductor[] robots = new Conductor[10];

        // Ubicar los robots en el parqueadero
        for (int i = 0; i < 10; i++) {
            robots[i] = new Conductor(3, 16, East, 0, Color.blue);
        }

        // Inicializar los hilos para manejar los robots
        for (Conductor robot : robots) {
            new Thread(robot).start();

            //new Thread(() -> {
                // AQUÍ: RECIBIR VIAJE, RECOGER PASAJERO, LLEVAR PASAJERO, DEJAR PASAJERO, REGRESAR POR PASAJERO, RECIBIR VIAJE, RECOGER PASAJERO
            //}).start();
        }
    }
}