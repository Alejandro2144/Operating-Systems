package Trabajos;

import kareltherobot.*;
import java.awt.Color;
import java.awt.Point;

public class MyRobot extends Robot implements Directions, Runnable {
    private Semaforo semaforo;

    public MyRobot(int street, int avenue, Directions.Direction direction, int beepers, Color badge, Semaforo semaforo) {
        super(street, avenue, direction, beepers, badge);
        this.semaforo = semaforo;
    }

    // Obtener la calle actual
    public int street() {
        String mensaje = this.toString();
        int posicion = mensaje.indexOf("street: ");
        int posFinal = mensaje.indexOf(")", posicion);
        return Integer.parseInt(mensaje.substring(posicion+8, posFinal));
    }

    // Obtener la avenida actual
    public int avenue() {
        String mensaje = this.toString()       ;
        int posicion = mensaje.indexOf("avenue: ");
        int posFinal = mensaje.indexOf(")", posicion);
        return Integer.parseInt(mensaje.substring(posicion+8, posFinal));
    }

    // Obtiene la proxima posición en funcion de la direccion del robot
    public Point calcularSiguientePosicion(){

        // Posicion inicial antes del movimiento
        int avenidaSiguiente = avenue();
        int calleSiguiente = street();

        if (facingEast()) {
            avenidaSiguiente++;
        } else if (facingWest()) {
            avenidaSiguiente--;
        } else if (facingSouth()) {
            calleSiguiente--;
        } else if (facingNorth()) {
            calleSiguiente++;
        }

        return new Point(avenidaSiguiente, calleSiguiente);
    }

    @Override
    public void move() {
        Point posicionActual = new Point(avenue(), street());
        Point siguientePosicion = calcularSiguientePosicion();

        try {
            // Esperar a que la siguiente posicion este libre
            semaforo.esperar(siguientePosicion);

            // Intentar ocupar el semáforo si existe en la siguiente posición
            while (semaforo.esSemaforo(siguientePosicion) && !semaforo.intentarOcuparSemaforo(siguientePosicion)) {
                semaforo.esperar(siguientePosicion);
            }

            // Actualizar la posición del robot en el semáforo
            semaforo.actualizarPosicion(siguientePosicion, true);

            // Realizar el movimiento
            super.move();

            // Liberar la posición actual
            semaforo.actualizarPosicion(posicionActual, false);

            // Liberar el semáforo en la posición anterior
            if (semaforo.esSemaforo(posicionActual)) {
                semaforo.liberarSemaforo(posicionActual);
            }

            // Notificar que el robot ha liberado el semáforo
            semaforo.notificar(posicionActual);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
