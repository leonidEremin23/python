'''
need to install pygame like:
1. Open terminal
2. Write 'pip install pygame' on it
P.S. To start a programm use some IDEs

'''

import pygame
import time
import sqlite3
import random
pygame.init()
pygame.init()
x, y = screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)
screen.fill((255, 255, 255))
con = sqlite3.connect('DIKTATOR.db')
cur = con.cursor()
reputations = [5 for _ in range(6)]
class form():
    def __init__(self):
        time.sleep(0.1)
        self.buttons = []
        self.showing = False
        self.active_button = None
        self.fct_id = {'Полиция': 1, 'Олигархи': 2, 'Армия': 3, 'Правозащитники': 4, 'Мафия': 5, 'Народ': 6}
        self.frction = None

    def show(self):
        self.showing = True
        finish_button.hide()
        screen.fill((255, 255, 255))
        self.fraction = ['Полиция', 'Олигархи', 'Армия', 'Правозащитники', 'Мафия', 'Народ']
        dy = 0

        pygame.draw.rect(screen,pygame.Color('white'), (0, 70, 500, 60), 0)
        for i in self.fraction:
            bt = button(242, 148 + dy, i, 40)
            lx, ly = bt.get_sizes()
            dy += ly
            self.buttons.append(bt)
            bt.attach(self.show_question)
    def hide(self):
        screen.fill((255, 255, 255))
    def refresh(self):
        for i in self.buttons:
            i.active()
    def show_question(self):

        screen.fill((255, 255, 255))
        for i in self.buttons:
            i.hide()
        frction = self.fct_id[self.active_button]
        query = f"SELECT question, id FROM fractions WHERE fraction = {frction}"
        question, self.idet = cur.execute(query).fetchall()[random.randint(0, 1)]
        retr = []
        actual_string = ''
        question = question.split()
        cnt = 1
        for i in question:
            actual_string += i + ' '
            if cnt % 6 == 0:
                retr.append(actual_string)
                actual_string = ''
            cnt += 1
            if cnt == len(question) + 1:
                retr.append(actual_string)
        font = pygame.font.Font(None, 20)
        cnt = 0
        dy = 0
        for i in retr:
            text = font.render(i, 1, (255, 0, 0))
            text_x = 450 // 2 - text.get_width() // 2
            text_y = 104 // 2 - text.get_height() // 2 + dy + 20
            dy += text.get_height()
            screen.blit(text, (text_x, text_y))
            cnt += 1
        self.oucorse_button = button(70, 289, 'Разрешаю', 30)
        self.oucorse_button.attach(self.agree)
        self.no_button = button(423, 290, 'Запрещаю', 30)
        self.no_button.attach(self.disagree)
        self.out_button = button(29, 26, '<-', 30)
        self.out_button.attach(self.ret)
        self.btt = [self.oucorse_button, self.no_button, self.out_button]
        self.ok = []
    def ret(self):
        screen.fill((255, 255, 255))
        for i in self.btt:
            i.hide()
        self.show()
    def agree(self):
        screen.fill((255, 255, 255))
        query = f"SELECT reaction_1, reaction_2, reaction_3, reaction_4, reaction_5," \
            f" reaction_6 FROM fractions WHERE id = {self.idet}"
        res = cur.execute(query).fetchall()[0]
        for i in range(len(reputations)):
            reputations[i] += res[i]
        for i in self.btt:
            i.hide()
        self.results()
    def disagree(self):
        screen.fill((255, 255, 255))
        query = f"SELECT reaction_1, reaction_2, reaction_3, reaction_4, reaction_5," \
            f" reaction_6 FROM fractions WHERE id = {self.idet}"
        res = cur.execute(query).fetchall()[0]
        for i in range(len(reputations)):
            reputations[i] -= res[i]
        for i in self.btt:
            i.hide()
        self.results()

    def results(self):
        self.ok.append(button(242, 431, 'ПРИНЯЛ', 30))
        self.ok[0].attach(self.check_res)
        font = pygame.font.Font(None, 40)
        cnt = 0
        dy = 0
        for i in range(len(reputations)):
            if reputations[i] <= 3 or reputations[i] > 6:
                text = font.render(f"{self.fraction[i]}:{reputations[i]}", 1, (255, 0, 0))
            elif 3 < reputations[i] <= 6:
                text = font.render(f"{self.fraction[i]}:{reputations[i]}", 1, (0, 255, 0))
            text_x = 350 // 2 - text.get_width() // 2
            text_y = 104 // 2 - text.get_height() // 2 + dy + 20
            dy += text.get_height()
            screen.blit(text, (text_x, text_y))
            cnt += 1
    def check_res(self):

        self.ok[0].hide()
        screen.fill((255, 255, 255))
        flag = True
        for i in range(len(reputations)):
            rep = reputations[i]
            if not(0 < rep < 10):
                flag = False
                traidor = self.fraction[i]
        if flag:
            self.show()
        else:
            font = pygame.font.Font(None, 20)
            text = font.render(f"ВАС ПРЕДАЛИ И СВЕРГЛИ. БУНТОВЩИКИ: {traidor}", 1, (255, 0, 0))
            text_x = 420 // 2 - text.get_width() // 2
            text_y = 188 // 2 - text.get_height() // 2
            screen.blit(text, (text_x, text_y))

class button():
    def __init__(self, x, y, txt, fnt_size):
        font = pygame.font.Font(None, fnt_size)
        text = font.render(txt, 1, (255, 0, 0))
        text_x = x - text.get_width() // 2
        text_y = y - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)
        self.x = text_x - 10
        self.y = text_y - 10
        self.finalis = (self.x + text_w + 20, self.y + text_h + 20)
        self.width = text_w + 20
        self.height = text_h + 20
        self.hide_is = True
        self.text = txt
        self.tapped = False
    def check_press(self, x, y):
        fnx, fny = self.finalis
        if self.x <= x <= fnx and self.y <= y <= fny and self.hide_is:
            self.tapped = True
            return True
    def attach(self, func):
        self.action = func

    def get_sizes(self):
        return (self.width, self.height)

    def hide(self):
        self.hide_is = False
    def active(self):
        self.hide_is = True

def out():
    pygame.quit()

def new_one():
    screen.fill((255,255,255))
    ft.show()

start_button = button(242, 75, 'НАЧАТЬ ПРАВЛЕНИЕ', 30)
start_button.attach(new_one)
finish_button = button(242, 226, 'ПОКИНУТЬ ГОС-ВО', 30)
finish_button.attach(out)
flag = False
ft = form()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                print(x, y)
                if start_button.check_press(x, y):
                    start_button.action()
                    continue
                elif finish_button.check_press(x, y):
                    finish_button.action()
                time.sleep(0.1)

                for i in ft.buttons:
                    if i.check_press(x, y):
                        ft.active_button = i.text
                        print(ft.active_button)
                        i.action()
                        continue
                time.sleep(0.1)
                for i in ft.btt:
                    if i.check_press(x, y):
                        i.action()
                        continue
                for i in ft.ok:
                    if i.check_press(x, y):
                        i.action()
                        continue
    pygame.display.flip()
pygame.quit()