from neopixel import *
import _rpi_ws281x as ws
import time
import random

# Variables de configuration de l'écran
LED_COUNT      = 64
LED_PIN        = 18
LED_FREQ_HZ    = 800000
LED_DMA        = 5
LED_BRIGHTNESS = 8
LED_INVERT     = False
CHANNEL        = 0
STRIP_TYPE     = ws.WS2811_STRIP_GRB

# Effacement complet de l'écran
def clearScreen(leds):
    for i in range(64):
        leds[i] = Color(0, 0, 0)

# Affichage de l'écran
def displayScreen(strip, leds):
    for i in range(64):
        strip.setPixelColor(i, leds[i])
    strip.show()

# Activation des leds du serpent
def addSnake(snake, leds):
    for (x, y) in snake:
        leds[x + y * 8] = Color(0, 255, 0)

# Désactivation des leds du serpent
def removeSnake(snake, leds):
    for (x, y) in snake:
        leds[x + y * 8] = Color(0, 0, 0)

# Calcul des novelles coordonnées du serpent
# pour un déplacement vers le haut
def snakeUp(snake):
    snake.pop()
    newLed_x, newLed_y = snake[0]
    if newLed_y == 0:
        newLed_y = 7
    else:
        newLed_y = newLed_y - 1
    snake.insert(0, (newLed_x, newLed_y))

# Calcul des novelles coordonnées du serpent
# pour un déplacement vers le bas
def snakeDown(snake):
    snake.pop()
    newLed_x, newLed_y = snake[0]
    if newLed_y == 7:
        newLed_y = 0
    else:
        newLed_y = newLed_y + 1
    snake.insert(0, (newLed_x, newLed_y))

# Calcul des novelles coordonnées du serpent
# pour un déplacement vers la droite
def snakeRight(snake):
    snake.pop()
    newLed_x, newLed_y = snake[0]
    if newLed_x == 7:
        newLed_x = 0
    else:
        newLed_x = newLed_x + 1
    snake.insert(0, (newLed_x, newLed_y))

# Calcul des novelles coordonnées du serpent
# pour un déplacement vers la gauche
def snakeLeft(snake):
    snake.pop()
    newLed_x, newLed_y = snake[0]
    if newLed_x == 0:
        newLed_x = 7
    else:
        newLed_x = newLed_x - 1
    snake.insert(0, (newLed_x, newLed_y))

# Changement aléatoire de direction
def changeDirection(direction):
    unauthorized = [1, 0, 3, 2]
    while True:
        newDirection = random.randint(0, 3)
        if newDirection != unauthorized[direction]:
            return newDirection


if __name__ == '__main__':
    # Position du serpent au départ
    serpent = [(2, 3), (2, 4), (2, 5)]
    # Initialisation des leds en noir
    leds = [Color(0, 0, 0)] * 64
    # Nombre de déplacements
    maxi = 99
    # Direction du serpent : 0 = haut, 1 = bas, 2= droite, 3 = gauche
    direction = 0

    # Création d'un élément permettant de "manipuler"
    # l'écran de leds
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, CHANNEL, STRIP_TYPE)

    # Initialisation de l'écran
    strip.begin()

    while maxi > 0:
        # Ajout du serpent sur l'écran
        addSnake(serpent, leds)
        # Affichage de l'écran
        displayScreen(strip, leds)
        # Attente de 0.1s
        time.sleep(0.1)
        # Effacement du serpent
        removeSnake(serpent, leds)
        # Changement de direction aléatoire
        #  tous les 5 déplacements
        if maxi % 5 == 0:
            direction = changeDirection(direction)
        # Déplacement (en mémoire) du serpent
        if direction == 0:
            snakeUp(serpent)
        elif direction == 1:
            snakeDown(serpent)
        elif direction == 2:
            snakeRight(serpent)
        else:
            snakeLeft(serpent)
        # Modification de la variable de boucle
        maxi = maxi - 1

    # Effacement de l'écran
    clearScreen(leds)
    displayScreen(strip, leds)
