import pyglet
from pyglet import gl
from pyglet.window import key
from math import sin, pi
from random import randint
import csv

status = 0
old_status = 0
# 0 - hlavní menu
# 1 - mapa 1
# 2 - mapa 2
# 3 - mapa 3
# 4 - animace po smrti hráče
# 5 - game over obrazovka
# 6 - pauza hry

# okno
WIDTH = 760
HEIGHT = 800

# zvukové efekty
eating_sound = pyglet.resource.media("eating.mp3", streaming=False)
powerup_sound = pyglet.resource.media("powerup.mp3", streaming=False)
death_sound = pyglet.resource.media("death.mp3", streaming=False)
port_sound = pyglet.resource.media("port.mp3", streaming=False)
victory_sound = pyglet.resource.media("victory.mp3", streaming=False)
play_once = 0  # proměnná pro přehrání zvuku pouze 1krát
sound = 1  # 1 - zapnutý zvuk, 0 - vypnutý zvuk

# pacman
PACMAN_SPEED = 4  # základní rychlost Pac-Mana
time_left = 0  # proměnná pro časovou pauzu po hře
additional_time = 0  # proměnná pro časovou pauzu po hře
PACMAN_DIRECTION = 0  # směr Pac-Mana
MOUTH = 0  # Pohyb Pac-Manových úst
MOUTH_DIRECTION = 1  # Směr Pac-Manových úst
pacman_soul = [0, 0]  # pozice mrtvé duše Pac-mana

# duch
GHOST_SPEED = 4  # rychlost duchů

# oči duchů
EYES = 0
c = 0  # koeficient pro hýbání očí duchů

# tečky v bludišti
COLOR = 0
k = 0  # koeficient pro změnu barvy (viditelnosti) teček

max_score = 0  # maximální možné skóre
score = 0  # skóre hráče
game_time = 0  # tisíciny sekundy
game_time_sec = 0  # sekundy
game_time_min = 0  # minuty

pressed_keys = []  # type: list
# předpřipravený seznam pro stisknuté klávesy hráčem

# Kódy políček
# -2 - portál
# -1 - power-up
# 0 - prázdné políčko
# 1 - políčko s bodem
# 2 - svislá čára
# 3 - vodorovná čára
# 4 - poloviční čára shora
# 5 - poloviční čára zdola
# 6 - poloviční čára zleva
# 7 - poloviční čára zprava
# 8 - tvar T shora
# 9 - tvar T spoda
# 10 - tvar T zleva
# 11 - tvar T zprava
# 12 - levý dolní roh
# 13 - pravý dolní roh
# 14 - levý horní roh
# 15 - pravý horní roh
# 16 - křížení svislé a vodorovné čáry

batch = pyglet.graphics.Batch()


def main_menu():  # hlavní menu při spuštění hry
    global status, pressed_keys
    window.clear()
    image = pyglet.image.load("main_menu.png")
    mainmenu = pyglet.sprite.Sprite(image)
    mainmenu.draw()

    if "map1" in pressed_keys:  # pokud hráč zvolil mapu č. 1
        status = 1
        set_map()
    elif "map2" in pressed_keys:  # pokud hráč zvolil mapu č. 2
        status = 2
        set_map()
    elif "map3" in pressed_keys:  # pokud hráč zvolil mapu č. 3
        status = 3
        set_map()


def set_map():  # nastaví proměnné pro zadanou mapu
    global maze, position_pacman, ENEMIES, ghost_position_x, ghost_position_y
    global ghost_direction, score, max_score, PACMAN_DIRECTION, MOUTH_DIRECTION
    global game_time, game_time_sec, game_time_min, play_once, PACMAN_SPEED
    maze = []  # předpřipravené pole pro dvojrozměrné bludiště
    maze_row = []  # seznam pro načítání jednotlivých řádků ze souborů s herními mapami
    score = 0
    max_score = 0
    game_time = 0
    game_time_sec = 0
    game_time_min = 0
    play_once = 0
    PACMAN_SPEED = 4
    if status == 1:  # pokud hráč vybral mapu 1
        with open("maze1.csv") as f:  # načtení bludiště ze souboru
            reader = csv.reader(f)
            for row in reader:  # pro každý řádek
                for element in row:  # pro každé políčko v daném řádku
                    maze_row.append(int(element))
                maze.append(list(maze_row))
                maze_row.clear()

        # nastavení výchozích pozic a směrů postav
        position_pacman = [360, 40]
        ENEMIES = 1  # začínající počet duchů
        ghost_position_x = [360, 360, 360, 360, 360, 360]  # x-ová pozice každého ducha
        ghost_position_y = [360, 360, 360, 360, 360, 360]  # y-ová pozice každého ducha
        ghost_direction = [1, 3, 1, 3, 1, 3]  # počáteční směr každého ducha
        PACMAN_DIRECTION = 0  # počáteční směr Pac-Mana
        MOUTH_DIRECTION = 1  # počáteční směr Pac-manových úst
    elif status == 2:  # pokud hráč vybral mapu 2
        with open("maze2.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                for element in row:
                    maze_row.append(int(element))
                maze.append(list(maze_row))
                maze_row.clear()

        position_pacman = [360, 360]
        ENEMIES = 2
        ghost_position_x = [200, 520, 480, 240, 480]
        ghost_position_y = [440, 440, 440, 440, 440]
        ghost_direction = [3, 1, 3, 1, 1]
        PACMAN_DIRECTION = 0
        MOUTH_DIRECTION = 1
    elif status == 3:  # pokud hráč vybral mapu 3
        with open("maze3.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                for element in row:
                    maze_row.append(int(element))
                maze.append(list(maze_row))
                maze_row.clear()

        position_pacman = [360, 200]
        ENEMIES = 3
        ghost_position_x = [320, 360, 400, 320, 360, 400]
        ghost_position_y = [40, 680, 40, 680, 40, 680]
        ghost_direction = [1, 2, 3, 1, 4, 3]
        PACMAN_DIRECTION = 0
        MOUTH_DIRECTION = 1

    for y in range(len(maze)):  # pro každý seznam v dvourozměrném poli mapy
        for x in range(len(maze[y])):  # pro každé políčko v tomto seznamu
            if maze[y][x] != 1:  # pokud toto políčko neobsahuje tečku, nic neděláme
                continue
            else:  # pokud je na políčku tečka, zvýšíme maximální možné skóre
                max_score += 10


def draw_outline(x1, y1, x2, y2):  # vykreslí stěny
    gl.glBegin(gl.GL_QUADS)
    gl.glColor3ub(255, 0, 102)
    gl.glVertex2f(x1, y1)
    gl.glVertex2f(x1, y2)
    gl.glVertex2f(x2, y2)
    gl.glVertex2f(x2, y1)
    gl.glEnd()


def draw_rectangle(x1, y1, x2, y2):  # vykreslí výplň stěn
    gl.glBegin(gl.GL_QUADS)
    gl.glColor3ub(102, 0, 51)
    gl.glVertex2f(x1, y1)
    gl.glVertex2f(x1, y2)
    gl.glVertex2f(x2, y2)
    gl.glVertex2f(x2, y1)
    gl.glEnd()


def draw_background(x1, y1, x2, y2):  # vykreslí pozadí hry
    gl.glBegin(gl.GL_QUADS)
    gl.glColor3ub(0, 0, 40)
    gl.glVertex2f(x1, y1)
    gl.glVertex2f(x1, y2)
    gl.glVertex2f(x2, y2)
    gl.glVertex2f(x2, y1)
    gl.glEnd()


def draw_points(x1, y1, x2, y2, x3, y3, x4, y4):  # vykreslí tečky
    global k
    gl.glBegin(gl.GL_TRIANGLE_FAN)
    gl.glColor3ub(0 + int(102 * k), 77 + int(142 * k), 102 + int(153 * k))
    # pomocí koeficientu k měníme barvu (viditelnost) teček
    gl.glVertex2f(x1, y1)
    gl.glVertex2f(x2, y2)
    gl.glVertex2f(x3, y3)
    gl.glVertex2f(x4, y4)
    gl.glEnd()


def draw_powerup(x, y):  # nakreslí power-up
    square = pyglet.shapes.Rectangle(
        x * 40 + 20, y * 40 + 20, 16, 16, color=(255, 170, 100)
    )

    # ukotvený bod, okolo kterého se bude powerup otáčet
    square.anchor_x = 8
    square.anchor_y = 8

    square.rotation = 57 * COLOR  # rotace power-upů využitím proměnné
    # pro blikání teček
    square.draw()


def draw_portal(x, y, radius, r, g, b):  # nakreslí portál
    portal = pyglet.shapes.Circle(
        x * 40 + 20, y * 40 + 20, radius, segments=6, color=(r, g, b)
    )
    portal.draw()


def draw_pacman():  # nakreslí pacmana včetně pohybu úst
    global PACMAN_DIRECTION, MOUTH, MOUTH_DIRECTION
    if PACMAN_DIRECTION > 0:
        MOUTH_DIRECTION = PACMAN_DIRECTION
    pacman = pyglet.shapes.Circle(
        position_pacman[0] + 20,
        position_pacman[1] + 20,
        16,
        color=(255, 255, 1),
        batch=batch,
    )
    pacman.draw()

    if status != 6:  # pokud není pozastavená hra, ústa se hýbou
        MOUTH += 0.25
        if MOUTH > pi:  # pokud je větší než π, resetuje se na 0
            # zajistí tak plynulé otevírání a zavírání úst pomocí funkce sinus níže
            MOUTH = 0

    # otevírání a zavírání úst podle směru Pac-Mana
    if status != 4:  # pokud hráč nezemřel, ústa se hýbou
        n = sin(MOUTH)  # koeficientem k  a funkcí sinus se násobí souřadnice
        # Pac-manových úst --> zavírání a otevírání úst
        x1, y1 = position_pacman[0] + 20, position_pacman[1] + 20
        x2, y2, x3, y3 = 1, 1, 1, 1
        if MOUTH_DIRECTION == 1:  # pokud jsou ústa nasměrována doprava
            x2 = position_pacman[0] + 36
            x3 = position_pacman[0] + 36
            y = position_pacman[1] + 20
            y2, y3 = y - 20 * n, y + 20 * n
        if MOUTH_DIRECTION == 2:  # dolů
            x = position_pacman[0] + 20
            x2 = x - 20 * n
            x3 = x + 20 * n
            y2 = position_pacman[1] + 36
            y3 = position_pacman[1] + 36
        if MOUTH_DIRECTION == 3:  # doleva
            x2 = position_pacman[0] + 4
            x3 = position_pacman[0] + 4
            y = position_pacman[1] + 20
            y2, y3 = y - 20 * n, y + 20 * n
        if MOUTH_DIRECTION == 4:  # nahoru
            x = position_pacman[0] + 20
            x2 = x - 20 * n
            x3 = x + 20 * n
            y2 = position_pacman[1] + 4
            y3 = position_pacman[1] + 4

        # vykreslení úst
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glColor3ub(0, 0, 40)
        gl.glVertex2f(x1, y1)
        gl.glVertex2f(x2, y2)
        gl.glVertex2f(x3, y3)
        gl.glEnd()

    if status == 4:  # pokud hráč umřel
        dead_eye1 = pyglet.shapes.Rectangle(
            position_pacman[0] + 13,
            position_pacman[1] + 24,
            4,
            4,
            color=(1, 1, 1),
        )
        dead_eye1.rotation = 45
        dead_eye1.draw()

        dead_eye2 = pyglet.shapes.Rectangle(
            position_pacman[0] + 26,
            position_pacman[1] + 24,
            4,
            4,
            color=(1, 1, 1),
        )
        dead_eye2.rotation = 45
        dead_eye2.draw()


def draw_ghost(x, y, ghost):  # nakreslí příšerku s barvou podle argumentu ghost
    global EYES, c
    if ghost == 0:
        r = 255
        g = 1
        b = 1
    if ghost == 1:
        r = 1
        g = 255
        b = 1
    if ghost == 2:
        r = 1
        g = 1
        b = 255
    if ghost == 3:
        r = 255
        g = 1
        b = 255
    if ghost == 4:
        r = 255
        g = 1
        b = 125
    if ghost == 5:
        r = 0
        g = 205
        b = 205

    color = (r, g, b)

    ghost = pyglet.shapes.Circle(x + 20, y + 24, 15, color=color, batch=batch)
    ghost.draw()

    gl.glBegin(gl.GL_POLYGON)
    gl.glColor3ub(r, g, b)
    gl.glVertex2f(x + 20, y + 30)
    gl.glVertex2f(x + 35, y + 25)
    gl.glVertex2f(x + 35, y + 4)
    gl.glVertex2f(x + 27.5, y + 11.5)
    gl.glVertex2f(x + 20, y + 4)
    gl.glVertex2f(x + 12.5, y + 11.5)
    gl.glVertex2f(x + 5, y + 4)
    gl.glVertex2f(x + 5, y + 25)
    gl.glEnd()

    c = sin(EYES)  # pohyb očí opět pomocí funkce sinus

    # pomocí koeficientu c se mění x-ová souřadnice očí - pohyb ze strany na stranu
    eye1 = pyglet.shapes.Circle(
        (x + 13) + c * 4, y + 24, 6.5, segments=15, color=(255, 255, 255), batch=batch
    )  # levé oko
    eye2 = pyglet.shapes.Circle(
        (x + 27) + c * 4, y + 24, 6.5, segments=15, color=(255, 255, 255), batch=batch
    )  # pravé oko

    pupil1 = pyglet.shapes.Circle(
        (x + 13) + c * 8, y + 24, 3, segments=10, color=(1, 1, 1), batch=batch
    )  # levá zornička

    pupil2 = pyglet.shapes.Circle(
        (x + 27) + c * 8, y + 24, 3, segments=10, color=(1, 1, 1), batch=batch
    )  # pravá zornička

    eye1.draw()
    eye2.draw()
    pupil1.draw()
    pupil2.draw()


def death():  # vykreslí mrtvé tělo Pacmana
    global pacman_soul, time_left, status
    soul = pyglet.shapes.Circle(
        pacman_soul[0],
        pacman_soul[1],
        16,
        color=(255, 255, 255),
        batch=batch,
    )  # bílá duše Pac-Mana
    if time_left >= 1:
        # duše je vidět do 1 sekundy před přepnutím na výslednou obrazovku
        soul.opacity = (time_left - 1) * 80  # duše je postupně méně viditelná
    else:  # duše zmizí 1 sekundu před přepnutím na výslednou obrazovku
        soul.opacity = 0

    soul.draw()

    dead_eye1 = pyglet.shapes.Rectangle(
        pacman_soul[0] - 7,
        pacman_soul[1] + 4,
        4,
        4,
        color=(1, 1, 1),
    )  # levé mrtvé oko duše Pac-Mana
    dead_eye1.rotation = 45
    if time_left >= 1:  # oko je vidět do 1 sekundy
        # před přepnutím na výslednou obrazovku
        dead_eye1.opacity = (time_left - 1) * 80  # oko je postupně méně viditelné
    else:  # oko zmizí 1 sekundu před přepnutím na výslednou obrazovku
        dead_eye1.opacity = 0  # oko zmizí
    dead_eye1.draw()

    # pravé mrtvé oko duše Pac-Mana
    dead_eye2 = pyglet.shapes.Rectangle(
        pacman_soul[0] + 6,
        pacman_soul[1] + 4,
        4,
        4,
        color=(1, 1, 1),
    )  # mrtvé oko duše Pac-Mana
    dead_eye2.rotation = 45
    if time_left >= 1:  # oko je vidět do 1 sekundy
        # před přepnutím na výslednou obrazovku
        dead_eye2.opacity = (time_left - 1) * 80  # oko je postupně méně viditelné
    else:  # oko zmizí 1 sekundu před přepnutím na výslednou obrazovku
        dead_eye2.opacity = 0  # oko zmizí
    dead_eye2.draw()


def reverse(direction):  # funkce vracející opačný směr pohybu
    if direction == 1:  # pokud je směr vpravo, dostaneme směr vlevo
        return 3
    elif direction == 2:
        return 4
    elif direction == 3:
        return 1
    elif direction == 4:
        return 2


def pause():  # zastavení hry, vykreslení informačního textu
    global k
    text1 = pyglet.text.Label(
        text="PAUSED",
        font_name="Arial Rounded MT Bold",
        font_size=80,
        color=(255, 255, 255, int(255 * k)),
        x=150,
        y=350,
    )
    text1.draw()
    text2 = pyglet.text.Label(
        text="PRESS P TO CONTINUE PLAYING",
        font_name="Arial Rounded MT Bold",
        font_size=10,
        color=(255, 173, 148, 255),
        x=520,
        y=777,
    )
    text2.draw()
    text3 = pyglet.text.Label(
        text="PRESS E TO RETURN TO MENU",
        font_name="Arial Rounded MT Bold",
        font_size=10,
        color=(255, 173, 148, 255),
        x=520,
        y=757,
    )
    text3.draw()


def gameover():  # obrazovka po konci hry
    global status, old_status, pressed_keys, score
    global game_time_sec, game_time_min

    if status == 5:  # pokud je hráč na výsledné obrazovce
        show_score = pyglet.text.Label(
            text=f"{score}",
            font_name="Bodoni MT Black",
            font_size=28,
            anchor_x="center",
            anchor_y="center",
            x=220,
            y=537,
        )  # vykreslení skóre hráče
        show_score.color = (255, 255, 0, 255)

        show_time_low = pyglet.text.Label(
            text=f"{game_time_min}:0{game_time_sec}",
            font_name="Bodoni MT Black",
            font_size=28,
            anchor_x="center",
            anchor_y="center",
            x=540,
            y=537,
        )  # text s časem hráče v případě, že sekundy jsou jednociferné

        show_time_high = pyglet.text.Label(
            text=f"{game_time_min}:{game_time_sec}",
            font_name="Bodoni MT Black",
            font_size=28,
            anchor_x="center",
            anchor_y="center",
            x=540,
            y=537,
        )  # text s časem hráče v případě, že sekundy jsou dvojciferné

        show_time_low.color = show_time_high.color = (0, 255, 98, 255)

        if score == max_score:  # vykreslení obrazovky, pokud hráč vyhrál
            victory = pyglet.image.load("victory_screen.png")
            victory = pyglet.sprite.Sprite(victory)
            victory.draw()
            show_score.draw()
            if game_time_sec < 10:  # pokud jsou sekundy jednociferné
                show_time_low.draw()
            else:  # pokud jsou sekundy dvojciferné
                show_time_high.draw()
        else:  # vykreslení obrazovky, pokud hráč prohrál
            defeat = pyglet.image.load("defeat_screen.png")
            defeat = pyglet.sprite.Sprite(defeat)
            defeat.draw()
            show_score.draw()
            if game_time_sec < 10:  # vykreslení času, pokud jsou sekundy jednociferné
                show_time_low.draw()
            else:  # vykreslení času, pokud jsou sekundy dvojciferné
                show_time_high.draw()

        if "enter" in pressed_keys:  # hráč chce hrát mapu znovu
            if score != max_score:
                pressed_keys.clear()
                status = old_status
                old_status = 0
                set_map()
            else:  # hráč se chce vrátit do hlavní nabídky
                pressed_keys.clear()
                old_status = 0
                status = 0

        elif "anykey" in pressed_keys:  # hráč se chce vrátit do hlavní nabídky
            pressed_keys.clear()
            old_status = 0
            status = 0


def key_press(symbol, modificators):  # registruje stisk klávesy
    global status
    if status != 6:
        if symbol == key.UP:
            pressed_keys.clear()
            pressed_keys.append("nahoru")
        if symbol == key.DOWN:
            pressed_keys.clear()
            pressed_keys.append("dolu")
        if symbol == key.RIGHT:
            pressed_keys.clear()
            pressed_keys.append("doprava")
        if symbol == key.LEFT:
            pressed_keys.clear()
            pressed_keys.append("doleva")
        if symbol == key.NUM_1:
            pressed_keys.clear()
            pressed_keys.append("map1")
        if symbol == key.NUM_2:
            pressed_keys.clear()
            pressed_keys.append("map2")
        if symbol == key.NUM_3:
            pressed_keys.clear()
            pressed_keys.append("map3")
    if symbol == key.P:
        pressed_keys.append("P")
    if symbol == key.E:
        if status == 0 or status == 5 or status == 6:
            pressed_keys.clear()
            pressed_keys.append("E")
    if symbol == key.S:
        pressed_keys.append("S")
    if status == 5:
        if symbol == key.ENTER:
            pressed_keys.clear()
            pressed_keys.append("enter")
        elif key.KeyStateHandler:
            pressed_keys.clear()
            pressed_keys.append("anykey")


def draw_text(text, x, y, font_name, font_size, color):  # vykreslí zadaný text
    text = pyglet.text.Label(
        text=text, x=x, y=y, font_name=font_name, font_size=font_size, color=color
    )
    text.draw()


def refresh(time):  # aktualizace pozic, směru pohybu, skóre
    global PACMAN_DIRECTION, EYES, c, COLOR, k
    global ghost_direction, ghost_position_x, ghost_position_y
    global status, old_status, PACMAN_SPEED, time_left, pacman_soul, score
    global max_score, additional_time, ENEMIES, eating_sound, death_sound, victory_sound
    global port_sound, play_once, game_time, game_time_sec, game_time_min, sound

    COLOR += 0.05
    if COLOR > pi:  # pokud je větší než π, resetuje se na 0
        # to zajistí plynulé blikání teček pomocí funkce sinus níže
        COLOR = 0
    k = sin(COLOR)  # koeficientem k se pak násobí barva (viditelnost) teček
    # způsobuje tak jejich blikání

    if "S" in pressed_keys:  # zapnutí / vypnutí zvuku ve hře
        pressed_keys.remove("S")
        if status == 1 or status == 2 or status == 3:  # pouze pokud je hráč ve hře
            if sound == 1:  # pokud je zaplý zvuk
                sound = 0  # zvuk se vypne
            elif sound == 0:  # pokud je vyplý zvuk
                sound = 1  # zvuk se zapne

    if status == 1:  # přidávání příšerek podle skóre hráče
        if ENEMIES == 1:
            if score > 1 / 4 * max_score:
                ENEMIES = 2
        if ENEMIES == 2:
            if score > 1 / 2 * max_score:
                ENEMIES = 3
        if ENEMIES == 3:
            if score > 3 / 4 * max_score:
                ENEMIES = 4
    if status == 2:
        if ENEMIES == 2:
            if score > 1 / 4 * max_score:
                ENEMIES = 3
        if ENEMIES == 3:
            if score > 2 / 3 * max_score:
                ENEMIES = 4
    if status == 3:
        if ENEMIES == 3:
            if score > 1 / 3 * max_score:
                ENEMIES = 4
        if ENEMIES == 4:
            if score > 4 / 5 * max_score:
                ENEMIES = 5

    if status == 1 or status == 2 or status == 3:
        old_status = status
        if "P" in pressed_keys:  # pauznutí hry pouze pokud je hráč ve hře
            if score != max_score:
                if status != 6:
                    old_status = status  # old_status si pamatuje, kterou mapu hráč
                    # hraje. Pokud hráč opět spustí hru, status se nastaví na old_status
                status = 6
            pressed_keys.remove("P")

        if score != max_score:  # pokud hráč ještě nevyhrál, počítá se čas
            game_time += 0.025  # game_time značí tisíciny sekundy a
            # tuto hodnotu volíme, protože hra se obnovuje 40x/s
            if game_time // 1 == 1:  # pokud uběhla sekunda
                game_time = 0
                game_time_sec += 1
            if game_time_sec // 60 == 1:  # pokud uběhla minuta
                game_time_sec = 0
                game_time_min += 1

    if status == 1 or status == 2 or status == 3 or status == 4:
        if score == max_score:  # nastavení krátkého čekacího času po výhře
            if additional_time == 0:  # zabráníme neustálému nastavování času
                additional_time = 1
                time_left = 2  # nastavení času
            if time_left <= 0:  # pokud uběhl čas, hra přepne se na výslednou obrazovku
                status = 5
                additional_time = 0
            else:  # pokud neuběhl, čas zkracujeme
                time_left -= 0.025
            if sound == 1:  # pokud je zaplý zvuk
                if play_once == 0:  # zabráníme tím, aby se zvuk přehrál několikrát
                    victory_sound.play()
                    play_once = 1

        else:
            x = position_pacman[0] // 40  # pozice x v dvojrozměrném poli mapy
            y = position_pacman[1] // 40  # pozice y v dvojrozměrném poli mapy

            if (
                (position_pacman[0] % 40 == 0)
                and (position_pacman[1] % 40 == 0)
                and (maze[y][x] == -2)
            ):  # hráč vejde do portálu
                if sound == 1:
                    port_sound.play()
                if PACMAN_DIRECTION == 1:  # Port do levého portálu
                    position_pacman[0] = 48
                    position_pacman[1] = 360
                elif PACMAN_DIRECTION == 3:  # Port do pravého portálu
                    position_pacman[0] = 672
                    position_pacman[1] = 360

            if (
                (position_pacman[0] % 40 == 0)
                and (position_pacman[1] % 40 == 0)
                and (maze[y][x] == 1)
            ):  # hráč sní tečku -> přičtení skóre, přehrání zvuku
                maze[y][x] = 0
                score += 10
                if sound == 1:
                    eating_sound.play()
            if (
                (position_pacman[0] % 40 == 0)
                and (position_pacman[1] % 40 == 0)
                and (maze[y][x] == -1)
            ):  # hráč sní power-up -> nastavení efektu, přehrání zvuku
                maze[y][x] = 0  # smazání tečky z daného políčka (dlaždice)
                if sound == 1:
                    powerup_sound.play()

                time_left = 3  # nastavení délky trvání efektu
                effect = randint(1, 3)
                if effect == 2:  # efekt zpomalení
                    PACMAN_SPEED = 2
                else:  # efekt zrychlení
                    PACMAN_SPEED = 8

            if time_left > 0:  # kontrola, zda už efekt vypršel
                time_left -= 0.025
            if time_left <= 0:  # pokud ano, zrušíme efekt
                if (position_pacman[0] % 40 == 0) and (position_pacman[1] % 40 == 0):
                    PACMAN_SPEED = 4

            if (
                status == 1 or status == 2 or status == 3
            ):  # ověření možnosti změny směru a následná změna směru
                if "doprava" in pressed_keys:  # pokud jde hráč doprava
                    if position_pacman[1] % 40 == 0 and maze[y][x + 1] < 2:
                        # pokud napravo od Pac-Mana není stěna, změní se Pac-Manův směr
                        PACMAN_DIRECTION = 1
                elif "nahoru" in pressed_keys:
                    if position_pacman[0] % 40 == 0 and maze[y + 1][x] < 2:
                        PACMAN_DIRECTION = 2
                elif "doleva" in pressed_keys:
                    if position_pacman[1] % 40 == 0 and maze[y][x - 1] < 2:
                        PACMAN_DIRECTION = 3
                elif "dolu" in pressed_keys:
                    if position_pacman[0] % 40 == 0 and maze[y - 1][x] < 2:
                        PACMAN_DIRECTION = 4

                # pohyb Pac-Mana
                if PACMAN_DIRECTION == 1:  # pokud jde směrem doprava
                    if maze[y][x + 1] > 1:  # pokud je napravo od Pac-Mana stěna,
                        # Pac-Man se zastaví
                        PACMAN_DIRECTION = 0
                    else:
                        position_pacman[0] += PACMAN_SPEED
                if PACMAN_DIRECTION == 2:  # pokud jde směrem nahoru
                    if maze[y + 1][x] > 1:
                        PACMAN_DIRECTION = 0
                    else:
                        position_pacman[1] += PACMAN_SPEED
                if PACMAN_DIRECTION == 3:  # pokud jde směrem vlevo
                    if position_pacman[0] % 40 == 0 and maze[y][x - 1] > 1:
                        PACMAN_DIRECTION = 0
                    else:
                        position_pacman[0] -= PACMAN_SPEED
                if PACMAN_DIRECTION == 4:  # pokud jde směrem dolů
                    if position_pacman[1] % 40 == 0 and maze[y - 1][x] > 1:
                        PACMAN_DIRECTION = 0
                    else:
                        position_pacman[1] -= PACMAN_SPEED
            else:
                PACMAN_DIRECTION = 0

            # Pohyb příšerek
            for myghost in range(
                0, ENEMIES
            ):  # myghost tu bude proměnná určující,
                # s kterou příšerkou zrovna pracujeme
                if (ghost_position_x[myghost] % 40 == 0) and (
                    ghost_position_y[myghost] % 40 == 0
                ):  # pokud je duch na středu políčka (dlaždice)
                    ghost_direction_list = []  # seznam dostupných směrů
                    direction_quantity = 0  # celkový počet dostupných směrů
                    a = ghost_position_x[myghost] // 40
                    # x-ová pozice ducha ve dvojrozměrném poli mapy
                    b = ghost_position_y[myghost] // 40
                    # y-ová pozice ducha ve dvojrozměrném poli mapy
                    if maze[b][a + 1] < 2:  # kontrola políčka nad duchem
                        ghost_direction_list.append(1)
                    if maze[b + 1][a] < 2:  # kontrola políčka vpravo od ducha
                        ghost_direction_list.append(2)
                    if maze[b][a - 1] < 2:  # kontrola políčka pod duchem
                        ghost_direction_list.append(3)
                    if maze[b - 1][a] < 2:  # kontrola políčka vlevo od ducha
                        ghost_direction_list.append(4)
                    direction_quantity = len(ghost_direction_list)
                    if direction_quantity == 1:
                        ghost_direction[myghost] = ghost_direction_list[0]
                    elif direction_quantity == 2 and (
                        (1 in ghost_direction_list and 3 in ghost_direction_list)
                        or (2 in ghost_direction_list and 4 in ghost_direction_list)
                    ):  # duch nebude měnit směr na každém políčku,
                        # ale jen na křižovatkách nebo v rozích
                        pass
                    elif (
                        direction_quantity == 2
                    ):  # duch bude měnit směr tak, aby se ve většině
                        # případů nevracel tam, odkud přišel
                        number = randint(1, 20)
                        if number == 1:  # obrátí se směr ducha na opačnou stranu
                            ghost_direction[myghost] = reverse(ghost_direction[myghost])
                        else:  # odstraní se opačný směr ducha
                            # a vybere se ten směr, který zůstal v seznamu
                            ghost_direction_list.remove(
                                reverse(ghost_direction[myghost])
                                )
                            ghost_direction[myghost] = ghost_direction_list[0]
                    else:  # odstraní se opačný směr ducha
                        # a vybere se jeden ze zbylých směrů
                        ghost_direction_list.remove(reverse(ghost_direction[myghost]))
                        number = randint(1, len(ghost_direction_list))
                        ghost_direction[myghost] = ghost_direction_list[number - 1]

                    if maze[b][a] == -2:  # pokud duch vejde do portálu
                        if ghost_direction[myghost] == 1:  # port do levého portálu
                            ghost_position_x[myghost] = 44
                            ghost_position_y[myghost] = 360
                        elif ghost_direction[myghost] == 3:  # port do pravého portálu
                            ghost_position_x[myghost] = 676
                            ghost_position_y[myghost] = 360

                # pohyb duchů podle jejich směru
                if ghost_direction[myghost] == 1:  # doprava
                    ghost_position_x[myghost] += GHOST_SPEED
                elif ghost_direction[myghost] == 2:  # dolů
                    ghost_position_y[myghost] += GHOST_SPEED
                elif ghost_direction[myghost] == 3:  # doleva
                    ghost_position_x[myghost] -= GHOST_SPEED
                elif ghost_direction[myghost] == 4:  # nahoru
                    ghost_position_y[myghost] -= GHOST_SPEED

                if (abs(ghost_position_x[myghost] - position_pacman[0]) < 20) and (
                    abs(ghost_position_y[myghost] - position_pacman[1]) < 20
                ):  # vzdálenost (hranice), která určí, jestli duch snědl Pac-Mana
                    status = 4
                    if sound == 1:
                        if play_once == 0:  # zabráníme tomu, aby se zvuk přehrál
                            # několikrát za sebou
                            death_sound.play()
                            play_once = 1

            # souřadnice pro hýbání očima ghostů
            EYES += 0.20
            if EYES > 2 * pi:  # zajistí plynulý pohyb očí ze strany na stranu
                EYES = 0
            c = sin(EYES)  # koeficientem c se násobí x-ová souřadnice očí

            if status == 4:  # nastavení čekacího času po smrti Pacmana
                if pacman_soul[1] == 0:  # pokud y-ová pozice duše Pac-Mana je 0
                    time_left = 3.5
                    pacman_soul[0] = position_pacman[0] + 20
                    # výchozí pozice x pro duši Pac-Mana
                    pacman_soul[1] = position_pacman[1] + 20
                    # výchozí pozice y pro duši Pac-Mana
                if time_left >= 1:  # duše bude stoupat, dokud nebude zbývat 1 sekunda
                    time_left -= 0.025
                    pacman_soul[1] += 1  # stoupání duše Pac-Mana
                elif time_left >= 0:  # jakmile zbývá 1 sekunda, duše už úplně zmizí
                    time_left -= 0.025  # zbylý čas ubýhá dál
                else:  # pozice duše se resetují a zobrazí se výsledná obrazovka
                    pacman_soul[0] = 0
                    pacman_soul[1] = 0
                    status = 5

    if "E" in pressed_keys:
        if status == 6:  # hráč se vrátí do hlavní nabídky
            pressed_keys.clear()
            status = 0
        elif status == 0:  # hráč ukončí program
            pyglet.app.exit()

    if status == 6:  # pokud je pozastavená hra
        if "P" in pressed_keys:  # zruší se pozastavení hry
            pressed_keys.remove("P")
            status = old_status
            old_status = 0


def render():  # vykreslení mapy a objektů
    global status, sound

    if status == 0:  # vykreslení hlavní nabídky
        main_menu()
    if (
        status == 1 or status == 2 or status == 3 or status == 4 or status == 6
    ):  # vykreslení mapy
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        draw_background(0, 0, WIDTH, HEIGHT)
        for y in range(len(maze)):  # pro každý řádek v seznamu
            for x in range(len(maze[y])):  # pro každé políčko v daném řádku
                # nyní se vykresluje každé políčko/dlaždice ve dvourozměrném poli mapy.
                # Každé políčko má svůj kód podle typu/tvaru objektu,
                # který je na dané dlaždici umístěň
                if maze[y][x] == -2:
                    draw_portal(x, y, 25, 255, 255, 255)
                    draw_portal(x, y, 23, 0, 0, 40)
                elif maze[y][x] == -1:
                    draw_powerup(x, y)
                elif maze[y][x] == 0:
                    pass
                elif maze[y][x] == 1:
                    draw_points(
                        20 + x * 40,
                        17 + y * 40,
                        23 + x * 40,
                        20 + y * 40,
                        20 + x * 40,
                        23 + y * 40,
                        17 + x * 40,
                        20 + y * 40,
                    )
                elif maze[y][x] == 2:
                    draw_outline(16 + x * 40, 0 + y * 40, 24 + x * 40, 40 + y * 40)
                    draw_rectangle(18 + x * 40, 0 + y * 40, 22 + x * 40, 40 + y * 40)
                elif maze[y][x] == 3:
                    draw_outline(0 + x * 40, 16 + y * 40, 40 + x * 40, 24 + y * 40)
                    draw_rectangle(0 + x * 40, 18 + y * 40, 40 + x * 40, 22 + y * 40)
                elif maze[y][x] == 4:
                    draw_outline(16 + x * 40, 18 + y * 40, 24 + x * 40, 40 + y * 40)
                    draw_rectangle(
                        18 + x * 40, 20 + y * 40, 22 + x * 40, 40 + y * 40
                    )
                elif maze[y][x] == 5:
                    draw_outline(16 + x * 40, 0 + y * 40, 24 + x * 40, 22 + y * 40)
                    draw_rectangle(18 + x * 40, 0 + y * 40, 22 + x * 40, 20 + y * 40)
                elif maze[y][x] == 6:
                    draw_outline(0 + x * 40, 16 + y * 40, 22 + x * 40, 24 + y * 40)
                    draw_rectangle(0 + x * 40, 18 + y * 40, 20 + x * 40, 22 + y * 40)
                elif maze[y][x] == 7:
                    draw_outline(18 + x * 40, 16 + y * 40, 40 + x * 40, 24 + y * 40)
                    draw_rectangle(
                        20 + x * 40, 18 + y * 40, 40 + x * 40, 22 + y * 40
                    )
                elif maze[y][x] == 8:
                    draw_outline(0 + x * 40, 16 + y * 40, 40 + x * 40, 24 + y * 40)
                    draw_outline(16 + x * 40, 0 + y * 40, 24 + x * 40, 22 + y * 40)
                    draw_rectangle(0 + x * 40, 18 + y * 40, 40 + 40 * x, 22 + 40 * y)
                    draw_rectangle(18 + x * 40, 0 + y * 40, 22 + x * 40, 20 + y * 40)
                elif maze[y][x] == 9:
                    draw_outline(0 + x * 40, 16 + y * 40, 40 + x * 40, 24 + y * 40)
                    draw_outline(16 + x * 40, 20 + y * 40, 24 + x * 40, 42 + y * 40)
                    draw_rectangle(0 + x * 40, 18 + y * 40, 40 + 40 * x, 22 + 40 * y)
                    draw_rectangle(
                        18 + x * 40, 20 + y * 40, 22 + x * 40, 40 + y * 40
                    )
                elif maze[y][x] == 10:
                    draw_outline(20 + x * 40, 16 + y * 40, 40 + x * 40, 24 + y * 40)
                    draw_outline(16 + x * 40, 0 + y * 40, 24 + x * 40, 40 + y * 40)
                    draw_rectangle(
                        20 + x * 40, 18 + y * 40, 40 + 40 * x, 22 + 40 * y
                    )
                    draw_rectangle(18 + x * 40, 0 + y * 40, 22 + x * 40, 40 + y * 40)
                elif maze[y][x] == 11:
                    draw_outline(0 + x * 40, 16 + y * 40, 20 + x * 40, 24 + y * 40)
                    draw_outline(16 + x * 40, 0 + y * 40, 24 + x * 40, 40 + y * 40)
                    draw_rectangle(0 + x * 40, 18 + y * 40, 20 + 40 * x, 22 + 40 * y)
                    draw_rectangle(18 + x * 40, 0 + y * 40, 22 + x * 40, 40 + y * 40)
                elif maze[y][x] == 12:
                    draw_outline(16 + x * 40, 18 + y * 40, 24 + x * 40, 40 + y * 40)
                    draw_outline(16 + x * 40, 16 + y * 40, 40 + x * 40, 24 + y * 40)
                    draw_rectangle(
                        18 + x * 40, 18 + y * 40, 22 + x * 40, 40 + y * 40
                    )
                    draw_rectangle(
                        20 + x * 40, 18 + y * 40, 40 + x * 40, 22 + y * 40
                    )
                elif maze[y][x] == 13:
                    draw_outline(16 + x * 40, 18 + y * 40, 24 + x * 40, 40 + y * 40)
                    draw_outline(0 + x * 40, 16 + y * 40, 24 + x * 40, 24 + y * 40)
                    draw_rectangle(
                        18 + x * 40, 18 + y * 40, 22 + x * 40, 40 + y * 40
                    )
                    draw_rectangle(0 + x * 40, 18 + y * 40, 20 + x * 40, 22 + y * 40)
                elif maze[y][x] == 14:
                    draw_outline(16 + x * 40, 0 + y * 40, 24 + x * 40, 22 + y * 40)
                    draw_outline(16 + x * 40, 16 + y * 40, 40 + x * 40, 24 + y * 40)
                    draw_rectangle(18 + x * 40, 0 + y * 40, 22 + x * 40, 22 + y * 40)
                    draw_rectangle(
                        20 + x * 40, 18 + y * 40, 40 + x * 40, 22 + y * 40
                    )
                elif maze[y][x] == 15:
                    draw_outline(16 + x * 40, 0 + y * 40, 24 + x * 40, 22 + y * 40)
                    draw_outline(0 + x * 40, 16 + y * 40, 24 + x * 40, 24 + y * 40)
                    draw_rectangle(18 + x * 40, 0 + y * 40, 22 + x * 40, 22 + y * 40)
                    draw_rectangle(0 + x * 40, 18 + y * 40, 20 + x * 40, 22 + y * 40)
                elif maze[y][x] == 16:
                    draw_outline(16 + x * 40, 0 + y * 40, 24 + x * 40, 18 + y * 40)
                    draw_outline(16 + x * 40, 22 + y * 40, 24 + x * 40, 40 + y * 40)
                    draw_outline(0 + x * 40, 16 + y * 40, 18 + x * 40, 24 + y * 40)
                    draw_outline(22 + x * 40, 16 + y * 40, 40 + x * 40, 24 + y * 40)
                    draw_rectangle(18 + x * 40, 0 + y * 40, 22 + x * 40, 40 + y * 40)
                    draw_rectangle(0 + x * 40, 18 + y * 40, 40 + 40 * x, 22 + 40 * y)
        draw_pacman()  # vykreslení Pac-Mana

        for myghost in range(0, ENEMIES):  # vykreslení každého ducha
            draw_ghost(ghost_position_x[myghost], ghost_position_y[myghost], myghost)

        draw_text(
            f"Score: {score}",
            25,
            HEIGHT - 40,
            font_name="Berlin Sans FB",
            font_size=25,
            color=(230, 255, 30, 255),
        )  # vykreslení skóre
        if game_time_sec < 10:  # vykreslení času s jednocifernými sekundami
            draw_text(
                f"Time: {game_time_min}:0{game_time_sec}",
                240,
                HEIGHT - 40,
                font_name="Berlin Sans FB",
                font_size=25,
                color=(0, 255, 98, 255),
            )
        else:  # vykreslení času s dvoucifernými sekundami
            draw_text(
                f"Time: {game_time_min}:{game_time_sec}",
                240,
                HEIGHT - 40,
                font_name="Berlin Sans FB",
                font_size=25,
                color=(0, 255, 98, 255),
            )

        if status == 1 or status == 2 or status == 3:  # pokud je hráč ve hře
            if score != max_score:  # vykreslení informačního textu
                draw_text(
                    "PRESS P TO PAUSE THE GAME",
                    520,
                    777,
                    font_name="Arial Rounded MT Bold",
                    font_size=10,
                    color=(255, 173, 148, 255),
                )
                if sound == 1:  # pokud je zapnutý zvuk
                    draw_text(
                        "PRESS S TO TURN OFF SOUND",
                        520,
                        757,
                        font_name="Arial Rounded MT Bold",
                        font_size=10,
                        color=(255, 173, 148, 255),
                    )
                elif sound == 0:  # pokud je vypnutý zvuk
                    draw_text(
                        "PRESS S TO TURN ON SOUND",
                        520,
                        757,
                        font_name="Arial Rounded MT Bold",
                        font_size=10,
                        color=(255, 173, 148, 255),
                    )

    if status == 4:  # pokud hráč umřel
        death()
    if status == 5:  # pokud je hráč ve výsledné obrazovce
        gameover()
    if status == 6:  # pokud je pozastavená hra
        pause()


window = pyglet.window.Window(width=WIDTH, height=HEIGHT)
window.push_handlers(on_draw=render, on_key_press=key_press)

pyglet.clock.schedule_interval(refresh, 1 / 40)

pyglet.app.run()
