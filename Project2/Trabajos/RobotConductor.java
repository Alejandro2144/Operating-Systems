package Trabajos;

import kareltherobot.*;
import java.awt.Color;
import java.util.Random;

public class RobotConductor extends Robot implements Runnable {

    private final RobotMover mover;
    private static final Random random = new Random();

    public RobotConductor(int street, int avenue, Direction direction, int beepers, Color color) {
        super(street, avenue, direction, beepers, color);
        World.setupThread(this);
        this.mover = new RobotMover(this);
    }

    @Override
    public void run() {
        int parada = seleccionarParada();
        mover.moverHaciaParada(parada);
    }

    private int seleccionarParada() {
        int parada = random.nextInt(4) + 1;
        System.out.println("El robot va hacia la parada " + parada);
        return parada;
    }
}
