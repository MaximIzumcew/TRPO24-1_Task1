class Board:
    """Класс, представляющий шахматную доску и управляющий ходами."""

    def __init__(self):
        """Инициализация доски и выбор режима игры."""
        a = int(input('Выберите режим игры: 1. Обычные шахматы 2. Модифицированная версия 3. Шашки - '))
        if a == 1:
            self.board = [
                ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
            ]
        elif a == 3:
            self.board = [
                ['.', 'c', '.', 'c', '.', 'c', '.', 'c'],
                ['c', '.', 'c', '.', 'c', '.', 'c', '.'],
                ['.', 'c', '.', 'c', '.', 'c', '.', 'c'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['O', '.', 'C', '.', 'C', '.', 'C', '.'],
                ['.', 'C', '.', 'C', '.', 'C', '.', 'C'],
                ['C', '.', 'C', '.', 'C', '.', 'C', '.']
            ]
        else:
            self.board = [
                ['r', 'n', 'd', 'q', 'k', 'b', 'n', 'r'],
                ['d', 'd', 'd', 'p', 'p', 'd', 'd', 'd'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['S', 'F', 'P', 'P', 'P', 'P', 'F', 'S'],
                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
            ]
        self.move_history = []
        self.redo_history = []

    def print_board(self, highlight=[]):
        """Печать доски с возможностью выделения клеток.

        Args:
            highlight (list): Список координат клеток для выделения.
        """
        print("    a b c d e f g h")
        print()
        for i in range(8):
            print(8 - i, end='   ')
            for j in range(8):
                if (i, j) in highlight:
                    print(f"\033[91m{self.board[i][j]}\033[0m", end=' ')
                else:
                    print(self.board[i][j], end=' ')
            print('  ', 8 - i)
        print()
        print("    a b c d e f g h")
        print('-----------------------------')

    def parse_position(self, pos):
        """Преобразование шахматной нотации в координаты доски.

        Args:
            pos (str): Позиция в шахматной нотации (например, "e2").

        Returns:
            tuple: Координаты (строка, столбец).
        """
        col = ord(pos[0]) - ord('a')
        row = 8 - int(pos[1])
        return row, col

    def make_move(self, start, end):
        """Выполнение хода на доске.

        Args:
            start (str): Начальная позиция в шахматной нотации.
            end (str): Конечная позиция в шахматной нотации.
        """
        start_row, start_col = self.parse_position(start)
        end_row, end_col = self.parse_position(end)
        piece = self.board[start_row][start_col]
        target_piece = self.board[end_row][end_col]

        if piece.lower() == 'f' and target_piece != '.':
            self.board[end_row][end_col] = '.'
            self.board[start_row][start_col] = '.'
            self.move_history.append((start, end, piece, target_piece))
            return

        if target_piece.lower() == 'f':
            self.board[end_row][end_col] = '.'
            self.board[start_row][start_col] = '.'
            self.move_history.append((start, end, piece, target_piece))
            return

        if piece.lower() in ['c', 'o']:  # Шашка или дамка
            if abs(start_row - end_row) == abs(start_col - end_col):  # Диагональный ход
                row_step = 1 if end_row > start_row else -1
                col_step = 1 if end_col > start_col else -1
                row, col = start_row + row_step, start_col + col_step
                while row != end_row:
                    if self.board[row][col] != '.' and self.board[row][col].islower() != piece.islower():
                        self.board[row][col] = '.'  # Удаляем фигуру противника
                    row += row_step
                    col += col_step

        self.move_history.append((start, end, piece, target_piece))
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = '.'
        if piece.lower() == 'c':  # Если это шашка
            self.promote_to_king(end_row, end_col, piece)

    def promote_to_king(self, row, col, piece):
        """Превращение шашки в дамку при достижении последней горизонтали.

        Args:
            row (int): Строка, на которой находится шашка.
            col (int): Столбец, на котором находится шашка.
        """
        print(f"Проверка превращения: piece={piece}, row={row}, col={col}")  # Отладочный вывод
        if piece == 'C' and row == 0:  # Черная шашка на последней горизонтали белых
            self.board[row][col] = 'O'  # Превращаем в черную дамку
            print(f"Шашка на {chr(col + ord('a'))}{8 - row} превратилась в дамку ('O')!")
        elif piece == 'c' and row == 7:  # Белая шашка на последней горизонтали черных
            self.board[row][col] = 'o'  # Превращаем в белую дамку
            print(f"Шашка на {chr(col + ord('a'))}{8 - row} превратилась в дамку ('o')!")

    def undo_move(self):
        """Отмена последнего хода."""
        if self.move_history:
            start, end, piece, captured_piece = self.move_history.pop()
            start_row, start_col = self.parse_position(start)
            end_row, end_col = self.parse_position(end)
            self.board[start_row][start_col] = piece
            self.board[end_row][end_col] = captured_piece
            self.redo_history.append((start, end, piece, captured_piece))

    def redo_move(self):
        """Повтор последнего отмененного хода."""
        if self.redo_history:
            start, end, piece, captured_piece = self.redo_history.pop()
            start_row, start_col = self.parse_position(start)
            end_row, end_col = self.parse_position(end)
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = '.'
            self.move_history.append((start, end, piece, captured_piece))

    def save_game(self, filename):
        """Сохранение текущей партии в файл.

        Args:
            filename (str): Имя файла для сохранения.
        """
        with open(filename, 'w') as file:
            for move in self.move_history:
                start, end, piece, captured_piece = move
                start_row, start_col = self.parse_position(start)
                end_row, end_col = self.parse_position(end)
                start_pos = f"{chr(start_col + ord('a'))}{8 - start_row}"
                end_pos = f"{chr(end_col + ord('a'))}{8 - end_row}"
                full_notation = f"{piece}{start_pos}{end_pos}"
                file.write(f"{full_notation}\n")
        print(f"Партия сохранена в файл {filename}")

    def load_game(self, filename):
        """Загрузка партии из файла.

        Args:
            filename (str): Имя файла для загрузки.
        """
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.move_history = []
        self.redo_history = []
        with open(filename, 'r') as file:
            for line in file:
                move = line.strip()
                piece = move[0]
                start_pos = move[1:3]
                end_pos = move[3:5]
                self.make_move(start_pos, end_pos)
        print(f"Партия загружена из файла {filename}")


class Piece:
    """Базовый класс для всех шахматных фигур."""

    def __init__(self, board, color):
        """Инициализация фигуры.

        Args:
            board (Board): Объект доски.
            color (str): Цвет фигуры ("white" или "black").
        """
        self.board = board
        self.color = color

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка допустимости хода.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def get_possible_moves(self, row, col):
        """Получение всех возможных ходов для фигуры.

        Args:
            row (int): Строка фигуры.
            col (int): Столбец фигуры.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        raise NotImplementedError("Subclasses should implement this method")


class Pawn(Piece):
    """Класс, представляющий пешку."""

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка допустимости хода для пешки.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        direction = -1 if self.color == 'black' else 1
        if start_col == end_col:
            if start_row + direction == end_row and self.board.board[end_row][end_col] == '.':
                return True
            if (start_row == 6 and self.color == 'black') or (start_row == 1 and self.color == 'white'):
                if start_row + 2 * direction == end_row and self.board.board[end_row][end_col] == '.' and self.board.board[start_row + direction][start_col] == '.':
                    return True
        elif abs(start_col - end_col) == 1 and start_row + direction == end_row:
            if self.board.board[end_row][end_col] != '.' and self.board.board[end_row][end_col].islower() != (self.color == 'white'):
                return True
        return False

    def get_possible_moves(self, row, col):
        """Получение всех возможных ходов для пешки.

        Args:
            row (int): Строка пешки.
            col (int): Столбец пешки.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        moves = []
        direction = -1 if self.color == 'black' else 1
        if 0 <= row + direction < 8 and self.board.board[row + direction][col] == '.':
            moves.append(f"{chr(col + ord('a'))}{8 - (row + direction)}")
        if (row == 6 and self.color == 'black') or (row == 1 and self.color == 'white'):
            if 0 <= row + 2 * direction < 8 and self.board.board[row + 2 * direction][col] == '.' and self.board.board[row + direction][col] == '.':
                moves.append(f"{chr(col + ord('a'))}{8 - (row + 2 * direction)}")
        for dc in [-1, 1]:
            if 0 <= col + dc < 8 and 0 <= row + direction < 8:
                target_piece = self.board.board[row + direction][col + dc]
                if target_piece != '.' and target_piece.islower() != (self.color == 'white'):
                    moves.append(f"{chr(col + dc + ord('a'))}{8 - (row + direction)}")
        return moves


class Rook(Piece):
    """Класс, представляющий ладью."""

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка допустимости хода для ладьи.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        if start_row == end_row:
            for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                if self.board.board[start_row][col] != '.':
                    return False
            return self.board.board[end_row][end_col] == '.' or self.board.board[end_row][end_col].islower() != (self.color == 'white')
        elif start_col == end_col:
            for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                if self.board.board[row][start_col] != '.':
                    return False
            return self.board.board[end_row][end_col] == '.' or self.board.board[end_row][end_col].islower() != (self.color == 'white')
        return False

    def get_possible_moves(self, row, col):
        """Получение всех возможных ходов для ладьи.

        Args:
            row (int): Строка ладьи.
            col (int): Столбец ладьи.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        moves = []
        for i in range(row - 1, -1, -1):
            if self.board.board[i][col] == '.':
                moves.append(f"{chr(col + ord('a'))}{8 - i}")
            else:
                if self.board.board[i][col].islower() != (self.color == 'white'):
                    moves.append(f"{chr(col + ord('a'))}{8 - i}")
                break
        for i in range(row + 1, 8):
            if self.board.board[i][col] == '.':
                moves.append(f"{chr(col + ord('a'))}{8 - i}")
            else:
                if self.board.board[i][col].islower() != (self.color == 'white'):
                    moves.append(f"{chr(col + ord('a'))}{8 - i}")
                break
        for j in range(col - 1, -1, -1):
            if self.board.board[row][j] == '.':
                moves.append(f"{chr(j + ord('a'))}{8 - row}")
            else:
                if self.board.board[row][j].islower() != (self.color == 'white'):
                    moves.append(f"{chr(j + ord('a'))}{8 - row}")
                break
        for j in range(col + 1, 8):
            if self.board.board[row][j] == '.':
                moves.append(f"{chr(j + ord('a'))}{8 - row}")
            else:
                if self.board.board[row][j].islower() != (self.color == 'white'):
                    moves.append(f"{chr(j + ord('a'))}{8 - row}")
                break
        return moves


class Knight(Piece):
    """Класс, представляющий коня."""

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка допустимости хода для коня.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return self.board.board[end_row][end_col] == '.' or self.board.board[end_row][end_col].islower() != (self.color == 'white')
        return False

    def get_possible_moves(self, row, col):
        """Получение всех возможных ходов для коня.

        Args:
            row (int): Строка коня.
            col (int): Столбец коня.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        moves = []
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in knight_moves:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board.board[new_row][new_col] == '.' or self.board.board[new_row][new_col].islower() != (self.color == 'white'):
                    moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
        return moves


class Bishop(Piece):
    """Класс, представляющий слона."""

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка допустимости хода для слона.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        if abs(start_row - end_row) == abs(start_col - end_col):
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            row, col = start_row + row_step, start_col + col_step
            while row != end_row:
                if self.board.board[row][col] != '.':
                    return False
                row += row_step
                col += col_step
            return self.board.board[end_row][end_col] == '.' or self.board.board[end_row][end_col].islower() != (self.color == 'white')
        return False

    def get_possible_moves(self, row, col):
        """Получение всех возможных ходов для слона.

        Args:
            row (int): Строка слона.
            col (int): Столбец слона.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        moves = []
        for i in range(1, 8):
            if row + i < 8 and col + i < 8:
                if self.board.board[row + i][col + i] == '.':
                    moves.append(f"{chr(col + i + ord('a'))}{8 - (row + i)}")
                else:
                    if self.board.board[row + i][col + i].islower() != (self.color == 'white'):
                        moves.append(f"{chr(col + i + ord('a'))}{8 - (row + i)}")
                    break
        for i in range(1, 8):
            if row + i < 8 and col - i >= 0:
                if self.board.board[row + i][col - i] == '.':
                    moves.append(f"{chr(col - i + ord('a'))}{8 - (row + i)}")
                else:
                    if self.board.board[row + i][col - i].islower() != (self.color == 'white'):
                        moves.append(f"{chr(col - i + ord('a'))}{8 - (row + i)}")
                    break
        for i in range(1, 8):
            if row - i >= 0 and col + i < 8:
                if self.board.board[row - i][col + i] == '.':
                    moves.append(f"{chr(col + i + ord('a'))}{8 - (row - i)}")
                else:
                    if self.board.board[row - i][col + i].islower() != (self.color == 'white'):
                        moves.append(f"{chr(col + i + ord('a'))}{8 - (row - i)}")
                    break
        for i in range(1, 8):
            if row - i >= 0 and col - i >= 0:
                if self.board.board[row - i][col - i] == '.':
                    moves.append(f"{chr(col - i + ord('a'))}{8 - (row - i)}")
                else:
                    if self.board.board[row - i][col - i].islower() != (self.color == 'white'):
                        moves.append(f"{chr(col - i + ord('a'))}{8 - (row - i)}")
                    break
        return moves


class Queen(Piece):
    """Класс, представляющий ферзя."""

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка допустимости хода для ферзя.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        return Rook.is_valid_move(self, start_row, start_col, end_row, end_col) or Bishop.is_valid_move(self, start_row, start_col, end_row, end_col)

    def get_possible_moves(self, row, col):
        """Получение всех возможных ходов для ферзя.

        Args:
            row (int): Строка ферзя.
            col (int): Столбец ферзя.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        return Rook.get_possible_moves(self, row, col) + Bishop.get_possible_moves(self, row, col)


class King(Piece):
    """Класс, представляющий короля."""

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка допустимости хода для короля.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return self.board.board[end_row][end_col] == '.' or self.board.board[end_row][end_col].islower() != (self.color == 'white')
        return False

    def get_possible_moves(self, row, col):
        """Получение всех возможных ходов для короля.

        Args:
            row (int): Строка короля.
            col (int): Столбец короля.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board.board[new_row][new_col] == '.' or self.board.board[new_row][new_col].islower() != (self.color == 'white'):
                        moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
        return moves


class FireGolem(Piece):
    """Класс, представляющий огненного голема."""

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка допустимости хода для огненного голема.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        if start_row != end_row and start_col != end_col:
            return False

        if abs(start_row - end_row) > 3 or abs(start_col - end_col) > 3:
            return False

        if start_row == end_row:  
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if self.board.board[start_row][col] != '.':
                    return False
        else: 
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if self.board.board[row][start_col] != '.':
                    return False

        target_piece = self.board.board[end_row][end_col]
        return target_piece == '.' or target_piece.islower() != (self.color == 'white')

    def get_possible_moves(self, row, col):
        """Получение всех возможных ходов для огненного голема.

        Args:
            row (int): Строка голема.
            col (int): Столбец голема.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

        for dr, dc in directions:
            for step in range(1, 4): 
                new_row, new_col = row + dr * step, col + dc * step
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board.board[new_row][new_col] == '.':
                        moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
                    else:
                        if self.board.board[new_row][new_col].islower() != (self.color == 'white'):
                            moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
                        break  
                else:
                    break 
        return moves
    def explode(self, row, col):
        """Уничтожение фигуры, которая взяла огненного голема.

        Args:
            row (int): Строка голема.
            col (int): Столбец голема.
        """
        self.board.board[row][col] = '.'


class Dragon(Piece):
    """Класс, представляющий дракона."""

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка допустимости хода для дракона.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            return self.board.board[end_row][end_col] == '.' or self.board.board[end_row][end_col].islower() != (self.color == 'white')
        elif start_col == end_col:
            step = 1 if end_row > start_row else -1
            return self.board.board[end_row][end_col] == '.' or self.board.board[end_row][end_col].islower() != (self.color == 'white')
        elif abs(start_row - end_row) == abs(start_col - end_col):
            return self.board.board[end_row][end_col] == '.' or self.board.board[end_row][end_col].islower() != (self.color == 'white')
        return False

    def get_possible_moves(self, row, col):
        """Получение всех возможных ходов для дракона.

        Args:
            row (int): Строка дракона.
            col (int): Столбец дракона.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            for step in range(1, 4):
                new_row, new_col = row + dr * step, col + dc * step
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board.board[new_row][new_col] == '.':
                        moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
                    else:
                        if self.board.board[new_row][new_col].islower() != (self.color == 'white'):
                            moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
                        break
                else:
                    break
        return moves


class Spearman(Piece):
    """Класс, представляющий копейщика."""

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка допустимости хода для копейщика.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 0:
            return self.board.board[end_row][end_col] == '.' or self.board.board[end_row][end_col].islower() != (self.color == 'white')
        if abs(start_col - end_col) == 2 and abs(start_row - end_row) == 0:
            return self.board.board[end_row][end_col] == '.' or self.board.board[end_row][end_col].islower() != (self.color == 'white')
        if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
            return self.board.board[end_row][end_col] == '.' or self.board.board[end_row][end_col].islower() != (self.color == 'white')
        return False

    def get_possible_moves(self, row, col):
        """Получение всех возможных ходов для копейщика.

        Args:
            row (int): Строка копейщика.
            col (int): Столбец копейщика.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        moves = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board.board[new_row][new_col] == '.' or self.board.board[new_row][new_col].islower() != (self.color == 'white'):
                    moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
        return moves


class Checker(Piece):
    """Класс, представляющий шашку."""

    def __init__(self, board, color):
        super().__init__(board, color)
        self.is_king = False 

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка допустимости хода для шашки.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        direction = -1 if self.color == 'white' else 1
        if not self.is_king:
            if (end_row - start_row) * direction >= 0:
                return False

        if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1:
            if self.board.board[end_row][end_col] == '.':
                return True
        elif abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            if self.board.board[middle_row][middle_col].islower() != (self.color == 'white'):
                if self.board.board[end_row][end_col] == '.':
                    return True
        return False

    def get_possible_moves(self, row, col):
        """Получение всех возможных ходов для шашки.

        Args:
            row (int): Строка шашки.
            col (int): Столбец шашки.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        moves = []
        direction = -1 if self.color == 'white' else 1

        for dr in [-1, 1]:
            for dc in [-1, 1]:
                new_row, new_col = row + dr * direction, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board.board[new_row][new_col] == '.':
                        moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
                    elif self.board.board[new_row][new_col].islower() != (self.color == 'white'):
                        jump_row = new_row + dr * direction
                        jump_col = new_col + dc
                        if 0 <= jump_row < 8 and 0 <= jump_col < 8:
                            if self.board.board[jump_row][jump_col] == '.':
                                moves.append(f"{chr(jump_col + ord('a'))}{8 - jump_row}")
        return moves

    def promote_to_king(self, row):
        """Превращение шашки в дамку.

        Args:
            row (int): Строка, на которой находится шашка.

        Returns:
            KingChecker: Возвращает объект KingChecker, если шашка превращается в дамку.
        """
        if (self.color == 'white' and row == 0) or (self.color == 'black' and row == 7):
            self.is_king = True
            return KingChecker(self.board, self.color)
        return None


class KingChecker(Piece):
    """Класс, представляющий дамку."""

    def __init__(self, board, color):
        super().__init__(board, color)

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """Проверка допустимости хода для дамки.

        Args:
            start_row (int): Начальная строка.
            start_col (int): Начальный столбец.
            end_row (int): Конечная строка.
            end_col (int): Конечный столбец.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1

        row, col = start_row + row_step, start_col + col_step
        opponent_found = None

        while row != end_row:
            if self.board.board[row][col] != '.':
                if opponent_found is not None:
                    return False
                if self.board.board[row][col].islower() != (self.color == 'white'):
                    opponent_found = (row, col)
                else:
                    return False
            row += row_step
            col += col_step

        if self.board.board[end_row][end_col] != '.':
            return False

        return True

    def get_possible_moves(self, row, col):
        """Получение всех возможных ходов для дамки.

        Args:
            row (int): Строка дамки.
            col (int): Столбец дамки.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            for step in range(1, 8):
                new_row, new_col = row + dr * step, col + dc * step
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board.board[new_row][new_col] == '.':
                        moves.append(f"{chr(new_col + ord('a'))}{8 - new_row}")
                    else:
                        if self.board.board[new_row][new_col].islower() != (self.color == 'white'):
                            jump_row = new_row + dr
                            jump_col = new_col + dc
                            if 0 <= jump_row < 8 and 0 <= jump_col < 8:
                                if self.board.board[jump_row][jump_col] == '.':
                                    moves.append(f"{chr(jump_col + ord('a'))}{8 - jump_row}")
                        break
                else:
                    break
        return moves


class Game:
    """Класс, представляющий игру."""

    def __init__(self):
        """Инициализация игры."""
        self.board = Board()
        self.turn = 'white'
        self.move_count = 0
        self.pieces = {
            'p': Pawn(self.board, 'white'),
            'P': Pawn(self.board, 'black'),
            'r': Rook(self.board, 'white'),
            'R': Rook(self.board, 'black'),
            'n': Knight(self.board, 'white'),
            'N': Knight(self.board, 'black'),
            'b': Bishop(self.board, 'white'),
            'B': Bishop(self.board, 'black'),
            'q': Queen(self.board, 'white'),
            'Q': Queen(self.board, 'black'),
            'k': King(self.board, 'white'),
            'K': King(self.board, 'black'),
            's': Spearman(self.board, 'white'),
            'S': Spearman(self.board, 'black'),
            'd': Dragon(self.board, 'white'),
            'D': Dragon(self.board, 'black'),
            'f': FireGolem(self.board, 'white'),
            'F': FireGolem(self.board, 'black'),
            'C': Checker(self.board, 'black'),
            'c': Checker(self.board, 'white'),
            'O': KingChecker(self.board, 'black'),
            'o': KingChecker(self.board, 'white')
        }

    def is_valid_move(self, start, end):
        """Проверка допустимости хода.

        Args:
            start (str): Начальная позиция в шахматной нотации.
            end (str): Конечная позиция в шахматной нотации.

        Returns:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = self.board.parse_position(start)
        end_row, end_col = self.board.parse_position(end)
        piece = self.board.board[start_row][start_col]
        if piece == '.':
            return False
        if piece in self.pieces:
            return self.pieces[piece].is_valid_move(start_row, start_col, end_row, end_col)
        return False

    def get_possible_moves(self, pos):
        """Получение всех возможных ходов для фигуры.

        Args:
            pos (str): Позиция фигуры в шахматной нотации.

        Returns:
            list: Список возможных ходов в шахматной нотации.
        """
        row, col = self.board.parse_position(pos)
        piece = self.board.board[row][col]
        if piece in self.pieces:
            return self.pieces[piece].get_possible_moves(row, col)
        return []

    def hint(self, pos):
        """Подсказка возможных ходов для фигуры.

        Args:
            pos (str): Позиция фигуры в шахматной нотации.
        """
        moves = self.get_possible_moves(pos)
        highlight = []
        for move in moves:
            row, col = self.board.parse_position(move)
            highlight.append((row, col))
        self.board.print_board(highlight)

    def threats(self, pos):
        """Проверка угроз для фигуры.

        Args:
            pos (str): Позиция фигуры в шахматной нотации.
        """
        row, col = self.board.parse_position(pos)
        threats = []
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                if piece != '.' and piece.islower() != self.board.board[row][col].islower():
                    moves = self.get_possible_moves(f"{chr(j + ord('a'))}{8 - i}")
                    for move in moves:
                        move_row, move_col = self.board.parse_position(move)
                        if move_row == row and move_col == col:
                            threats.append((i, j))
        self.board.print_board(threats)
        if threats:
            print(f"Фигура на позиции {pos} находится под угрозой от следующих фигур:")
            for threat in threats:
                print(f"{self.board.board[threat[0]][threat[1]]} на {chr(threat[1] + ord('a'))}{8 - threat[0]}")
        else:
            print(f"Фигура на позиции {pos} не находится под угрозой.")
        self.is_check('white' if self.board.board[row][col].isupper() else 'black')

    def is_check(self, color):
        """Проверка, находится ли король под шахом.

        Args:
            color (str): Цвет короля ("white" или "black").
        """
        threats = []
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] == 'k':
                    black_king_pos = (i, j)
                elif self.board.board[i][j] == 'K':
                    white_king_pos = (i, j)
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                if piece.islower():
                    moves = self.get_possible_moves(f"{chr(j + ord('a'))}{8 - i}")
                    for move in moves:
                        move_row, move_col = self.board.parse_position(move)
                        if move_row == white_king_pos[0] and move_col == white_king_pos[1]:
                            threats.append((i, j))
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                if piece.isupper():
                    moves = self.get_possible_moves(f"{chr(j + ord('a'))}{8 - i}")
                    for move in moves:
                        move_row, move_col = self.board.parse_position(move)
                        if move_row == black_king_pos[0] and move_col == black_king_pos[1]:
                            threats.append((i, j))
        if threats and color == 'white':
            print("Король белых находится под шахом!")
        elif threats and color == 'black':
            print("Король черных находится под шахом!")
        else:
            print("Шаха нет.")

    def main(self):
        """Основной цикл игры."""
        while True:
            self.board.print_board()
            print(f"Ход {self.turn.capitalize()}. Введите ход (например, e2 e4) или команду (undo, redo, hint, threats, save, load, exit):")
            command = input().strip().lower()
            if command == 'exit':
                break
            elif command == 'undo':
                self.board.undo_move()
                self.move_count -= 1
                self.turn = 'black' if self.turn == 'white' else 'white'
            elif command == 'redo':
                self.board.redo_move()
                self.move_count += 1
                self.turn = 'black' if self.turn == 'white' else 'white'
            elif command.startswith('hint'):
                pos = command.split()[1]
                self.hint(pos)
            elif command.startswith('threats'):
                pos = command.split()[1]
                self.threats(pos)
            elif command.startswith('save'):
                filename = command.split()[1]
                self.board.save_game(filename)
            elif command.startswith('load'):
                filename = command.split()[1]
                self.board.load_game(filename)
            else:
                try:
                    start, end = command.split()
                    start_row, start_col = self.board.parse_position(start)
                    piece = self.board.board[start_row][start_col]
                    if (self.turn == 'white' and piece.islower()) or (self.turn == 'black' and piece.isupper()):
                        print("Неверный ход. Нельзя трогать фигуры противника.")
                        continue
                    if self.is_valid_move(start, end):
                        end_row, end_col = self.board.parse_position(end)
                        if self.board.board[end_row][end_col] == 'k':
                            print("Черный король повержен! Белые победили!")
                            print("Количество ходов - ", self.move_count + 1)
                            break
                        elif self.board.board[end_row][end_col] == 'K':
                            print("Белый король повержен! Черные победили!")
                            print("Количество ходов - ", self.move_count + 1)
                            break
                        self.board.make_move(start, end)
                        self.move_count += 1
                        self.turn = 'black' if self.turn == 'white' else 'white'
                        self.board.redo_history.clear()
                    else:
                        print("Неверный ход. Попробуйте еще раз.")
                except ValueError:
                    print("Неверный формат команды. Попробуйте еще раз.")


if __name__ == "__main__":
    game = Game()
    game.main()