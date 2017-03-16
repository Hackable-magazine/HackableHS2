from neopixel import *
import _rpi_ws281x as ws
import time
import curses

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

# Initialisation de curses
def initCurses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    return stdscr

# Fermeture de curses
def closeCurses(stdscr):
    stdscr.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    # Position du serpent au départ
    serpent = [(2, 3), (2, 4), (2, 5)]
    # Initialisation des leds en noir
    leds = [Color(0, 0, 0)] * 64

    # Création d'un élément permettant de "manipuler"
    # l'écran de leds
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, CHANNEL, STRIP_TYPE)

    # Initialisation de l'écran
    strip.begin()

    stdscr = initCurses()

    while True:
        # Ajout du serpent sur l'écran
        addSnake(serpent, leds)
        # Affichage de l'écran
        displayScreen(strip, leds)
        # Attente de 0.1s
        time.sleep(0.1)
        # Effacement du serpent
        removeSnake(serpent, leds)
        #direction = changeDirection(direction)
        direction = stdscr.getch()
        stdscr.refresh()
        # Déplacement (en mémoire) du serpent
        if direction == curses.KEY_UP:
            snakeUp(serpent)
        elif direction == curses.KEY_DOWN:
            snakeDown(serpent)
        elif direction == curses.KEY_RIGHT:
            snakeRight(serpent)
        elif direction == curses.KEY_LEFT:
            snakeLeft(serpent)
        elif direction == 27:
            closeCurses(stdscr)
            break

    # Effacement de l'écran
    clearScreen(leds)
    displayScreen(strip, leds)
