# ----- LIBRERIAS ----- #

# random -> permite generar acciones aleatorias
import random
# time -> permite hacer pausas entre acciones para que la batalla se vea más dinámica
import time
# ABC y abstractmethod -> sirven para crear clases abstractas
from abc import ABC, abstractmethod


# ----- CLASE BATALLA ----- #

class Batalla:

    # Constructor de la batalla
    # Recibe dos personajes que pelearán
    def __init__(self, player_1, player_2):
        # Guarda el primer jugador
        self.player_1 = player_1
        # Guarda el segundo jugador
        self.player_2 = player_2
        # Variable que controla el turno actual
        self.turno = 1


    # Método principal que inicia la batalla
    def iniciar(self):
        # Mensaje inicial
        print("\n ¡COMIENZA LA BATALLA! ")
        # Ciclo principal:
        # se ejecuta mientras ambos jugadores tengan vida
        while self.player_1.esta_vivo() and self.player_2.esta_vivo():
            print(f"\n========== TURNO {self.turno} ==========")
            # Mostrar estado actual de los personajes
            self.mostrar_estado()

            # ----- TURNO PLAYER 1 ----- #
            # Elige una acción aleatoria:
            # True = atacar
            # False = defender
            accion = random.choice(["atacar", "defender"])
            # Si la acción es atacar
            if accion == "atacar":
                self.player_1.atacar(self.player_2)
            # Si la acción es defender
            else:
                self.player_1.defender()

            # Verifica si el jugador 2 murió
            if not self.player_2.esta_vivo():
                break
            # Pausa de 1 segundo
            time.sleep(1)

            # ----- TURNO PLAYER 2 ----- #
            accion = random.choice(["atacar", "defender"])
            if accion == "atacar":
                self.player_2.atacar(self.player_1)
            else:
                self.player_2.defender()
            # Verifica si el jugador 1 murió
            if not self.player_1.esta_vivo():
                break
            # Aumenta el contador de turnos
            self.turno += 1
            # Pausa visual
            time.sleep(1)
        # Cuando termina el ciclo, se anuncia el ganador
        self.hay_ganador()


    # Método que muestra la vida de ambos personajes
    def mostrar_estado(self):
        print(f"\n Estado actual:")
        # Imprime información del jugador 1
        print(self.player_1)
        # Imprime información del jugador 2
        print(self.player_2)
        # Pequeña pausa
        time.sleep(1)


    # Método que determina quién ganó
    def hay_ganador(self):
        # Si player_1 tiene vida, es el ganador
        ganador = self.player_1 if self.player_1.get_vida() > 0 else self.player_2
        # Determina quién perdió
        perdedor = self.player_2 if ganador == self.player_1 else self.player_1
        # Mensaje final
        print(f"\n ¡{ganador.nombre} ganó la batalla!")
        print(f" {perdedor.nombre} fue derrotado")


# ----- CLASE ABSTRACTA PERSONAJE ----- #

class Personaje(ABC):

    # Constructor general para todos los personajes
    def __init__(self, nombre, vida, defensa):
        # Nombre del personaje
        self.nombre = nombre
        # Vida privada (encapsulamiento)
        self.__vida = 0
        # Usa setter para validar la vida
        self.set_vida(vida)
        # Defensa privada
        self.__defensa = defensa
        # Variable que indica si está defendiendo
        self.__defendiendo = False


    # ----- GETTERS Y SETTERS ----- #

    # Devuelve la vida actual
    def get_vida(self):
        return self.__vida


    # Devuelve la defensa
    def get_defensa(self):
        return self.__defensa


    # Cambia la vida validando límites
    def set_vida(self, valor):
        # Si la vida baja de 0
        if valor < 0:
            self.__vida = 0
        # Si supera 100
        elif valor > 100:
            self.__vida = 100
        # Valor válido
        else:
            self.__vida = valor


    # ----- MÉTODOS DE DEFENSA ----- #

    # Activa el modo defensa
    def defender(self):
        # Cambia el estado a defendiendo
        self.__defendiendo = True
        print(f" {self.nombre} se pone en defensa")


    # Método que recibe daño
    def recibir_danio(self, danio):
        # Si estaba defendiendo
        if self.__defendiendo:
            # Reduce el daño a la mitad
            danio = int(danio * 0.5)
            print(f" {self.nombre} reduce el daño a {danio}")
        # Resta el daño a la vida
        self.set_vida(self.get_vida() - danio)
        # Desactiva defensa después de recibir golpe
        self.__defendiendo = False


    # Método que verifica si sigue vivo
    def esta_vivo(self):
        # Devuelve True si la vida es mayor a 0
        return self.__vida > 0


    # Método especial para imprimir objetos fácilmente
    def __str__(self):
        return f"{self.nombre} |  Vida: {self.__vida}"


    # Método abstracto:
    # obliga a las clases hijas a implementar atacar()
    @abstractmethod
    def atacar(self, enemigo):
        pass


# ----- CLASE GUERRERO ----- #
class Guerrero(Personaje):
    # Constructor del guerrero
    def __init__(self, nombre):
        # vida = 100
        # defensa = 20
        super().__init__(nombre, 100, 20)


    # Ataque especial del guerrero
    def atacar(self, enemigo):
        # Fórmula de daño
        danio = int((30 * 1.2) - enemigo.get_defensa())
        # Evita daño negativo
        danio = max(0, danio)
        print(f" {self.nombre} ataca a {enemigo.nombre} causando {danio} de daño")
        # Aplica daño al enemigo
        enemigo.recibir_danio(danio)


# ----- CLASE MAGO ----- #
class Mago(Personaje):
    # Constructor del mago
    def __init__(self, nombre):
        # vida = 80
        # defensa = 10
        super().__init__(nombre, 80, 10)


    # Ataque especial del mago
    def atacar(self, enemigo):
        # Daño mágico
        danio = int((30 * 1.2) - enemigo.get_defensa())
        # Evita negativos
        danio = max(0, danio)
        print(f" {self.nombre} lanza un hechizo a {enemigo.nombre} causando {danio} de daño")
        # El enemigo recibe daño
        enemigo.recibir_danio(danio)


# ----- CLASE ARQUERO ----- #
class Arquero(Personaje):
    # Constructor del arquero
    def __init__(self, nombre):
        # vida = 90
        # defensa = 15
        super().__init__(nombre, 90, 15)


    # Ataque especial del arquero
    def atacar(self, enemigo):
        # Daño del disparo
        danio = int((30 * 1.2) - enemigo.get_defensa())
        # Evita negativos
        danio = max(0, danio)
        print(f" {self.nombre} dispara una flecha a {enemigo.nombre} causando {danio} de daño")
        # El enemigo recibe daño
        enemigo.recibir_danio(danio)

if __name__ == "__main__":

    print(" SELECCIONA TU PERSONAJE")
    print("1. Guerrero")
    print("2. Mago")
    print("3. Arquero")

    opcion = input("Seleccione una opción: ")

    # Crear personaje jugador
    if opcion == "1":
        nombre = input("Ingrese nombre del Guerrero: ")
        jugador = Guerrero(nombre)
    elif opcion == "2":
        nombre = input("Ingrese nombre del Mago: ")
        jugador = Mago(nombre)
    elif opcion == "3":
        nombre = input("Ingrese nombre del Arquero: ")
        jugador = Arquero(nombre)
    else:
        print(" Opción inválida")
        exit()


    # Lista de enemigos posibles
    enemigos = [
        Guerrero("Kratos"),
        Mago("Gandalf"),
        Arquero("Legolas")
    ]

    # Elegir enemigo aleatorio
    enemigo = random.choice(enemigos)

    # Evita que salga el mismo personaje
    while enemigo.nombre == jugador.nombre:
        enemigo = random.choice(enemigos)

    print(f"\n Tu enemigo será: {enemigo.nombre}")

    # Crear batalla
    batalla = Batalla(jugador, enemigo)

    # Iniciar juego
    batalla.iniciar()