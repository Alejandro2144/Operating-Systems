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

            // Verificar si hay un robot en la siguiente posición
            MyRobot otroRobot = semaforo.obtenerRobotEnPosicion(siguientePosicion);

            if (otroRobot != null) {
                // Si hay un deadlock cara a cara (direcciones opuestas)
                if (esDeadlock(otroRobot)) {
                    resolverDeadlock(otroRobot);
                    return;  // No intentar moverse hasta que se resuelva el deadlock
                }
            }

            // Intentar ocupar el semáforo si existe en la siguiente posición
            while (semaforo.esSemaforo(siguientePosicion) && !semaforo.intentarOcuparSemaforo(siguientePosicion)) {
                semaforo.esperar(siguientePosicion);
            }

            // Actualizar la posición del robot en el semáforo
            semaforo.actualizarPosicion(siguientePosicion, true);
            semaforo.actualizarPosicionRobot(this, posicionActual, siguientePosicion);  // Actualizar posición del robot

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

    // Metodo para detectar si hay un deadlock entre robots mirando en direcciones opuestas
    public boolean esDeadlock(MyRobot otroRobot) {
        // Variables para almacenar el resultado de las comparaciones
        boolean deadlockNorteSur = (this.facingNorth() && otroRobot.facingSouth()) || (this.facingSouth() && otroRobot.facingNorth());
        boolean deadlockEsteOeste = (this.facingEast() && otroRobot.facingWest()) || (this.facingWest() && otroRobot.facingEast());

        // Si hay un deadlock norte-sur
        if (deadlockNorteSur) {
            System.out.println("Deadlock: Un robot está mirando al norte y el otro al sur.");
        }

        // Si hay un deadlock este-oeste
        if (deadlockEsteOeste) {
            System.out.println("Deadlock: Un robot está mirando al este y el otro al oeste.");
        }

        // Retornar true si ocurre cualquier tipo de deadlock
        return deadlockNorteSur || deadlockEsteOeste;
    }

    // Metodo para resolver el deadlock
    public void resolverDeadlock(MyRobot otroRobot) {
        // Aquí puedes implementar la lógica para resolver el deadlock
        boolean deadlockNorteSur = (this.facingNorth() && otroRobot.facingSouth()) || (this.facingSouth() && otroRobot.facingNorth());
        boolean deadlockEsteOeste = (this.facingEast() && otroRobot.facingWest()) || (this.facingWest() && otroRobot.facingEast());

        if (deadlockNorteSur) {
            System.out.println("Resolviendo deadlock entre robots en direcciones norte-sur.");
            if (this.facingNorth()) {
                retroceder();  // Retroceder este robot
            } else {
                otroRobot.retroceder();  // Retroceder el otro robot
            }
        } else if (deadlockEsteOeste) {
            System.out.println("Resolviendo deadlock entre robots en direcciones este-oeste.");
            if (this.facingEast()) {
                retroceder();  // Retroceder este robot
            } else {
                otroRobot.retroceder();  // Retroceder el otro robot
            }
        }
    }

    // Metodo para retroceder el robot en caso de deadlock
    public void retroceder() {
        // pass
    }


}
