import pygame
import random
from math import *

pygame.init()
pygame.display.set_caption("Hangman")
screen = pygame.display.set_mode((1280, 720))


default_font = pygame.font.Font("blzee.ttf", 80)
button_font = pygame.font.Font("blzee.ttf", 40)
answer_font = pygame.font.Font("blzee.ttf", 50)
end_font = pygame.font.Font("blzee.ttf", 150)
background_image = pygame.image.load("background.jpg")
white_font = (255, 255, 255)
highlight_font = (233, 233, 78)
limbs = 0
stages = ["hangman0.png", "hangman1.png", "hangman2.png", "hangman3.png", "hangman4.png", "hangman5.png",
          "hangman6.png"]
hangman_images = [pygame.image.load(i) for i in stages]
used_button = False
guessed_work = []

alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()

words = open("words.txt", "r").readlines()
guess_phrase = words[random.randint(0, len(words) - 1)]
if "\n" in guess_phrase:
    guess_phrase = guess_phrase[:-1]
status_word = ""
for char in guess_phrase:
    if char == " ":
        char = char
    else:
        char = "_"
    status_word += char + " "
    guessed_work.append(" ")
holder = guess_phrase


def onscreen_word():
    global base_x
    displayed = default_font.render(status_word, True, white_font)
    base_x = 640 - len(status_word) * 20
    screen.blit(displayed, (base_x, 600))


def letter_buttons(x, y, letter, state):
    if letter == " ":
        pass
    elif state == "resting":
        pygame.draw.circle(screen, white_font, (x, y), 30, 2)
        button = button_font.render(letter, True, white_font)
        screen.blit(button, (x - 12, y - 21))
    elif state == "hovering":
        pygame.draw.circle(screen, highlight_font, (x, y), 35, 5)
        button = button_font.render(letter, True, highlight_font)
        screen.blit(button, (x - 12, y - 21))


running = True
while running:
    global base_x
    screen.blit(background_image, (0, 0))
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            for idx, i in enumerate(alphabet):
                if i == " ":
                    pass
                else:
                    if idx <= 12:
                        idx_reference = idx
                        y = 80
                    if idx >= 13:
                        idx_reference = idx - 13
                        y = 180
                    distance = ((mouse_position[0] - (90 * idx_reference + 95)) ** 2 + (mouse_position[1] - y) ** 2) ** 0.5
                    if distance <= 30:
                        if i in guess_phrase:
                            for z in range(holder.count(i)):
                                guessed_work[holder.find(i)] = i
                                holder = " " * (holder.find(i) + 1) + holder[holder.find(i) + 1:]

                        if i not in guess_phrase:
                            limbs += 1

                        alphabet[idx] = " "
                        holder = guess_phrase

    for idx, i in enumerate(alphabet):
        if idx <= 12:
            idx = idx
            y = 80
        if idx >= 13:
            idx = idx - 13
            y = 180
        distance = ((mouse_position[0] - (90 * idx + 95)) ** 2 + (mouse_position[1] - y) ** 2) ** 0.5
        if distance <= 30:
            letter_buttons(90 * idx + 95, y, i, "hovering")
        else:
            letter_buttons(90 * idx + 95, y, i, "resting")

    for idx, x in enumerate(guessed_work):
        insertion = answer_font.render(x, True, white_font)
        screen.blit(insertion, (idx * 83 + (640 - len(status_word) * 20), 600))

    screen.blit(hangman_images[limbs], (500, 240))
    onscreen_word()
    if ''.join(guessed_work) == guess_phrase:
        winner_text = end_font.render("You Win!", True, white_font)
        screen.blit(background_image, (0, 0))
        screen.blit(winner_text, (300, 250))
        for idx, x in enumerate(guessed_work):
            insertion = answer_font.render(x, True, white_font)
            screen.blit(insertion, (idx * 83 + (640 - len(status_word) * 20), 600))
        alphabet = " "
    if limbs == 6:
        winner_text = end_font.render("You Lose!", True, white_font)
        screen.blit(background_image, (0, 0))
        screen.blit(winner_text, (300, 250))
        holder = guess_phrase
        guessed_work = []
        for i in guess_phrase:
            guessed_work += i
        for idx, x in enumerate(guessed_work):
            insertion = answer_font.render(x, True, white_font)
            screen.blit(insertion, (idx * 83 + (640 - len(status_word) * 20), 600))
        alphabet = " "
    pygame.display.update()

pygame.quit()
