package Trabajos;

import kareltherobot.*;
import java.awt.Color;
import java.util.Random;

public class Conductor extends MyRobot implements Runnable {

    private final Random random = new Random(); // Parada donde deja el pasajero
    private int pasajerosDisponibles = 1000; // Cantidad de pasajeros disponibles


    public Conductor(int street, int avenue, Direction direction, int beepers, Color color, Semaforo semaforo) {
        super(street, avenue, direction, beepers, color, semaforo);
    }

    @Override
    public void run() {
        while (pasajerosDisponibles > 0) {
            // Ir a recoger el pasajero
            irARecogerPasajero();

            // Recoger el pasajero
            recogerPasajero();

            // Elegir una parada aleatoria
            int paradaElegida = seleccionarParada();

            // Llevar el pasajero a la parada elegida
            llevarPasajero(paradaElegida);

            // Dejar el pasajero
            dejarPasajero();

            // Regresar al punto de recogida
            regresar(paradaElegida);
        }
    }

    private int seleccionarParada(){
        int parada = random.nextInt(4) + 1;
        System.out.println("El robot va hacia la parada: " + parada);
        return parada;
    }

    private void irARecogerPasajero(){
        mover(3);
        girarAlNorte();
        mover(5);
        girarAlOeste();
    }

    private void recogerPasajero(){
        pickBeeper();
        pasajerosDisponibles--;
    }

    private void llevarPasajero(int paradaElegida){
        switch (paradaElegida){
            case 1:
                irAParada1();
                break;
            case 2:
                irAParada2();
                break;
            case 3:
                irAParada3();
                break;
            case 4:
                irAParada4();
                break;
            default:
                System.out.println("Parada inválida");
        }
    }

    private void dejarPasajero(){
        putBeeper();
    }

    private void regresar(int paradaElegida){
        switch (paradaElegida){
            case 1:
                regresarDesdeParada1();
                break;
            case 2:
                regresarDesdeParada2();
                break;
            case 3:
                regresarDesdeParada3();
                break;
            case 4:
                regresarDesdeParada4();
                break;
            default:
                System.out.println("Parada inválida");
        }
    }

    private void mover(int pasos){
        for (int i = 0; i < pasos; i++){
            move();
        }
    }

    public void girarAlNorte() {
        while (!facingNorth()) {
            turnLeft();
        }
    }

    public void girarAlSur() {
        while (!facingSouth()) {
            turnLeft();
        }
    }

    public void girarAlEste() {
        while (!facingEast()) {
            turnLeft();
        }
    }

    public void girarAlOeste() {
        while (!facingWest()) {
            turnLeft();
        }
    }

    private void irAParada1(){
        entrarAlBloqueDeParadas();
        mover(4);
        girarAlSur();
        mover(3);
    }

    private void irAParada2(){
        entrarAlBloqueDeParadas();
        mover(7);
        girarAlSur();
        mover(4);
        girarAlOeste();
        mover(6);
        girarAlSur();
        mover(5);
        girarAlEste();
        mover(3); // Aqui se entra a la interseccion (avenue 6, street 9)
        mover(4); // Aqui se entra a la interseccion (avenue 10, street 9)
        mover(7);
        girarAlNorte();
        mover(1);
        girarAlOeste();
        mover(7); // Aqui se entra a la interseccion (avenue 10, street 10)
        mover(3);
        girarAlNorte();
        mover(3);
    }

    private void irAParada3(){
        entrarAlBloqueDeParadas();
        mover(7);
        girarAlSur();
        mover(4);
        girarAlOeste();
        mover(6);
        girarAlSur();
        mover(5);
        girarAlEste();
        mover(3); // Aqui se entra a la interseccion (avenue 6, street 9)
        girarAlSur();
        mover(3);
        girarAlEste();
        mover(2);
        girarAlNorte();
        mover(2);
    }

    private void irAParada4(){
        entrarAlBloqueDeParadas();
        mover(7);
        girarAlSur();
        mover(4);
        girarAlOeste();
        mover(6);
        girarAlSur();
        mover(5);
        girarAlEste();
        mover(3); // Aqui se entra a la interseccion (avenue 6, street 9)
        mover(4); // Aqui se entra a la interseccion (avenue 10, street 9)
        mover(7);
        girarAlNorte();
        mover(1);
        girarAlOeste();
        mover(2);
        girarAlNorte();
        mover(1); // Aqui podria mover 2 para llegar a la zona de descanso en (avenue 15, street 12)
        girarAlOeste();
        mover(4);
        girarAlNorte();
        mover(4);
        girarAlEste();
        mover(4); // Aqui podria mover 5 para llegar a la zona de descanso en (avenue 16, street 15)
        girarAlSur();
        mover(2);
        girarAlEste();
        mover(2);
        girarAlNorte();
        mover(3);
        girarAlOeste();
        mover(5); // Aqui podria mover 6 para llegar a la zona de descanso en (avenue 11, street 16)
        girarAlNorte();
        mover(1);
        girarAlEste();
        mover(6);
        girarAlSur();
        mover(8); // Aqui podria mover 5 para llegar a la zona de descanso en (avenue 17, street 12)
        girarAlEste();
        mover(1);
        girarAlNorte();
        mover(10);
    }

    private void regresarDesdeParada1() {
        girarAlNorte();
        mover(3);
        girarAlEste();
        mover(3);
        girarAlSur();
        mover(4);
        girarAlOeste();
        mover(6);
        girarAlSur();
        mover(5);
        girarAlEste();
        mover(7); // Aqui se entra a la interseccion (avenue, 10, street 9)
        girarAlNorte();
        mover(1); // Aqui se entra a la interseccion (avenue, 10, street 10)
        regresarDesdeLaInterseccion();
    }

    private void regresarDesdeParada2() {
        girarAlSur();
        mover(3);
        girarAlOeste();
        mover(1);
        girarAlSur();
        mover(1); // Aqui se entra a la interseccion (avenue 6, street 9)
        mover(3);
        girarAlEste();
        mover(4);
        girarAlNorte();
        mover(4); // Aqui se entra a la interseccion (avenue, 10, street 10)
        regresarDesdeLaInterseccion();
    }

    private void regresarDesdeParada3() {
        girarAlSur();
        mover(2);
        girarAlEste();
        mover(2);
        girarAlNorte();
        mover(4); // Aqui se entra a la interseccion (avenue, 10, street 10)
        regresarDesdeLaInterseccion();
    }

    private void regresarDesdeParada4() {
        girarAlSur();
        mover(10);
        girarAlOeste();
        mover(1);
        girarAlNorte();
        mover(8); // Aqui podria mover 3 para llegar al punto de descanso en (avenue 17, street 12)
        girarAlOeste();
        mover(6);
        girarAlSur();
        mover(1); // Luego de esto podria girar al oeste y mover 1 para entrar al punto de descanso en (avenue 11, street 16)
        girarAlEste();
        mover(5);
        girarAlSur();
        mover(3);
        girarAlOeste();
        mover(2);
        girarAlNorte();
        mover(2); // Luego de esto podria girar al este y mover 1 para entrar al punto de descanso en (avenue 16, street 15)
        girarAlOeste();
        mover(4);
        girarAlSur();
        mover(4);
        girarAlEste();
        mover(4); // Luego de esto podria girar al norte y mover 1 para entrar al punto de descanso en (avenue 15, street 12)
        girarAlSur();
        mover(1);
        girarAlOeste();
        mover(5); // Aqui se entra a la interseccion (avenue, 10, street 10)
        girarAlNorte();
        regresarDesdeLaInterseccion();

    }

    private void regresarDesdeLaInterseccion(){
        // Esta intersección es el punto (avenue 10, street 10)
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
        mover(1);
        girarAlOeste();
        mover(3);
        girarAlNorte();
        mover(1);
        girarAlEste(); // Esto lo deja en el punto de partida
    }

    private void entrarAlBloqueDeParadas(){
        // Esto me deja en el punto (avenue 2, street 18)
        mover(8);
        girarAlSur();
        mover(6);
        girarAlOeste();
        mover(9);
        girarAlNorte();
        mover(16);
        girarAlEste();
    }

}