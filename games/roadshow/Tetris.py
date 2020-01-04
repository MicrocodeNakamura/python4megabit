#

import pygame

pygame.init()

# ---------------------------------------#


# -------------IMAGES and MUSIC--------------------#

# ---- BACKGROUND IMAGES ---- #
#tetris_img = pygame.image.load('images/Tetris.jpg')

# --------------------------- #

# ---- SOUND EFFECTS ---- #
#block_rotate = pygame.mixer.Sound('Sounds/block-rotate.ogg')
# ----------------------- #

# ---- BACKGROUND MUSIC ---- #
#kalinka = pygame.mixer.Sound('Music/kalinka.ogg')
# -------------------------- #

# ---- BLOCK PREVIEWS ---- #
#cube_block = pygame.image.load('Previews/cube-block.png').convert_alpha()

# ---- FONTS ---- #
pygame.font.init()
font = pygame.font.SysFont('Arial Black', 21)


# --------------- #

# ------------- FUNCTIONS -------------------- #

# ------------- MAIN PROGRAM -------------------- #

# infinity loop
while True:
#    bg_music = choice([kalinka, katyusha, korobushka, smuglianka])
#    pygame.mixer.Channel(0).play(bg_music, -1)

    # ---- INTRO SCREEN ---- #

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            inPlay = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_8:
                # ボタン押下時のダイアル誤動作抑止のために、２カウントで移動する判定
    #                    if ( previous_key == pygame.K_8 ):

# while not inPlay and hasPlayed:

# ----------------------------------------------- #

pygame.quit()
sys.exit("Exited Final")
