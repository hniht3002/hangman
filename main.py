import math
import time

from variable import *
import pygame

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# game loop
clock = pygame.time.Clock()
isRunning = True
newWord = True
GUESSED = ""
isCorrect = False
isHoverNextArrow = False


# function
def load_images():
    images = []
    for i in range(1, 9):
        image = pygame.image.load(("assets/" + str(i) + ".JPG"))
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        images.append(image)
    return images


def load_button_letters():
    BTN_LETTERS = []
    BTN_START_X = 50
    BTN_START_Y = 350
    A_CODE = 65
    for i in range(26):
        x = BTN_START_X
        y = BTN_START_Y
        BTN_START_X = BTN_START_X + 20 + BTN_GAP * 2
        if (i == 9):
            BTN_START_X = 46
            BTN_START_X = BTN_START_X + 33
            BTN_START_Y = BTN_START_Y + 40 + BTN_GAP
        elif (i == 18):
            BTN_START_X = 78
            BTN_START_X = BTN_START_X + BTN_GAP * 2 + BTN_RADIUS
            BTN_START_Y = BTN_START_Y + 40 + BTN_GAP

        BTN_LETTERS.append([x, y, chr(A_CODE + i), True])
    return BTN_LETTERS


def findAllIndex(ch, s):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def replaceAt(index, char, s):
    ltrList = list(s)
    for i in index:
        ltrList[i] = char

    return "".join(ltrList)


def updateGuessWord(character, s):
    ltrList = list(s)
    if character in KEYWORD:
        pos = (findAllIndex(character, KEYWORD))
        for index in pos:
            ltrList[index * 2] = character

    return "".join(ltrList)


# display UI
def showStartScreen():
    # show menu screen
    print()


def showChooseSubject():
    # show choose subject screen
    print()


def showMainGame():
    keyBG = pygame.image.load(("assets/menu/BG BUTTON_ELEMENTS.png"))
    nextArrow = pygame.image.load("assets/menu/next_arrow.png")
    # draw level
    LEVEL_TEXT = pygame.font.SysFont(FONT, 32).render("Level: " + str(LEVEL), 1, WHITE)
    display.blit(LEVEL_TEXT, (322 - LEVEL_TEXT.get_width() / 2, 50))
    # draw subject
    SJ = pygame.font.SysFont(FONT, 32).render(SUBJECT[SUBJECT_INDEX], 1, WHITE)
    display.blit(SJ, (322 - SJ.get_width() / 2, 100))
    if not isCorrect:
        # draw message
        message = pygame.font.SysFont(FONT, 32).render("Next ", 1, WHITE)
        display.blit(message, (800, 400))
        if isHoverNextArrow:
            display.blit(pygame.transform.scale(nextArrow, (150, 100)), (800, 400))
        else:
            display.blit(pygame.transform.scale(nextArrow, (100, 70)), (800, 400))
    # draw keyword
    GUESSED_WORD = pygame.font.SysFont(FONT, 32).render(GUESSED, 1, WHITE)
    display.blit(GUESSED_WORD, (322 - GUESSED_WORD.get_width() / 2, 200))
    # draw button

    keyBG_sm = pygame.transform.scale(keyBG, (65, 65))
    for letter in BTN_LETTERS:
        posx, posy, ltr, visible = letter
        if (visible):
            # pygame.gfxdraw.aacircle(display, posx, posy, BTN_RADIUS, BLACK)
            # pygame.gfxdraw.filled_circle(display, posx, posy, BTN_RADIUS, BLACK)
            display.blit(keyBG_sm, (posx - 31, posy - 37))
            text = pygame.font.SysFont(FONT, 32).render(ltr, 1, BLACK)
            display.blit(text, (posx - text.get_width() / 2, posy - text.get_height() / 2))


def showEndGame():
    # show end screen
    print()


# button variables
BTN_LETTERS = load_button_letters()

# load images
images = load_images()


def draw():
    display.fill(WHITE)
    display.blit(images[HANGMAN_STATUS], (0, 0))

    if GAME_STATUS == 0:
        showStartScreen()
    elif GAME_STATUS == 1:
        showChooseSubject()
    elif GAME_STATUS == 2:
        showMainGame()
    elif GAME_STATUS == 3:
        showEndGame()
    pygame.display.update()


while isRunning:
    clock.tick(FPS)
    KEYWORD = WORD_LIST[SUBJECT_INDEX][LEVEL - 1]
    if newWord:
        GUESSED = "_ " * len(KEYWORD)
        newWord = False
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            isRunning = False
        if GAME_STATUS == 0:
            # handle start screen
            print("Load start screen")

        elif GAME_STATUS == 1:
            # handle choose subject
            print()
        elif GAME_STATUS == 2:
            m_x, m_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for letter in BTN_LETTERS:
                    x, y, ltr, visible = letter
                    if (visible):
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < BTN_RADIUS:
                            valid = False

                            if ltr in KEYWORD: valid = True

                            # update GUESSED if character is in KEYWORD
                            if valid:
                                GUESSED = updateGuessWord(ltr, GUESSED)

                                if "_" not in GUESSED:
                                    isCorrect = True


                            # update hangman_status if char is not in KEYWORD
                            else:
                                HANGMAN_STATUS += 1
                                # handle endgame
                                if HANGMAN_STATUS == len(images) - 1: print(
                                    "End Game"); HANGMAN_STATUS = HANGMAN_STATUS - 1

                                print(HANGMAN_STATUS)
                            # update button visibility
                            letter[3] = False
                if isCorrect and m_x in range(799, 845) and m_y in range(403, 432):
                    LEVEL += 1
                    BTN_LETTERS = load_button_letters()
                    newWord = True
                    isCorrect = False

            if m_x in range(799, 845) and m_y in range(403, 432):
                isHoverNextArrow = True
            else: isHoverNextArrow = False


        elif GAME_STATUS == 3:
            # handle endgame
            print()
