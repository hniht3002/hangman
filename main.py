import math

from button import Button
from variable import *
import pygame, sys

pygame.init()
pygame.mixer.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")


# game loop
clock = pygame.time.Clock()
isRunning = True
newWord = True
GUESSED = ""
isCorrect = False
isMute = False
pygame.mixer.music.load("assets/picture/bg sound.mp3")
pygame.mixer.music.play(-1)
def get_font(size):
    return pygame.font.Font("assets/picture/juice itc.ttf", size)

def toggleMusic():
    if(not isMute):
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(1)

NEXT_BUTTON = Button(
    image=pygame.transform.scale(pygame.image.load("assets/picture/Play Rect.png"), (200, 50)),
    pos=(WIDTH * 0.25 + 78, 320),
    text_input="NEXT LEVEL", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

MUSIC_ON = Button(
    image=pygame.transform.scale(pygame.image.load("assets/picture/12.JPG"), (70, 70)),
    pos=(WIDTH - 50, 50),
    text_input="", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

MUSIC_OFF = Button(
    image=pygame.transform.scale(pygame.image.load("assets/picture/13.JPG"), (60, 60)),
    pos=(WIDTH - 50, 50),
    text_input="", font=get_font(40), base_color="#d7fcd4", hovering_color="White")


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
    global GAME_STATUS
    global isMute
    BG = pygame.image.load("assets/menu/MENU BG.png")
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    MENU_TEXT = pygame.image.load("assets/menu/TEXT_ELEMENTS.png")
    MENU_TEXT = pygame.transform.scale(MENU_TEXT, (540, 188))

    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 170))

    PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/picture/Play Rect.png"), (100, 50)),
                         pos=(WIDTH / 2, 320),
                         text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/picture/Quit Rect.png"), (100, 50)),
                         pos=(WIDTH / 2, 400),
                         text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

    MUSIC = MUSIC_OFF
    if not isMute:
        MUSIC = MUSIC_ON

    display.blit(MENU_TEXT, MENU_RECT)

    for button in [PLAY_BUTTON, QUIT_BUTTON, MUSIC]:
        button.changeColor(MENU_MOUSE_POS)
        button.update(display)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                GAME_STATUS = 1
            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()
            if MUSIC.checkForInput(MENU_MOUSE_POS):
                toggleMusic()
                isMute = not isMute

def showChooseSubject():
    global GAME_STATUS
    global SUBJECT_INDEX
    global isMute
    background_color = (0, 0, 0)

    # Màu ô chữ
    text_box_color = (255, 255, 255)

    # Font và kích thước chữ
    font = get_font(32)

    # Dữ liệu cho các cột và từ
    column1_data = SUBJECT[:5]
    column2_data = SUBJECT[-5:]

    # Vẽ background
    display.blit(images[HANGMAN_STATUS], (0, 0))
    # Vẽ nút "Back"
    BACK_BUTTON = Button(
        image=pygame.transform.scale(pygame.image.load("assets/picture/Play Rect.png"), (100, 50)),
        pos=(WIDTH * 0.01 + 78, 50),
        text_input="BACK", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

    MENU_MOUSE_POS = pygame.mouse.get_pos()
    BACK_BUTTON.changeColor(MENU_MOUSE_POS)
    BACK_BUTTON.update(display)

    MUSIC = MUSIC_OFF
    if not isMute:
        MUSIC = MUSIC_ON

    MUSIC.update(display)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                GAME_STATUS = 0
            if MUSIC.checkForInput(MENU_MOUSE_POS):
                isMute = not isMute

    # Vẽ tiêu đề "Choose Topic"
    title_text = font.render("Choose Topic", True, (255, 255, 255))
    display.blit(title_text, (WIDTH // 1.95 - title_text.get_width() // 2, 65))

    # Vẽ cột 1
    column1_x = WIDTH // 6
    column_y = 150
    for index, word in enumerate(column1_data):
        rect = pygame.Rect(column1_x, column_y, 250, 50)
        pygame.draw.rect(display, text_box_color, rect)
        text_surface = font.render(word, True, background_color)
        display.blit(text_surface,
                     (column1_x + 75 - text_surface.get_width() // 2, column_y + 25 - text_surface.get_height() // 2))
        if rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  # Kiểm tra xem có phải là lúc click chuột trái không
                SUBJECT_INDEX = index
                GAME_STATUS = 2
        column_y += 60
    # Vẽ cột 2
    column2_x = WIDTH // 4 * 2.4
    column_y = 150
    for index, word in enumerate(column2_data):
        rect = pygame.Rect(column2_x, column_y, 250, 50)
        pygame.draw.rect(display, text_box_color, rect)  # Tăng chiều dài và thêm khoảng trống
        text_surface = font.render(word, True, background_color)
        display.blit(text_surface,
                     (column2_x + 75 - text_surface.get_width() // 2, column_y + 25 - text_surface.get_height() // 2))
        if rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  # Kiểm tra xem có phải là lúc click chuột trái không
                SUBJECT_INDEX = index + 5
                GAME_STATUS = 2
        column_y += 60


def showMainGame():
    global isMute
    keyBG = pygame.image.load(("assets/menu/BG BUTTON_ELEMENTS.png"))
    nextArrow = pygame.image.load("assets/menu/next_arrow.png")

    MUSIC = MUSIC_OFF
    if not isMute:
        MUSIC = MUSIC_ON
    MUSIC.update(display)

    # draw level
    LEVEL_TEXT = get_font(32).render("Level: " + str(LEVEL), 1, WHITE)
    display.blit(LEVEL_TEXT, (322 - LEVEL_TEXT.get_width() / 2, 50))
    # draw subject
    SJ = get_font(32).render(SUBJECT[SUBJECT_INDEX], 1, WHITE)
    display.blit(SJ, (322 - SJ.get_width() / 2, 100))
    if isCorrect:
        # draw message
        NEXT_BUTTON.changeColor(pygame.mouse.get_pos())
        NEXT_BUTTON.update(display)

    # draw keyword
    GUESSED_WORD = get_font(32).render(GUESSED, 1, WHITE)
    display.blit(GUESSED_WORD, (322 - GUESSED_WORD.get_width() / 2, 200))
    # draw button
    keyBG_sm = pygame.transform.scale(keyBG, (65, 65))
    for letter in BTN_LETTERS:
        posx, posy, ltr, visible = letter
        if (visible and not isCorrect):
            display.blit(keyBG_sm, (posx - 31, posy - 37))
            text = get_font(32).render(ltr, 1, BLACK)
            display.blit(text, (posx - text.get_width() / 2, posy - text.get_height() / 2))
def showResultGame(msg, color):
    global GAME_STATUS
    global LEVEL
    global HANGMAN_STATUS
    global SUBJECT_INDEX;
    global newWord;

    font = get_font(60)
    font_button = get_font(40)
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    # Vẽ background
    display.blit(images[HANGMAN_STATUS], (0, 0))

    # Hiển thị chữ "End Game"
    text = font.render(msg, True, color)
    display.blit(text, (WIDTH // 2 - text.get_width() // 2, 200))

    # Vẽ nút Restart

    RESTART_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/picture/Play Rect.png"), (100, 50)),
                            pos=(WIDTH * 0.25 + 150, 320),
                            text_input="Restart", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

    # Vẽ nút Thoát

    QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/picture/Play Rect.png"), (100, 50)),
                         pos=(WIDTH * 0.75 - 150, 320),
                         text_input="Exit", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

    for button in [RESTART_BUTTON, QUIT_BUTTON]:
        button.changeColor(MENU_MOUSE_POS)
        button.update(display)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if RESTART_BUTTON.checkForInput(MENU_MOUSE_POS):
                GAME_STATUS = 0;
                LEVEL = 1
                SUBJECT_INDEX = 0
                HANGMAN_STATUS = 0
                newWord = True

            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()


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
        showResultGame("You Lose!", BLACK)
    else:
        showResultGame("You Win!!!", WHITE)
    pygame.display.update()


while isRunning:
    clock.tick(FPS)
    draw()
    for event in pygame.event.get():
        if GAME_STATUS == 0:
            showStartScreen()
        elif GAME_STATUS == 1:
            showChooseSubject()
        elif GAME_STATUS == 2:
            KEYWORD = WORD_LIST[SUBJECT_INDEX][LEVEL - 1]
            if newWord:
                GUESSED = "_ " * len(KEYWORD)
                newWord = False
                BTN_LETTERS = load_button_letters()

            m_x, m_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(m_x in range(890, 930) and m_y in range(30, 70)) :
                    isMute = not isMute
                for letter in BTN_LETTERS:
                    x, y, ltr, visible = letter
                    if (visible and not isCorrect):
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < BTN_RADIUS:
                            valid = False

                            if ltr in KEYWORD: valid = True

                            # update GUESSED if character is in KEYWORD
                            if valid:
                                GUESSED = updateGuessWord(ltr, GUESSED)

                                if "_" not in GUESSED:
                                    if LEVEL + 1 == 6:
                                        GAME_STATUS = 4
                                    else:
                                        isCorrect = True



                            # update hangman_status if char is not in KEYWORD
                            else:
                                HANGMAN_STATUS += 1
                                # handle endgame
                                if HANGMAN_STATUS == len(images) - 1:
                                    GAME_STATUS = 3
                                    LEVEL = 1
                            # update button visibility
                            letter[3] = False

                if isCorrect and NEXT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    LEVEL += 1
                    BTN_LETTERS = load_button_letters()
                    newWord = True
                    isCorrect = False



        elif GAME_STATUS == 3:
            showResultGame("You Lose!", BLACK)

        else:
            showResultGame("You Win!!!", WHITE)

        if event.type == pygame.QUIT:
            pygame.quit()
            isRunning = False
            break
