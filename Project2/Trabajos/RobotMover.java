package Trabajos;

import kareltherobot.*;

public class RobotMover {

    private final Robot robot;

    public RobotMover(Robot robot) {
        this.robot = robot;
    }

    public void moverHaciaParada(int parada) {
        switch (parada) {
            case 1,2,3,4:
                irAParada1YRegresar();
                break;
                /*
            case 2:
                irAParada2();
                break;
            case 3:
                irAParada3();
                break;
            case 4:
                irAParada4();
                break;
                 */
            default:
                System.out.println("Parada inválida");
        }
    }

    private void irAParada1YRegresar() {
        mover(2);
        girarAlNorte();
        moverYPick(5);
        girarAlOeste();
        mover(8);
        girarAlSur();
        mover(6);
        girarAlOeste();
        mover(9);
        girarAlNorte();
        mover(16);
        girarAlEste();
        mover(4);
        girarAlSur();
        moverYPut(3);
        girarAlOeste();
        mover(3);
        girarAlNorte();
        mover(1);
        girarAlEste();
        mover(3);
        girarAlNorte();
        mover(2);
        girarAlEste();
        mover(3);
        girarAlSur();
        mover(4);
        girarAlOeste();
        mover(6);
        girarAlSur();
        mover(5);
        girarAlEste();
        mover(14);
        girarAlNorte();
        mover(1);
        girarAlOeste();
        mover(7);
        girarAlNorte();
        mover(8);
        girarAlEste();
        mover(7);
        girarAlNorte();
        mover(1);
        girarAlOeste();
        mover(16);
        girarAlSur();
        mover(18);
        girarAlEste();
        mover(18);
        girarAlNorte();
        // aca debemos pensar que se debe volver a reasignar la parada aleatoria para el robot
        moverYPick(7);

    }

    private void irAParada2() {
        // Completar con parada 2
    }

    private void irAParada3() {
        // Completar con parada 3
    }

    private void irAParada4() {
        // Completar con parada 4
    }

    private void moverYPick(int pasos) {
        mover(pasos);
        robot.pickBeeper();
    }

    private void moverYPut(int pasos) {
        mover(pasos);
        robot.putBeeper();
    }

    private void mover(int pasos) {
        for (int i = 0; i < pasos; i++) {
            robot.move();
        }
    }

    public void girarAlNorte() {
        while (!robot.facingNorth()) {
            robot.turnLeft();
        }
    }

    public void girarAlSur() {
        while (!robot.facingSouth()) {
            robot.turnLeft();
        }
    }

    public void girarAlEste() {
        while (!robot.facingEast()) {
            robot.turnLeft();
        }
    }

    public void girarAlOeste() {
        while (!robot.facingWest()) {
            robot.turnLeft();
        }
    }
}
