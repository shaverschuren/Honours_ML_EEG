# ToDo: Implement counter
# ToDo: Implement tracking (to csv)
# ToDo: Make easier / harder levels
# ToDo: Fix border
# ToDo: evt. Implement distractions etc.

import pygame
import random
import itertools
import pandas as pd
import datetime


class Button:
    def __init__(self, rect, command):
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size).convert()
        # self.image.fill((255,255,255))
        self.function = command

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.function()

    def draw(self, surf):
        surf.blit(self.image, self.rect)


def btn1_press():
    # print('button1_was_pressed')
    global selected_items
    if 1 not in selected_items:
        selected_items.append(1)
    else:
        selected_items.remove(1)


def btn2_press():
    # print('button2_was_pressed')
    global selected_items
    if 2 not in selected_items:
        selected_items.append(2)
    else:
        selected_items.remove(2)


def btn3_press():
    # print('button3_was_pressed')
    global selected_items
    if 3 not in selected_items:
        selected_items.append(3)
    else:
        selected_items.remove(3)


def btn4_press():
    # print('button4_was_pressed')
    global selected_items
    if 4 not in selected_items:
        selected_items.append(4)
    else:
        selected_items.remove(4)


def btn5_press():
    # print('button5_was_pressed')
    global selected_items
    if 5 not in selected_items:
        selected_items.append(5)
    else:
        selected_items.remove(5)


def btn6_press():
    # print('button6_was_pressed')
    global selected_items
    if 6 not in selected_items:
        selected_items.append(6)
    else:
        selected_items.remove(6)


def change_selection_visualisation():

    global cards
    global selected_items
    # print('selection changed to ', selected_items)

    button_ll_coords = [(100, 50), (600, 50), (1100, 50), (100, 550), (600, 550), (1100, 550)]
    display_cards()

    for item in selected_items:
        # Draw frame
        pygame.draw.rect(screen, (255, 0, 0), (button_ll_coords[item-1][0]+2, button_ll_coords[item-1][1]+2, 395, 395), 6)
        # Fix ugly corners ...
        pygame.draw.rect(screen, (255, 0, 0), (button_ll_coords[item-1][0], button_ll_coords[item-1][1], 6, 6))
        pygame.draw.rect(screen, (255, 0, 0), (button_ll_coords[item-1][0]+394, button_ll_coords[item-1][1], 6, 6))
        pygame.draw.rect(screen, (255, 0, 0), (button_ll_coords[item-1][0]+394, button_ll_coords[item-1][1]+394, 6, 6))
        pygame.draw.rect(screen, (255, 0, 0), (button_ll_coords[item-1][0], button_ll_coords[item-1][1]+394, 6, 6))


def check_answer():
    # selected_items, cards, attribute_list
    selected_cards = []
    selected_attributes = []
    shape_list = []
    color_list = []
    fill_list = []
    for selected_item in selected_items:
        selected_cards.append(cards[selected_item-1])

    for selected_card in selected_cards:
        selected_attributes.append(attribute_list[selected_card])

    for i in range(3):
        shape_list.append(selected_attributes[i][0])
        color_list.append(selected_attributes[i][1])
        fill_list.append(selected_attributes[i][2])

    att_set_list = []
    for att_list in [shape_list, color_list, fill_list]:
        all_same = all(elem == att_list[0] for elem in att_list)
        all_different = len(att_list) == len(set(att_list))

        if all_same == True or all_different == True:
            att_set = True
        else:
            att_set = False

        att_set_list.append(att_set)

    if all(elem == True for elem in att_set_list):
        correct_answer = True
    else:
        correct_answer = False

    return correct_answer


def store_answer(true_answer):
    global game_data

    append_row = [datetime.datetime.now(), int(true_answer)]

    append_df = pd.DataFrame([append_row], columns=["TimeStamp", "correct"])
    game_data = pd.concat([game_data, append_df], ignore_index=True)

    game_data.loc[[len(game_data)-1]].to_csv(logs_path, mode='a', index=False, header=False)

    print(game_data.loc[[len(game_data)-1]])


def check_for_set(cards):
    present_set = False

    card_attributes = []
    for card in cards:
        card_attributes.append(attribute_list[card])

    for combination in itertools.combinations(card_attributes, 3):
        shape_list = []
        color_list = []
        fill_list = []
        for i in range(3):
            shape_list.append(combination[i][0])
            color_list.append(combination[i][1])
            fill_list.append(combination[i][2])

        att_set_list = []
        for att_list in [shape_list, color_list, fill_list]:
            all_same = all(elem == att_list[0] for elem in att_list)
            all_different = len(att_list) == len(set(att_list))

            if all_same == True or all_different == True:
                att_set = True
            else: att_set = False

            att_set_list.append(att_set)

        if all(elem == True for elem in att_set_list):
            present_set = True

    return present_set


def choose_display_card(exclude):
    randInt = random.randint(0, 26)
    return choose_display_card(exclude) if randInt in exclude else randInt


def switch_f():

    global cards
    global selected_items

    selected_items = []

    present_set = False
    while not present_set:
        cards = []
        for i in range(6):
            card = choose_display_card(cards)
            cards.append(card)
        present_set = check_for_set(cards)

    display_cards()


def display_cards():

    screen.blit(symbol_list[cards[0]], [100, 50])
    screen.blit(symbol_list[cards[1]], [600, 50])
    screen.blit(symbol_list[cards[2]], [1100, 50])
    screen.blit(symbol_list[cards[3]], [100, 550])
    screen.blit(symbol_list[cards[4]], [600, 550])
    screen.blit(symbol_list[cards[5]], [1100, 550])


def main_gui():
    global screen
    global symbol_list
    global attribute_list
    global selected_items
    global cards
    global true_answer
    global logs_path
    global game_data

    red = (200,0,0)
    green = (0,150,50)
    blue = (0,50,90)

    bright_red = (255,0,0)
    bright_green = (0,255,0)

    pygame.init()

    screen_height = 1080
    screen_width = 1920

    screen = pygame.display.set_mode([screen_width, screen_height], flags=pygame.FULLSCREEN)
    screen.fill(blue)

    symbol_list = []
    attribute_list = []

    for shape in [1, 2, 3]:
        for color in [1, 2, 3]:
            for fill in [1, 2, 3]:
                attribute_list.append((shape, color, fill))
                symbol_tag = str(shape) + "-" + str(color) + "-" + str(fill)
                symbol_path = "set_cards\\" + symbol_tag + ".png"
                symbol_list.append(pygame.image.load(symbol_path).convert())

    btn1 = Button(rect=(100, 50, 400, 400), command=btn1_press)
    btn2 = Button(rect=(600, 50, 400, 400), command=btn2_press)
    btn3 = Button(rect=(1100, 50, 400, 400), command=btn3_press)
    btn4 = Button(rect=(100, 550, 400, 400), command=btn4_press)
    btn5 = Button(rect=(600, 550, 400, 400), command=btn5_press)
    btn6 = Button(rect=(1100, 550, 400, 400), command=btn6_press)

    # pygame.draw.rect(screen, (0,0,0), (100, 50, 400, 400), 1)
    # pygame.draw.rect(screen, (0,0,0), (600, 50, 400, 400), 1)
    # pygame.draw.rect(screen, (0,0,0), (1100, 50, 400, 400), 1)
    # pygame.draw.rect(screen, (0,0,0), (100, 550, 400, 400), 1)
    # pygame.draw.rect(screen, (0,0,0), (600, 550, 400, 400), 1)
    # pygame.draw.rect(screen, (0,0,0), (1100, 550, 400, 400), 1)

    cards = []
    selected_items = []
    old_len_selected_items = 0

    import OSC_stream_tryout

    logs_path = OSC_stream_tryout.log_folder + '\\game.csv'
    print(logs_path)

    game_data = pd.DataFrame(columns=["TimeStamp", "correct"])
    game_data.to_csv(logs_path, index=False)

    switch_f()


    done = False
    switch = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_SPACE:
                    switch_f()
            elif event.type == pygame.QUIT:
                done = True
            for btn in [btn1, btn2, btn3, btn4, btn5, btn6]:
                btn.get_event(event)

        if len(selected_items) != old_len_selected_items:
            change_selection_visualisation()

        if len(selected_items) == 3:
            true_answer = check_answer()
            store_answer(true_answer)
            switch_f()

        old_len_selected_items = len(selected_items)

        # draw etc...
        pygame.display.update()


if __name__ == "__main__":
    main_gui()