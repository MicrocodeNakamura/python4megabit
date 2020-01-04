#########################################
# File name: Tetris.py                  #
# Author: David Gurevich                #
# Course: ICS3U                         #
# Instructor: D. Mavrodin               #
# --------------------------------------#
# Last Modified: 11/12/2017 @ 21:02     #
#########################################

import sys
from random import randint, choice

from Classes import *

pygame.init()

HEIGHT = 600
WIDTH = 575
GRIDSIZE = HEIGHT // 24
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris - David Gurevich and microcode plus funny friends changed.")

LVL_1, LVL_2, LVL_3, LVL_4, LVL_5, LVL_6, LVL_7, LVL_8, LVL_9 = 30, 18, 16, 7, 5, 4, 3, 2, 1

LEVELS = [LVL_1, LVL_2, LVL_3, LVL_4, LVL_5, LVL_6, LVL_7, LVL_8, LVL_9, LVL_9]

SCORE = 0
HighSchore = 1000

# ---------------------------------------#

COLUMNS = 14
ROWS = 24
LEFT = 0
RIGHT = LEFT + COLUMNS
MIDDLE = LEFT + COLUMNS // 2
TOP = 1
FLOOR = TOP + ROWS

# -------------IMAGES and MUSIC--------------------#

pygame.mixer.set_num_channels(6)

# Channel 0: Background Music
# Channel 1: Block Rotation
# Channel 2: Force Hit
# Channel 3: Line Remove
# Channel 4: Slow Hit
# Channel 5: Tetris Remove


# ---- BACKGROUND IMAGES ---- #
tetris_img = pygame.image.load('images/Tetris.jpg')
grid_img = pygame.image.load('images/gridBG.jpg')

intro_screen = pygame.image.load('images/Intro.jpg')
outro_screen = pygame.image.load('images/Outro.jpg')
# --------------------------- #

# ---- SOUND EFFECTS ---- #
block_rotate = pygame.mixer.Sound('Sounds/block-rotate.ogg')
force_hit = pygame.mixer.Sound('Sounds/force-hit.ogg')
line_remove = pygame.mixer.Sound('Sounds/line-remove.ogg')
slow_hit = pygame.mixer.Sound('Sounds/slow-hit.ogg')
tetris_remove = pygame.mixer.Sound('Sounds/tetris-remove.ogg')
# ----------------------- #

# ---- BACKGROUND MUSIC ---- #
kalinka = pygame.mixer.Sound('Music/kalinka.ogg')
katyusha = pygame.mixer.Sound('Music/katyusha.ogg')
korobushka = pygame.mixer.Sound('Music/korobushka.ogg')
smuglianka = pygame.mixer.Sound('Music/smuglianka.ogg')
# -------------------------- #

# ---- BLOCK PREVIEWS ---- #
cube_block = pygame.image.load('Previews/cube-block.png').convert_alpha()
i_block = pygame.image.load('Previews/i-block.png').convert_alpha()
j_block = pygame.image.load('Previews/j-block.png').convert_alpha()
L_block = pygame.image.load('Previews/L-block.png').convert_alpha()
r_s_block = pygame.image.load('Previews/r-s-block.png').convert_alpha()
s_block = pygame.image.load('Previews/s-block.png').convert_alpha()
t_block = pygame.image.load('Previews/t-block.png').convert_alpha()

block_img_lst = [r_s_block, s_block, L_block, j_block, i_block, t_block, cube_block]  # MUST MATCH LIST IN CLASSES.PY
# ------------------------ #

# ---- FAVICON ---- #
favicon = pygame.image.load('images/favicon.png').convert_alpha()
pygame.display.set_icon(favicon)
# ----------------- #

# ---- FONTS ---- #
pygame.font.init()
my_font = pygame.font.SysFont('Arial Black', 21)


# --------------- #

# ------------- FUNCTIONS -------------------- #


def draw_grid():
    """ Draw horisontal and vertical lines on the entire game window.
        Space between the lines is GRIDSIZE.
    """
    for i in range(15):
        pygame.draw.line(screen, BLACK, (i * GRIDSIZE, 0), (i * GRIDSIZE, HEIGHT), 1)

    for i in range(24):
        pygame.draw.line(screen, BLACK, (0, i * GRIDSIZE), (GRIDSIZE * 24, i * GRIDSIZE), 1)


def redraw_screen():
    score_text = my_font.render(str(SCORE), True, WHITE)
    timer_text = my_font.render(str(round(pygame.time.get_ticks() / 1000, 2)), True, WHITE)
    level_text = my_font.render(str(level + 1), True, WHITE)

    screen.blit(grid_img, (0, 0))
    draw_grid()
    screen.blit(tetris_img, (GRIDSIZE * 14, 0))
    shape.draw(screen, GRIDSIZE)
    shadow.draw(screen, GRIDSIZE, True)
    obstacles.draw(screen, GRIDSIZE)

    # BLIT FONTS
    screen.blit(score_text, ((GRIDSIZE * 14) + 90, 460))
    screen.blit(timer_text, ((GRIDSIZE * 14) + 85, 538))
    screen.blit(level_text, ((GRIDSIZE * 14) + 100, 380))

    # BLIT NEXT SHAPE
    screen.blit(block_img_lst[nextShapeNo - 1], ((GRIDSIZE * 14) + 72, 240))

    pygame.display.flip()


def drop(my_shape):
    flow = False
    while not flow:
        my_shape.move_down()
        if my_shape.collides(floor) or my_shape.collides(obstacles):
            my_shape.move_up()
            flow = True

    if not my_shape.shadow:
        pygame.mixer.Channel(2).play(force_hit)


# -------------------------------------------- #

# ------------- MAIN PROGRAM -------------------- #

# infinity loop
while True:
    counter = 0

    shapeNo = randint(1, 7)
    nextShapeNo = randint(1, 7)

    shape = Shape(MIDDLE, TOP, shapeNo)
    floor = Floor(LEFT, ROWS, COLUMNS)
    leftWall = Wall(LEFT - 1, 0, ROWS)
    rightWall = Wall(RIGHT, 0, ROWS)
    # 再ゲームのための初期化
    obstacles = Obstacles(LEFT, FLOOR)
    inPlay = False
    hasPlayed = False
    level = 0
    SCORE = 0

    PREV_TETRIS = False

    # レベルのオーバーライド
#    SCORE = 1800

    previous_key = 0
    # ブロック接地猶予時間[ms]
    delayTime = 700
    # ブロック接地フラグ
    fitflag = False
    # ブロック接地までの猶予時間管理変数。　ブロックが一段下がるとブロック接地フラグと共にリセットされる
    downtime = 0

    # 曲選択（ランダム）
    bg_music = choice([kalinka, katyusha, korobushka, smuglianka])
    pygame.mixer.Channel(0).play(bg_music, -1)

    start_timer = 0

    # ---- INTRO SCREEN ---- #
    while not inPlay and not hasPlayed:
        screen.blit(intro_screen, (0, 0))
        pygame.display.flip()

        screen.blit(intro_screen, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
    #            if event.key == pygame.K_SPACE:
                if (event.key == pygame.K_SPACE) or (event.key == pygame.K_9):
                    inPlay = True
                    hasPlayed = True

    # ---------------------- #
    while inPlay:

        shadow = Shape(shape.col, shape.row, shape.clr, shape._rot, True)
        drop(shadow)

        if counter % LEVELS[level] == 0:
            # 最下段もしくは、ブロックに接地していた場合、カウントダウンを開始し1.5秒経過で着地とみなす
            # もしその間に移動が発生しフロアがなくなった場合はFallとする

            # ブロックの論理位置を一段落とす
            shape.move_down()
            # ブロックが接地（collides(floor)）または、ブロックの上にある（shape.collides(obstacles)）かをチェックする
            if shape.collides(floor) or shape.collides(obstacles):
                # 接地後時間経過判定
                if fitflag == False:
                    # 接地フラグ判定。　接地していなければ、現在時刻＋1.5秒をアラーム時刻に設定
                    fitflag = True
                    downtime = pygame.time.get_ticks() + delayTime
                    # 接地していないので下げたブロックの論理座標を元に戻す
                    shape.move_up()
                # 現在時刻が接地後猶予時間を超えていたらブロック接地とみなす
                elif ( pygame.time.get_ticks() >= downtime ):
                    # ブロック接地後判定処理の開始。　ブロックの論理位置を一段上げる（下げたブロックを元に戻す）
                    shape.move_up()
                    obstacles.append(shape)
                    pygame.mixer.Channel(5).play(slow_hit)
                    fullRows = obstacles.findFullRows(TOP, FLOOR, COLUMNS)

                    # --------- CHECK --------- #
                    if 4 > len(fullRows) > 0:
                        SCORE += 100 * len(fullRows)
                        pygame.mixer.Channel(3).play(line_remove)
                    elif len(fullRows) >= 4:
                        SCORE += 800 + (100 * (len(fullRows) - 4))
                        pygame.mixer.Channel(4).play(tetris_remove)
                        PREV_TETRIS = True
                    elif len(fullRows) >= 4 and PREV_TETRIS:
                        SCORE += 1200 + (100 * (len(fullRows) - 4))
                        PREV_TETRIS = True
                        pygame.mixer.Channel(4).play(tetris_remove)
                    else:
                        SCORE += 30 + ( level * 5 )
                    # ------------------------ #

                    # fullRowsが0以外（かつ4以下）ならライン消去発生。 ウェイト0.5secを挿入
                    if ( len(fullRows) != 0 ):
                        pygame.time.delay( 500 ) # 500ms = 0.5sec

                    obstacles.removeFullRows(fullRows)
                    shapeNo = nextShapeNo
                    nextShapeNo = randint(1, 7)
                    if not shape.row <= 1:
                        shape = Shape(MIDDLE, TOP, shapeNo)
                    else:
                        # ゲームオーバー
                        pygame.time.delay(2500)
                        inPlay = False
                else:
                    # 接地後時間経過判定がFalseだったので、ブロックの論理位置を元に戻す
                    shape.move_up()
            else:
                # ブロックは接地していなかった。　ブロック接地フラグをクリア
                fitflag = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                inPlay = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_8:
                    # ボタン押下時のダイアル誤動作抑止のために、２カウントで移動する判定
#                    if ( previous_key == pygame.K_8 ):
                    if True:
                        previous_key = 0
                        shape.rotateClkwise()
                        shape._rotate()
                        if shape.collides(leftWall) or shape.collides(rightWall) or shape.collides(floor) or shape.collides(
                                obstacles):
                            shape.rotateCntclkwise()
                            shape._rotate()
                        else:
                            pygame.mixer.Channel(1).play(block_rotate)
                    else:
                        previous_key = pygame.K_8

                if event.key == pygame.K_7:
                    # ボタン押下時のダイアル誤動作抑止のために、２カウントで移動する判定
#                    if ( previous_key == pygame.K_7 ):
                    if ( True ):
                        previous_key = 0
                        shape.rotateCntclkwise()
                        shape._rotate()
                        if shape.collides(leftWall) or shape.collides(rightWall) or shape.collides(floor) or shape.collides(
                                obstacles):
                            shape.rotateClkwise()
                            shape._rotate()
                        else:
                            pygame.mixer.Channel(1).play(block_rotate)
                    else:
                        previous_key = pygame.K_7

                if event.key == pygame.K_LEFT:
                    shape.move_left()
                    if shape.collides(leftWall):
                        shape.move_right()
                    elif shape.collides(obstacles):
                        shape.move_right()

                if event.key == pygame.K_RIGHT:
                    shape.move_right()
                    if shape.collides(rightWall):
                        shape.move_left()
                    elif shape.collides(obstacles):
                        shape.move_left()

    #            if event.key == pygame.K_DOWN:
    #            if event.key == pygame.K_SPACE:
                if event.key == pygame.K_9:
                    shape.move_down()
                    if shape.collides(floor) or shape.collides(obstacles):
                        # 接地後時間経過判定
                        if fitflag == False:
                            # 接地フラグ判定。　接地していなければ、現在時刻＋1.5秒をアラーム時刻に設定
                            fitflag = True
                            downtime = pygame.time.get_ticks() + delayTime
                            # 接地していないので下げたブロックの論理座標を元に戻す
                            shape.move_up()
                        elif ( pygame.time.get_ticks() >= downtime ):
                            shape.move_up()
                            obstacles.append(shape)
                            fullRows = obstacles.findFullRows(TOP, FLOOR, COLUMNS)
                            # --------- CHECK --------- #
                            if 4 > len(fullRows) > 0:
                                SCORE += 100 * len(fullRows)
                                pygame.mixer.Channel(3).play(line_remove)
                            elif len(fullRows) >= 4:
                                SCORE += 800 + (100 * (len(fullRows) - 4))
                                pygame.mixer.Channel(4).play(tetris_remove)
                                PREV_TETRIS = True
                            elif len(fullRows) >= 4 and PREV_TETRIS:
                                SCORE += 1200 + (100 * (len(fullRows) - 4))
                                PREV_TETRIS = True
                                pygame.mixer.Channel(4).play(tetris_remove)
                            else:
                                SCORE += 80
                            # ------------------------- #

                            obstacles.removeFullRows(fullRows)
                            shapeNo = nextShapeNo
                            nextShapeNo = randint(1, 7)
                            shape = Shape(MIDDLE, TOP, shapeNo)
    #                        shape = Shape(MIDDLE, TOP, shapeNo)
                        else:
                            # 接地後時間経過判定がFalseだったので、ブロックの論理位置を元に戻す
                            shape.move_up()
                    else:
                        # ブロック非接地なので接地フラグをリセット
                        fitflag = False
                        SCORE += (level+1) * 2


    #            if event.key == pygame.K_SPACE:
                if event.key == pygame.K_DOWN:
                    drop(shape)
                    obstacles.append(shape)
                    shapeNo = nextShapeNo
                    nextShapeNo = randint(1, 7)
                    shape = Shape(MIDDLE, TOP, shapeNo)
                    fullRows = obstacles.findFullRows(TOP, FLOOR, COLUMNS)
                    # --------- CHECK --------- #
                    if 4 > len(fullRows) > 0:
                        SCORE += 100 * len(fullRows)
                        pygame.mixer.Channel(3).play(line_remove)
                    elif len(fullRows) >= 4:
                        SCORE += 800 + (100 * (len(fullRows) - 4))
                        pygame.mixer.Channel(4).play(tetris_remove)
                        PREV_TETRIS = True
                    elif len(fullRows) >= 4 and PREV_TETRIS:
                        SCORE += 1200 + (100 * (len(fullRows) - 4))
                        PREV_TETRIS = True
                        pygame.mixer.Channel(4).play(tetris_remove)
                    # ------------------------- #
                    obstacles.removeFullRows(fullRows)

        if 1000 >= SCORE >= 500:
            level = 1
        elif 2000 >= SCORE > 1000:
            level = 2
        elif 3000 >= SCORE > 2000:
            level = 3
        elif 4500 >= SCORE > 3000:
            level = 4
        elif 6000 >= SCORE > 4500:
            level = 5
        elif 10000 >= SCORE > 15000:
            level = 6
        elif 22500 >= SCORE > 15000:
            level = 7
        elif 35000 >= SCORE > 50000:
            level = 8
        elif SCORE >= 50000:
            level = 9

        PREV_TETRIS = False
        counter += 1
        redraw_screen()

    while not inPlay and hasPlayed:
        if start_timer == 0:
            start_timer = pygame.time.get_ticks() + 8000
        screen.blit(outro_screen, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
    #            if event.key == pygame.K_SPACE:
                if (event.key == pygame.K_SPACE) or (event.key == pygame.K_o):
                    # キーを押されると、メインプログラムの最初から実行
                    hasPlayed = False
                    pygame.time.delay(500)
                    pygame.event.clear()
                    break
#                    pygame.quit()
#                    sys.exit(0)

        # 8秒経過でタイトル画面へ
        if pygame.time.get_ticks() >= start_timer:
            break
#           pygame.quit()
#           sys.exit(0)

# ----------------------------------------------- #

pygame.quit()
sys.exit("Exited Final")
