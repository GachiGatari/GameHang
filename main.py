import pygame
import os
import math
import random
import sys


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.init()
WIDTH,HEIGHT = 800,500
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Висельница")


#font
LETTER_FONT = pygame.font.SysFont('comicsans', 28)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
MESSAGE_FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

#buton
RADIUS = 15
GAP = 10
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 16) / 2)
starty = 400
A = 1040

for i in range(32):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 16))
    y = starty + ((i // 16) * (GAP + RADIUS * 2))
    letters.append([x, y,chr(A+i),True])


#image download
asset_url = resource_path("/home/maxim/PycharmProjects/pythonProject/venv/images/hangman")
images = []
for i in range(6):
    image = pygame.image.load(asset_url+str(i)+".png")
    images.append(image)
#game var
hangman_status = 0
words = ["МАКСИМ","НЕКИТ","ПИТОН","ЛИНУКС","СТРИЖМЫК"]
word = random.choice(words)
guessed = []
#color
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

#setup game loop


def draw():
    win.fill(WHITE)
    #draw title
    text = TITLE_FONT.render("Виселица by JuniorHikki",1,BLACK)
    win.blit(text,(WIDTH/2 - text.get_width()/2,20))
    #draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word = display_word + letter +" "
        else:
            display_word = display_word + "_ "

    text = WORD_FONT.render(display_word,1,BLACK)
    win.blit(text,(400,200))

    #draw button
    for letter in letters:
        x,y,ltr,visible = letter
        if visible:
            pygame.draw.circle(win,BLACK,(x,y),RADIUS,3)
            text = LETTER_FONT.render(ltr,1,BLACK)
            win.blit(text,(x-text.get_width()/2,y-text.get_height()/2))

    win.blit(images[hangman_status],(100,150))
    pygame.display.update()

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    if message == "Ты победил,ёпта!":
        text = MESSAGE_FONT.render(f"{message}Словом было {word}", 1, GREEN)
    else:
        text = MESSAGE_FONT.render(f"{message}Словом было {word}", 1, RED)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)

run = True
FPS = 60
clock = pygame.time.Clock()

while run:
    clock.tick(FPS)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x,m_y = pygame.mouse.get_pos()
            for letter in letters:
                x,y,ltr,visible = letter
                if visible:
                    dis = math.sqrt((x-m_x)**2+(y-m_y)**2)
                    if dis<RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman_status+=1
        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
    if won:
        display_message("Ты победил,ёпта!")
        break
    if hangman_status == 6:
        display_message("Ты проиграл,ёпта(")
        break


pygame.quit()