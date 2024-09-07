package Trabajos;
import kareltherobot.*;
import java.awt.Color;
import java.util.Random;

public class Conductor extends Robot implements Runnable {

    private final int calleRecogida = 19; // Calle donde recoge el pasajero
    private final int avenidaRecogida = 8; // Avenida donde recoge el pasajero

    private int currentStreet;
    private int currentAvenue;

    final int[][] paradas = { {6, 16}, {7, 12}, {8, 8}, {19, 19} }; // Coordenadas de las paradas

    private Random random = new Random(); // Parada donde deja el pasajero

    public Conductor(int street, int avenue, Direction direction, int beepers, Color color){
        super(street, avenue, direction, beepers, color);
    }

    @Override
    public void run() {
        while (true){
            // Ir a recoger el pasajero
            irARecogerPasajero();

            // Recoger el pasajero
            recogerPasajero();

            // Elegir una parada aleatoria
            int paradaElegida = random.nextInt(paradas.length);

            // Llevar el pasajero a la parada elegida
            llevarPasajero(paradaElegida);

            // Dejar el pasajero
            dejarPasajero();

            // Regresar al punto de recogida
            regresar();
        }
    }

    private void irARecogerPasajero(){
        moverseA(calleRecogida, avenidaRecogida);
    }

    private void recogerPasajero(){
        if (nextToABeeper()) {
            pickBeeper();
        }
    }

    private void llevarPasajero(int indiceParada){
        int paradaX = paradas[indiceParada][0];
        int paradaY = paradas[indiceParada][1];
        moverseA(paradaX, paradaY);
    }

    private void dejarPasajero(){
        putBeeper();
    }

    private void regresar(){
        moverseA(calleRecogida, avenidaRecogida);
    }

    private void moverseA(int street, int avenue){
        while (currentStreet != street) {
            if (currentStreet < street && frontIsClear()) {
                move();
            } else {
                voltear();
                if (frontIsClear()) {
                    move();
                }
            }
        }
        while (currentAvenue != avenue) {
            if (currentAvenue < avenue && frontIsClear()) {
                move();
            } else {
                voltear();
                if (frontIsClear()) {
                    move();
                }
            }
        }
    }

    private void voltear(){
        turnLeft();
    }


}
