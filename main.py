from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP

import sudoku

reserve = 20
side = 50
width = reserve * 2 + side * 9
height = reserve * 2 + side * 9

# Создаем пользовательский интерфейс для игры
class sudokugui(Frame):

    def __init__(self, parent, completeboard, board):
        self.endboard = completeboard
        self.board = board
        self.parent = parent
        Frame.__init__(self, parent)
        self.row = 0
        self.col = 0
        self.__initUI()

    def __initUI(self):
        self.parent.title("Судоку!")
        self.difficulty = "Базовый"
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=width, height=height, bg='#fbfaff')
        self.canvas.pack(fill=BOTH, side=TOP)

        newGameButton = Button(self, text="Новая игра", width=10, height=1, command=self.new_game)
        newGameButton.place(x=20, y=500)
        easyButton = Button(self, text="Базовый", width=10, height=1, command=self.easy_game)
        easyButton.place(x=120, y=500)
        mediumButton = Button(self, text="Повышенный", width=11, height=1, command=self.medium_game)
        mediumButton.place(x=220, y=500)
        hardButton = Button(self, text="Высокий", width=10, height=1, command=self.hard_game)
        hardButton.place(x=325, y=500)

        self.draw_grid()
        self.draw_numbers()

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)
    # Рисуем сетку
    def draw_grid(self):
        for i in range(10):
            color = "#582eff" if i % 3 == 0 else "#a994ff"

            x0 = reserve + i * side
            y0 = reserve
            x1 = reserve + i * side
            y1 = height - reserve
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = reserve
            y0 = reserve + i * side
            x1 = width - reserve
            y1 = reserve + i * side
            self.canvas.create_line(x0, y0, x1, y1, fill=color)
    # Определение верности введенного числа
    def draw_numbers(self):
        self.canvas.delete("Числа")
        for row in range(9):
            for col in range(9):
                numberentered = self.board[row][col]
                if numberentered != 0:
                    x = reserve + col * side + side / 2
                    y = reserve + row * side + side / 2
                    answer = self.endboard[row][col]
                    color = "#000000" if answer == numberentered else "#ff335c"
                    self.canvas.create_text(x, y, text=numberentered, tags="Числа", fill=color)
    # Обозначаем функционал для кнопок
    def new_game(self):
        self.endboard = sudoku.completedSudokuBoard()
        self.board = sudoku.puzzleSudokuBoard(self.endboard, self.difficulty)
        self.canvas.delete("Победа")
        self.draw_numbers()

    def easy_game(self):
        self.endboard = sudoku.completedSudokuBoard()
        self.difficulty = "Базовый"
        self.board = sudoku.puzzleSudokuBoard(self.endboard, self.difficulty)
        self.canvas.delete("Победа")
        self.draw_numbers()

    def medium_game(self):
        self.endboard = sudoku.completedSudokuBoard()
        self.difficulty = "Повышенный"
        self.board = sudoku.puzzleSudokuBoard(self.endboard, self.difficulty)
        self.canvas.delete("Победа")
        self.draw_numbers()

    def hard_game(self):
        self.endboard = sudoku.completedSudokuBoard()
        self.difficulty = "Высокий"
        self.board = sudoku.puzzleSudokuBoard(self.endboard, self.difficulty)
        self.canvas.delete("Победа")
        self.draw_numbers()
    # Находим выбранную ячейку
    def cell_clicked(self, event):
        if self.endboard == self.board:
            self.victory_text()
            return
        x = event.x
        y = event.y
        if reserve < x < width - reserve and reserve < y < height - reserve:
            self.canvas.focus_set()
            # Находит строку и столбец из y,x координат
            row = int((y - reserve) / side)
            col = int((x - reserve) / side)
            # Отменяет выбор ячейки при перемещении
            if (row, col) == (self.row, self.col):
                self.row = -1
                self.col = -1
            else:
                self.row = row
                self.col = col

        self.draw_highlight()
    # Выделение выбранной клетки
    def draw_highlight(self):
        self.canvas.delete("Курсор")
        if self.row >= 0 and self.col >= 0:
            x0 = reserve + self.col * side + 1
            y0 = reserve + self.row * side + 1
            x1 = reserve + (self.col + 1) * side - 1
            y1 = reserve + (self.row + 1) * side - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="#b60aff", tags="Курсор"
            )

    # Передвижение по клеткам поля при помощи стрелок , ввод чисел с клавиатуры
    def key_pressed(self, event):
        if event.keysym == "Left":
            self.col -= 1
            self.draw_numbers()
            self.draw_highlight()
        elif event.keysym == "Right":
            self.col += 1
            self.draw_numbers()
            self.draw_highlight()
        elif event.keysym == "Up":
            self.row -= 1
            self.draw_numbers()
            self.draw_highlight()
        elif event.keysym == "Down":
            self.row += 1
            self.draw_numbers()
            self.draw_highlight()

        elif self.endboard == self.board:
            self.victory_text()
            return
        elif self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.board[self.row][self.col] = int(event.char)
            self.draw_numbers()
            self.draw_highlight()
            if self.endboard == self.board:
                self.victory_text()

    # Оповещение о верно завершенной игре
    def victory_text(self):
        x = y = reserve + 4 * side + side / 2
        self.canvas.create_text(
            x, y,
            text="Победа!", tags="Победа",
            fill="#b60aff", font=("Arial", 64)
        )


answerboard = sudoku.completedSudokuBoard()
puzzleboard = sudoku.puzzleSudokuBoard(answerboard, "Базовый")

root = Tk()
root.geometry("%dx%d" % (width, height + 40))

sudokugui(root, answerboard, puzzleboard)
root.mainloop()