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
    public int street()
    {
        String mensaje = this.toString();
        int posicion = mensaje.indexOf("street: ");
        int posFinal = mensaje.indexOf(")", posicion);
        return Integer.parseInt(mensaje.substring(posicion+8, posFinal));
    }

    // Obtener la avenida actual
    public int avenue()
    {
        String mensaje = this.toString()       ;
        int posicion = mensaje.indexOf("avenue: ");
        int posFinal = mensaje.indexOf(")", posicion);
        return Integer.parseInt(mensaje.substring(posicion+8, posFinal));
    }

    // Obtiene la proxima posición dependiendo de a dónde este mirando el robot
    public void modificarPosicion()
    {
        // Posicion inicial antes del movimiento
        int avenidaActual = avenue();
        int calleActual = street();

        // Ver la siguiente casilla en funcion de la direccion
        int avenidaSiguiente = avenidaActual;
        int calleSiguiente = calleActual;

        if (facingEast()) {
            avenidaSiguiente++;
            semaforo.actualizarPosiciones(new Point(avenidaSiguiente, calleActual));
        } else if (facingWest()) {
            avenidaSiguiente--;
            semaforo.actualizarPosiciones(new Point(avenidaSiguiente, calleActual));
        } else if (facingSouth()) {
            calleSiguiente++;
            semaforo.actualizarPosiciones(new Point(avenidaActual, calleSiguiente));
        } else if (facingNorth()) {
            calleSiguiente--;
            semaforo.actualizarPosiciones(new Point(avenidaActual, calleSiguiente));
        }

    }

    @Override
    public synchronized void move() {
        // Antes del movimiento aqui hay que hacer lo siguiente:
        // Preguntar si a donde me voy a mover es semaforo y esta ocupado

        // Llamar a moverse de la logica original
        super.move();

        // Hacer algo despues del movimiento si es que es necesario
    }

}
