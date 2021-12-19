import random
import copy

emptygrid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
completed = [1, 2, 3, 4, 5, 6, 7, 8, 9]


# Функционирующий вариант доски
def completedSudokuBoard():
    while True:
        board = generatePossibleSudoku()
        if checkifSudokuisvalid(board):
            break
    return board


# Создает уровень в соответствии с выбранным вариантом сложности
def puzzleSudokuBoard(grid, difficulty):
    # Свободно 30 ячеек
    if difficulty == "Базовый":
        lbound = 2200
    # Свободны более 40 ячеек
    elif difficulty == "Повышенный":
        lbound = 15000
    # Свободны более 50 ячеек
    elif difficulty == "Высокий":
        lbound = 45000
    puzzlegrid = copy.deepcopy(grid)
    puzzlescore = diffultyscore(puzzlegrid)
    tempgrid = copy.deepcopy(grid)

    while not (lbound <= puzzlescore):
        # Очищает случайную ячейку
        row = random.choice(range(9))
        col = random.choice(range(9))
        valueremoved = copy.deepcopy(tempgrid[row][col])
        tempgrid[row][col] = 0
        tempscore = diffultyscore(tempgrid)

        # Проверка решаемости головоломки при удалении определенного числа
        if backtrackingSolve(tempgrid) != 1:
            tempgrid[row][col] = valueremoved

        # Проверка при высоком уровне сложности
        if tempscore > puzzlescore:
            puzzlegrid = copy.deepcopy(tempgrid)
            puzzlescore = tempscore

    print(diffultyscore(puzzlegrid))

    return puzzlegrid


def diffultyscore(grid):
    emptycells = 0
    for row in grid:
        for column in row:
            if column == 0:
                emptycells += 1
    branchdifficulty = 0
    row = 0
    while row <= 8:
        col = 0
        while col <= 8:
            if isCellempty(grid, row, col):
                branchdifficulty = branchdifficulty + (len(possibleCandidates(grid, row, col)) - 1) ** 2
            col += 1
        row += 1
    score = branchdifficulty * 100 + emptycells
    print(emptycells)
    return score

# Если доска не рабочая - возвращает 0
def checkifSudokuisvalid(grid):
    for row in grid:
        for column in row:
            if column == 0:
                return False
    return True

# Создает игровую доску, проверяет на наличие 0
def generatePossibleSudoku():
    playgrid = copy.deepcopy(emptygrid)
    while not checkifSudokuisvalid(playgrid):
        curr_cell = fewest_candidates(playgrid)
        curr_posscand = possibleCandidates(playgrid, curr_cell[0], curr_cell[1])
        # Если ячейки не могут быть заполнены
        if len(curr_posscand) == 0:
            playgrid = copy.deepcopy(emptygrid)
        else:
            playgrid[curr_cell[0]][curr_cell[1]] = random.choice(curr_posscand)
    return playgrid


# Лист возможных значений в ячейке по столбцу
def columnCheck(board, column):
    curr_col = []
    for row in board:
        curr_col.append(row[column])
    return list(set(completed) - set(curr_col))


# Лист возможных значений в ячейке по строке
def rowCheck(board, row):
    return list(set(completed) - set(board[row]))


# Лист возможных значений в ячейке после анализа фрагмента поля
def boxCheck(board, row, column):
    curr_box = []

    if 0 <= column <= 2:
        search_col = 0
    elif 3 <= column <= 5:
        search_col = 3
    elif 6 <= column <= 8:
        search_col = 6

    if 0 <= row <= 2:
        search_row = 0
    elif 3 <= row <= 5:
        search_row = 3
    elif 6 <= row <= 8:
        search_row = 6

    counter = 3
    while counter > 0:
        curr_box.append(board[search_row][search_col])
        curr_box.append(board[search_row][search_col + 1])
        curr_box.append(board[search_row][search_col + 2])
        search_row += 1
        counter -= 1

    return list(set(completed) - set(curr_box))


# Лист возможных значений в ячейке по итогам анализа столбца, строки и поля
def possibleCandidates(board, row, column):
    columncand = columnCheck(board, column)
    rowcand = rowCheck(board, row)
    boxcand = boxCheck(board, row, column)
    return list(set(boxcand) & set(list(set(columncand) & set(rowcand))))


# Анализирует подходящие в ячейку числа
# Если количество кандидатов в нескольких ячейках воспадает, возвращает самую верхнюю и левую ячейку
def fewest_candidates(board):
    ans_row = 0
    ans_col = 0
    least_candidates = 9
    curr_row = 0
    for row in board:
        curr_col = 0
        for column in row:
            if isCellempty(board, curr_row, curr_col) == False:
                curr_col += 1
                continue
            curr_cands = len(possibleCandidates(board, curr_row, curr_col))
            if 0 <= curr_cands < least_candidates:
                ans_row = curr_row
                ans_col = curr_col
                least_candidates = curr_cands
            curr_col += 1
        curr_row += 1
    return [ans_row, ans_col]


def isCellempty(board, row, column):
    if board[row][column] == 0:
        return True
    return False

# Возвращает имеющиеся решения на доску
def backtrackingSolve(board):
    numsols = 0
    empty = findEmptyCell(board)
    if empty == []:
        return 1
    row = empty[0]
    col = empty[1]
    for plug in range(1, 10):
        if acceptableAnswer(board, plug, row, col):
            board[row][col] = plug
            numsols += backtrackingSolve(board)
            board[row][col] = 0
    return numsols


def findEmptyCell(board):
    row_count = 0
    for row in board:
        col_count = 0
        for col in row:
            if col == 0:
                return [row_count, col_count]
            col_count += 1
        row_count += 1
    return []


def acceptableAnswer(board, answer, row, column):
    poss = possibleCandidates(board, row, column)
    if answer in poss:
        return True
    return False


testgrid1 = [
    [0, 8, 0, 0, 0, 9, 7, 4, 3],
    [0, 5, 0, 0, 0, 8, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 0, 8, 0, 4, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 0, 0, 7, 0],
    [0, 3, 0, 5, 0, 0, 0, 8, 0],
    [9, 7, 2, 4, 0, 0, 0, 5, 0]
]

testgrid2 = [
    [2, 8, 6, 1, 5, 9, 7, 4, 3],
    [3, 5, 7, 6, 4, 8, 2, 1, 9],
    [4, 1, 9, 7, 0, 0, 5, 6, 8],
    [8, 2, 1, 9, 6, 5, 4, 3, 7],
    [6, 9, 3, 8, 7, 4, 1, 2, 5],
    [7, 4, 5, 3, 0, 0, 8, 9, 6],
    [5, 6, 8, 2, 0, 0, 9, 7, 4],
    [1, 3, 4, 5, 9, 7, 6, 8, 2],
    [9, 7, 2, 4, 8, 6, 3, 5, 1]
]