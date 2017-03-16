from neopixel import *
import _rpi_ws281x as ws
import time
import curses
import os

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

# Détecte si le serpent rentre en collision avec un élément
def detectCollision(elt, snakeHead):
    return snakeHead in elt

# Supprime la nourriture digeree
def digestedFood(food, digest, snake):
    for aliment in digest:
        if aliment not in snake:
            digest.remove(aliment)
            snake.append(aliment)

# Activation des leds des murs
def addWall(wall, leds):
    addElement(wall, leds, Color(255, 0, 0))

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

# Lecture d'un niveau et conversion des éléments du jeu
# en coordonnées
def readLevel(filename):
    snake = []
    food = []
    walls = []
    try:
        with open(filename, 'r') as fic:
            level = fic.readlines()
    except:
        exit(1)

    for y in range(8):
        for x, symbol in enumerate(level[y]):
            if symbol == 'X':
                snake.append((x, y))
            elif symbol == '*':
                walls.append((x, y))
            elif symbol == 'O':
                food.append((x, y))

    return (snake, food, walls)
 
# Animation de début de niveau
def newLevelAnimation(leds):
    for y in range(8):
        for x in range(8): 
            leds[x + y * 8] = Color(0, 0, 255)
        displayScreen(strip, leds)
        time.sleep(0.2)
        for x in range(8): 
            leds[x + y * 8] = Color(0, 0, 0)

# Affichage et jeu sur un niveau
def play(snake, food, walls, leds, strip, stdscr):
    # Elements en cours de digestion
    digest = []
    # Direction de départ
    direction = 0
    newDirection = direction

    # Animation de début de niveau
    newLevelAnimation(leds)

    while True:
        # Ajout du serpent sur l'écran
        addSnake(snake, leds)
        # Detecte si le serpent mange
        if detectCollision(food, snake[0]):
            digest.append(snake[0])
            food.remove(snake[0])
        # Supprime la nourriture digérée
        digestedFood(food, digest, snake)
        # Ajout de la nourriture
        addFood(food, leds)
        # Détecte si le serpent rencontre un mur
        if detectCollision(walls, snake[0]):
            die(snake, leds, strip)
            return False
        # Ajout des murs
        addWall(walls, leds)
        # Affichage de l'écran
        displayScreen(strip, leds)
        # Attente de 0.1s
        time.sleep(0.1)
        # Teste si le serpent est mort
        if isDead(serpent):
            die(snake, leds, strip)
            return False
        # Teste si le joueur a gagné
        if isWinner(food, digest):
            return True
        # Effacement du serpent
        removeSnake(snake, leds)
        move = stdscr.getch()
        stdscr.refresh()
        if move == curses.KEY_UP:
            newDirection = 0
        elif move == curses.KEY_DOWN:
            newDirection = 1
        elif move == curses.KEY_RIGHT:
            newDirection = 2
        elif move == curses.KEY_LEFT:
            newDirection = 3
        elif move == 27:
            closeCurses(stdscr)
            return False
        direction = changeDirection(direction, newDirection)
        # Déplacement (en mémoire) du serpent
        if direction == 0:
            snakeUp(snake)
        elif direction == 1:
            snakeDown(snake)
        elif direction == 2:
            snakeRight(snake)
        elif direction == 3:
            snakeLeft(snake)
           
    
if __name__ == '__main__':
    # Création d'un élément permettant de "manipuler"
    # l'écran de leds
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, CHANNEL, STRIP_TYPE)

    # Initialisation de l'écran
    strip.begin()

    stdscr = initCurses()

    # Initialisation des leds en noir
    leds = [Color(0, 0, 0)] * 64

    # Parcourt de tous les niveaux
    listeFichiers = os.listdir('levels')
    for fichier in listeFichiers:
         if fichier.endswith('.txt'):
             # Lecture des données du niveau
             serpent, nourriture, murs = readLevel('levels/' + fichier)
             # Lancement du niveau
             continuerJeu = play(serpent, nourriture, murs, leds, strip, stdscr)
             # Si le joueur a perdu ou choisi d'arrêter, on stoppe le jeu
             if not continuerJeu:
                 break

    # Animation de victoire
    if continuerJeu:
        victory(leds, strip)
             
    # Effacement de l'écran
    clearScreen(leds)
    displayScreen(strip, leds)

    # Fermeture de curses
    closeCurses(stdscr)
