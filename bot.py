from PIL import ImageGrab
from PIL.Image import Image
from py2d import Rect, Pixel
from pyevolution import Gentic_Evolution
from pynput.keyboard import Key, Controller as kctrl
from pynput.mouse import Button, Controller as mctrl
from time import sleep, time
import numpy as np
import pickle
import math
import os


def findwindow():
    screen: Image = ImageGrab.grab()

    for y in range(screen.height):
        for x in range(screen.width):
            pix: tuple = screen.getpixel((x, y))
            if (pix == (100, 205, 120)):
                foundgreen = False
                left = x
                top = y

                while (True):
                    x += 1
                    pix: tuple = screen.getpixel((x, y))

                    if (pix == (92, 195, 111)):
                        foundgreen = True

                    if (foundgreen and pix != (92, 195, 111)):
                        x -= 1
                        break

                while (screen.getpixel((x, y)) == (92, 195, 111)):
                    y += 1
                y -= 1

                width = x - left
                height = y - top

                return Rect(left, top, width, height)

    return Rect(0, 0, 0, 0)


# globals
gen = 1
genomas = 12
lastang = 0.5
data_filename = 'neurons.obj'

genetic = Gentic_Evolution(genomas)
if (os.path.exists(data_filename)):
    genetic.from_file(data_filename)

window = findwindow()
keyboard = kctrl()
mouse = mctrl()


def gamestate(frame: Image=None):
    if (frame is None):
        frame = ImageGrab.grab(window.getbox())

    x = int(window.width / 3)
    y = int(5 * window.height / 6)

    if (frame.getpixel((x, y)) == (212, 41, 89)):
        return 'score'

    x = int(window.width / 2)
    y = int(window.height * 0.1576)

    if (frame.getpixel((x, y)) == (255, 206, 48)):
        return 'ready'

    return 'ingame'


def calculate_angle(neycrp: Pixel):
    pixl = []

    for i in range(5):
        pix = neycrp.findpixel((255, 192, 42), i)

        if (pix is not None):
            pixl.append(pix)

        if (len(pixl) == 2):
            break

    if (len(pixl) != 2):
        return 0

    pixa, pixb = pixl

    diffx = pixa.x - pixb.x
    diffy = pixa.y - pixb.y

    arg = math.pi/2 if diffx == 0 else math.atan(diffy/diffx)
    return arg + math.pi/2


def normalize(v, vmax, vmin=0):
    v -= vmin
    vmax -= vmin
    return v / vmax


def presskey(key):
    keyboard.press(key)
    keyboard.release(key)


def loop(network):
    global lastang
    frame: Image = ImageGrab.grab(window.getbox())
    neycrp = Pixel(frame, (350, 770))

    if (gamestate(frame) == 'score'):
        return

    ang = calculate_angle(neycrp)
    ang = normalize(ang, math.pi)

    # can't find ney
    if (ang == 0):
        return

    w = ang - lastang
    w = normalize(w, 0.2, -0.2)

    output = network.forward([ang, w])[0]
    print('ang: {} | w: {} | out: {}'
          .format(round(ang, 2), round(w, 2), round(output, 2)))

    if (output > 0.55):
        presskey(Key.right)
    if (output < 0.45):
        presskey(Key.left)

    # sleep for 10ms (MemoryError fix)
    # sleep(0.01)
    # close image, may it releases the memory
    frame.close()

    lastang = ang
    loop(network)


def getparents(pop, scores):
    arr = np.array(scores)
    indexes = arr.argsort()[-2:][::-1]
    return pop[indexes[0]], pop[indexes[1]]


def main():
    global gen
    global lastang

    pop = genetic.population
    scores = []

    for i in range(genomas):
        print('Generation: {} | Genome: {}'.format(gen, i+1))
        network = pop[i]
        lastang = 0.5

        while (gamestate() != 'ready'):
            # print('Waiting for ready state')
            pass

        presskey(Key.space)

        pretime = time()
        loop(network)
        postime = time()

        scores.append(postime - pretime)

        while (gamestate() != 'score'):
            # print('Waiting for score state')
            pass

        mouse.click(Button.left)
        sleep(1)

    father, mother = getparents(pop, scores)
    genetic.renew_generation(father, mother)
    gen += 1

    with open(data_filename, 'wb') as filehandler:
        pickle.dump([gen, father, mother], filehandler)
        filehandler.close()

    main()


main()
