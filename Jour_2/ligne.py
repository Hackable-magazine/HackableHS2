"""
   Affichage d'une ligne rouge

   Auteur       : Tristan Colombo <tristan@gnulinuxmag.com>
   Création     : 26/01/2017
   Modification : 27/01/2017
"""

from neopixel import *
import _rpi_ws281x as ws
import time

# Variables de configuration de l'écran
LED_COUNT      = 64
LED_PIN        = 18
LED_FREQ_HZ    = 800000
LED_DMA        = 5
LED_BRIGHTNESS = 8
LED_INVERT     = False
CHANNEL        = 0
STRIP_TYPE     = ws.WS2811_STRIP_GRB

# Création d'un élément permettant de "manipuler"
# l'écran de leds
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, CHANNEL, STRIP_TYPE)

# Initialisation de l'écran
strip.begin()

leds = [Color(0, 0, 0)] * 64
for i in range(8):
    leds[i] = Color(255, 0, 0)

# Affichage de l'écran
for i in range(64):
    strip.setPixelColor(i, leds[i])
strip.show()

# Attente de 10s
time.sleep(10)

for i in range(8):
    leds[i] = Color(0, 0, 0)

# Affichage de l'écran
for i in range(64):
    strip.setPixelColor(i, leds[i])
strip.show()
