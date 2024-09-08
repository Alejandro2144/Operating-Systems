package Trabajos;

import kareltherobot.*;

import java.awt.Color;

public class TrafficManagement implements Directions {
    public static void main(String[] args) {

        World.readWorld("Mapa.kwld");
        World.setVisible(true);
        World.showSpeedControl(true, true);

        RobotConductor robot1 = new RobotConductor(3, 17, East, 0, Color.red);

        new Thread(robot1).start();
    }
}
