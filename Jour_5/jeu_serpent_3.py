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

# Activation générique des leds
def addElement(elt, leds, color):
    for (x, y) in elt:
        leds[x + y * 8] = color

# Activation des leds du serpent
def addSnake(snake, leds):
    addElement(snake, leds, Color(0, 255, 0))

# Désactivation des leds du serpent
def removeSnake(snake, leds):
    for (x, y) in snake:
        leds[x + y * 8] = Color(0, 0, 0)

# Calcul des nouvelles coordonnées du serpent
# pour un déplacement vers le haut
def snakeUp(snake):
    snake.pop()
    newLed_x, newLed_y = snake[0]
    if newLed_y == 0:
        newLed_y = 7
    else:
        newLed_y = newLed_y - 1
    snake.insert(0, (newLed_x, newLed_y))

# Calcul des nouvelles coordonnées du serpent
# pour un déplacement vers le bas
def snakeDown(snake):
    snake.pop()
    newLed_x, newLed_y = snake[0]
    if newLed_y == 7:
        newLed_y = 0
    else:
        newLed_y = newLed_y + 1
    snake.insert(0, (newLed_x, newLed_y))

# Calcul des nouvelles coordonnées du serpent
# pour un déplacement vers la droite
def snakeRight(snake):
    snake.pop()
    newLed_x, newLed_y = snake[0]
    if newLed_x == 7:
        newLed_x = 0
    else:
        newLed_x = newLed_x + 1
    snake.insert(0, (newLed_x, newLed_y))

# Calcul des nouvelles coordonnées du serpent
# pour un déplacement vers la gauche
def snakeLeft(snake):
    snake.pop()
    newLed_x, newLed_y = snake[0]
    if newLed_x == 0:
        newLed_x = 7
    else:
        newLed_x = newLed_x - 1
    snake.insert(0, (newLed_x, newLed_y))

# Validation d'un changement de direction
def changeDirection(direction, newDirection):
    unauthorized = [1, 0, 3, 2]
    if newDirection != unauthorized[direction]:
        return newDirection
    else:
        return direction

# Activation des leds de nourriture
def addFood(food, leds):
    addElement(food, leds, Color(255, 255, 0))

# Détecte si le serpent vient de manger
def detectFood(food, snakeHead):
    return snakeHead in food

# Supprime la nourriture digeree
def digestedFood(food, digest, snake):
    for aliment in digest:
        if aliment not in snake:
            digest.remove(aliment)
            snake.append(aliment)

# Mort du serpent : on fait clignoter les leds
def die(snake, leds, strip):
    for nb in range(5):
        for i in range(50):
            addElement(snake, leds, Color(0, 255 - i * 5, 5 + i * 5))
            displayScreen(strip, leds)
            time.sleep(0.01)
        for i in range(50):
            addElement(snake, leds, Color(0, 5 + i * 5, 255 - i * 5))
            displayScreen(strip, leds)
            time.sleep(0.01)

# Teste si le serpent se mord la queue
def isDead(snake):
    return snake[0] in snake[1:]

# Teste si le joueur a gagné
def isWinner(food, digest):
    return len(food) == 0 and len(digest) == 0

# Affichage d'un cadre
def displayBox(size, color, leds):
    for x in range(size, 8 - size):
        for y in range(size, 8 - size):
            leds[x + y * 8] = color

# Animation de victoire
def victory(leds, strip):
    clearScreen(leds)
    displayScreen(strip, leds)
    for nb in range(5):
        for size in range(4):
            displayBox(size, Color(255 - 40 * size, 50 * size, 0), leds)
            displayScreen(strip, leds)
            time.sleep(0.2)
        for size in range(4, 0, -1):
            displayBox(size, Color(0, 0, 0), leds)
            displayScreen(strip, leds)
            time.sleep(0.2)

# Initialisation de curses
def initCurses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.nodelay(1)
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
    # Position de la nourriture
    nourriture = [(1, 1), (5, 3), (6,7), (1, 6), (3, 4)]
    nourriture = [(1, 1)]
    # Elements en cours de digestion
    estomac = []
    # Initialisation des leds en noir
    leds = [Color(0, 0, 0)] * 64
    # Direction de départ
    direction = 0
    newDirection = direction

    # Création d'un élément permettant de "manipuler"
    # l'écran de leds
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, CHANNEL, STRIP_TYPE)

    # Initialisation de l'écran
    strip.begin()

    stdscr = initCurses()

    while True:
        # Ajout du serpent sur l'écran
        addSnake(serpent, leds)
        # Detecte si le serpent mange
        if detectFood(nourriture, serpent[0]):
            estomac.append(serpent[0])
            nourriture.remove(serpent[0])
        # Supprime la nourriture digérée
        digestedFood(nourriture, estomac, serpent)
        # Ajout de la nourriture
        addFood(nourriture, leds)
        # Affichage de l'écran
        displayScreen(strip, leds)
        # Attente de 0.1s
        time.sleep(0.1)
        # Teste si le serpent est mort
        if isDead(serpent):
            die(serpent, leds, strip)
            break
        # Teste si le joueur a gagné
        if isWinner(nourriture, estomac):
            victory(leds, strip)
            break
        # Effacement du serpent
        removeSnake(serpent, leds)
        deplacement = stdscr.getch()
        stdscr.refresh()
        if deplacement == curses.KEY_UP:
            newDirection = 0
        elif deplacement == curses.KEY_DOWN:
            newDirection = 1
        elif deplacement == curses.KEY_RIGHT:
            newDirection = 2
        elif deplacement == curses.KEY_LEFT:
            newDirection = 3
        elif deplacement == 27:
            closeCurses(stdscr)
            break
        direction = changeDirection(direction, newDirection)
        # Déplacement (en mémoire) du serpent
        if direction == 0:
            snakeUp(serpent)
        elif direction == 1:
            snakeDown(serpent)
        elif direction == 2:
            snakeRight(serpent)
        elif direction == 3:
            snakeLeft(serpent)

    # Effacement de l'écran
    clearScreen(leds)
    displayScreen(strip, leds)
