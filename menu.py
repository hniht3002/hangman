import pygame, sys
from button import Button
from pygame import mixer

pygame.init()

#Display
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("picture/10.jpg")
BG = pygame.transform.scale(BG, (1280, 720))

#load image
def load_images():
    images = []
    for i in range(2, 11):
        image = pygame.image.load(("picture/" + str(i) + ".JPG"))
        image = pygame.transform.scale(image, (1280, 720))
        images.append(image)
    return images

#font
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("picture/juice itc.ttf", size)

#Play
def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    

#Instruction
def instruction():
    while True:
        INSTRUCTION_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        INSTRUCTION_TEXT = get_font(45).render("This is the INSTRUCTION screen.", True, "Black")
        INSTRUCTION_RECT = INSTRUCTION_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(INSTRUCTION_TEXT, INSTRUCTION_RECT)

        INSTRUCTION_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        INSTRUCTION_BACK.changeColor(INSTRUCTION_MOUSE_POS)
        INSTRUCTION_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTION_BACK.checkForInput(INSTRUCTION_MOUSE_POS):
                    main_menu()

        pygame.display.update()
        
#Main Menu
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = pygame.image.load("picture/11.jpg")
        MENU_TEXT = pygame.transform.scale(MENU_TEXT, (1000, 250))
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 80))
        SCREEN.blit(MENU_TEXT, MENU_RECT) 

        PLAY_BUTTON = Button(image=pygame.image.load("picture/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        INSTRUCTION_BUTTON = Button(image=pygame.image.load("picture/Options Rect.png"), pos=(640, 400), 
                            text_input="INSTRUCTION", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("picture/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, INSTRUCTION_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if INSTRUCTION_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instruction()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()

# load images
images = load_images()

#Background sound
mixer.music.load('picture/bg sound.mp3')
mixer.music.play(-1)

class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()

		self.image = img
		self.scale = scale
		self.image = pygame.transform.scale(self.image, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

	def draw(self, SCREEN):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		SCREEN.blit(self.image, self.rect)
		return action


on = pygame.image.load('picture/12.jpg')
off = pygame.image.load('picture/13.jpg')


sound_btn = Button(off, (24, 24), 300, 50)

# button = Button(off, (100, 70), WIDTH//2-100, HEIGHT//2)
sound_on = False

running = True
while running:
	SCREEN.fill(('white'))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q or \
				event.key == pygame.K_ESCAPE:
				running = False

	if sound_btn.draw(SCREEN):
		sound_on = not sound_on
		
		if sound_on:
			sound_btn.update_image(on)
		else:
			sound_btn.update_image(off)
	pygame.display.update()

# # Function to toggle music
def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.pause()
        music_playing = False
    else:
        pygame.mixer.music.unpause()
        music_playing = True

# running = True
# while running:
#     SCREEN.fill('WHITE')
#     volume_btn.draw(SCREEN)

#     # # Check for events
#     # for event in pygame.event.get():
#     #     if event.type == pygame.QUIT:
#     #         running = False
#     #     elif event.type == pygame.MOUSEBUTTONDOWN:
#     #         if event.button == 1:  # Left mouse button
#     #             if button_rect.collidepoint(event.pos):
#     #                 toggle_music()

#     # # Change button image when hovered or pressed
#     # if button_rect.collidepoint(pygame.mouse.get_pos()):
#     #     SCREEN.blit(button_image_pressed, button_rect)
#     # else:
#     #     SCREEN.blit(button_image_normal, button_rect)

#     # pygame.display.flip()

# # Quit Pygame
# pygame.quit()
