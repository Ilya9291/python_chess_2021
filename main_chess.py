import pygame
from pprint import pprint


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.board = [[0] * width for _ in range(height)]

        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 55

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    #  возвращает координаты клетки в виде кортежа по переданным координатам мыши
    def get_cell(self, mouse_pos):
        for i in range(self.height):
            for j in range(self.width):
                if (
                        self.left + self.cell_size * j < mouse_pos[0] < self.left + self.cell_size * j + self.cell_size
                        and
                        self.top + self.cell_size * i < mouse_pos[1] < self.top + self.cell_size * i + self.cell_size
                ):
                    return i, j
        return None


class Chess(Board):
    def __init__(self):
        super(Chess, self).__init__(8, 8)  # создание доски 8 на 8
        # расстановка фигур:
        # пешки:
        for i in range(8):
            self.board[1][i] = Pawn(1, i, False)  # чёрная пешка
            self.board[6][i] = Pawn(6, i, True)  # белая пешка
        '''
        # ладьи:
        self.board[0][0] = Rook(0, 0, False)
        self.board[0][7] = Rook(0, 7, False)
        self.board[7][0] = Rook(7, 0, True)
        self.board[7][7] = Rook(7, 7, True)
        # кони:
        self.board[0][1] = Horse(0, 1, False)
        self.board[0][6] = Horse(0, 6, False)
        self.board[7][1] = Horse(7, 1, True)
        self.board[7][6] = Horse(7, 6, True)
        # слоны:
        self.board[0][2] = Bishop(0, 2, False)
        self.board[0][5] = Bishop(0, 5, False)
        self.board[7][2] = Bishop(7, 2, True)
        self.board[7][5] = Bishop(7, 5, True)
        # ферзи:
        self.board[0][3] = Queen(0, 3, False)
        self.board[7][3] = Queen(7, 3, True)
        # короли:
        self.board[0][4] = King(0, 4, False)
        self.board[7][4] = King(7, 4, True)
        '''

        self.step = True  # True означает белый цвет хода
        self.eaten_pieces = []  # листок, который хранит съеденные фигуры

    # отрисовка доски
    def render(self, input_screen):
        input_screen.fill((0, 0, 0))  # очистка экрана
        for i in range(self.height):
            for j in range(self.width):
                # отрисовка фоноваго квадрата
                if (i + j) % 2 == 0:  # светлый квадрат
                    pygame.draw.rect(input_screen, pygame.Color('#99958C'),
                                     pygame.Rect(self.left + self.cell_size * j,
                                                 self.top + self.cell_size * i, self.cell_size,
                                                 self.cell_size), 0)
                else:  # тёмный квадрат
                    pygame.draw.rect(input_screen, pygame.Color('#474A51'),
                                     pygame.Rect(self.left + self.cell_size * j,
                                                 self.top + self.cell_size * i, self.cell_size,
                                                 self.cell_size), 0)
                #  отрисовка фигур
                if bool(self.board[i][j]) is not False:
                    self.board[i][j].render(input_screen)

    def on_click(self, y, x, screen_of_click):  # обработчик действий на поле
        print(y, x)
        if bool(self.board[y][x]):  # если нажатие произошло на фигуру
            if self.step == self.board[y][x].color:  # можно ходить только в свой ход(проверка на цвет фигуры = хода)
                self.render(screen_of_click)  # отривоска самой доски и фигур

                steps_field = self.board[y][x].possible_steps_field()  # получение всех возможный ходов фигуры
                for i in range(8):
                    for j in range(8):
                        if bool(steps_field[i][j]):  # если ход возможен в координату
                            #  отрисовка зелёной окружности
                            pygame.draw.circle(screen_of_click, pygame.Color('Green'),
                                               (self.left + self.cell_size * j + self.cell_size // 2,
                                                self.top + self.cell_size * i + self.cell_size // 2),
                                               self.cell_size // 2 - 2, 3)

                # вылавливание второго нажатия на поле для выбора конечной координаты хода
                step_y, step_x = 10, 10  # неправильные значения хода(если вылетит с этим, то проблемма в цикле)
                local_clock = pygame.time.Clock()
                local_running = True
                while local_running:
                    for local_event in pygame.event.get():
                        if local_event.type == pygame.QUIT:
                            pygame.quit()

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if local_event.button == 1:
                                step_y, step_x = board.get_cell(local_event.pos)  # координаты хода
                                local_running = False  # выход из цикла
                    local_clock.tick(60)

                if step_y != y and step_x != x:  # нельзя сходить в клетку старта
                    if bool(steps_field[step_y][step_x]):  # если ход в координату возможен
                        if bool(self.board[step_y][step_x]):  # если в клетке хода есть фигура, то её нужно сьесть
                            self.eaten_pieces.append(self.board[step_y][step_x])  # съеденная фигура записана в листок
                        self.board[step_y][step_x] = self.board[y][x].copy()  # перемещение фигуры в клетку хода
                        self.step = not self.step  # смена хода


class Piece:
    def __init__(self, y, x, color=True):
        self.y, self.x = y, x  # координаты фигуры (y-сверху, x-слева-направо)
        self.color = color  # значение True означает белый цвет фигуры

    def __hash__(self):
        return hash((str(type(self).__name__), self.x, self.y))

    def __repr__(self):
        return str(type(self).__name__) + ' y:' + str(self.get_y()) + ' x:' + str(self.get_x())

    def set_new_position(self, y, x):
        self.y, self.x = y, x

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

    def get_pos(self):
        return self.get_y(), self.get_x()

    def is_it_possible_step(self, step_y, step_x):  # проверка на возможность шага(ввод- конечные координаты)
        return False

    def possible_steps_field(self):
        steps_field = []
        for y in range(8):
            line = []
            for x in range(8):
                if self.is_it_possible_step(y, x):
                    line.append(1)
                else:
                    line.append(0)
            steps_field.append(line)
        return steps_field


class Pawn(Piece):
    def __init__(self, y, x, color=True):
        super().__init__(y, x, color=color)
        self.was_moved = False

    def render(self, screen_name):  # отрисовка фигуры
        pass

    def is_it_possible_step(self, step_y, step_x):  # проверка на возможность шага(ввод- конечные координаты)
        if not self.was_moved:  # создание списка изменения y-координаты
            lst = [1, 2]
        else:
            lst = [1]
        if self.color:  # фигура белая
            if step_y - self.y in lst:  # ходит вверх на столько клеток, сколько есть в списке
                return True
        else:
            if self.y - step_y in lst:  # ходит вниз на столько клеток, сколько есть в списке
                return True
        return False


board = Chess()

pygame.init()

screen = pygame.display.set_mode((board.cell_size * board.width, board.cell_size * board.height + 50))
# + 50 по высоте - для поля со съедеными фигурами
pygame.display.set_caption('Шахматы')

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.on_click(*board.get_cell(event.pos), screen)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:  # новая игра
                board = Chess()  # сздание нового поля

    board.render(screen)

    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
