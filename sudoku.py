from random import randint, shuffle
import time
import copy
import csv
import cProfile


def print_board(board):
    boardString = ""
    for i in range(9):
        for j in range(9):
            boardString += str(board[i][j]) + " "
            if (j + 1) % 3 == 0 and j != 0 and j + 1 != 9:
                boardString += "| "

            if j == 8:
                boardString += "\n"

            if j == 8 and (i + 1) % 3 == 0 and i + 1 != 9:
                boardString += "- - - - - - - - - - - \n"
    print(boardString)


def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def find_empty_greedy(board):
    empty = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:

                possible = [_ for _ in range(1,10)]
                for k in range(9):
                    if board[i][k] in possible:
                        possible.remove(board[i][k])
                for k in range(9):
                    if board[k][j] in possible:
                        possible.remove(board[k][j])
                start_i = (i // 3) * 3
                start_j = (j // 3) * 3
                for p in range(start_i,start_i+3):
                    for q in range(start_j,start_j+3):
                            if board[p][q] in possible:
                                possible.remove(board[p][q])
                empty.append([i,j,len(possible),possible])
    
    if not empty:
        return None
    sorted_list = sorted(empty, key=lambda x: x[2])
    return sorted_list[0][0] , sorted_list[0][1], sorted_list[0][3]



def valid(board, pos, num): 
    #CHECK IF VALID IN ROW
    for i in range(9):
        if board[i][pos[1]] == num: 
            return False

    #CHECK IF VALID IN COLUMN
    for j in range(9):
        if board[pos[0]][j] == num:
            return False

    #CHECK IF VALID IN THE 3X3 SUBGRID
    start_i = pos[0] - pos[0] % 3
    start_j = pos[1] - pos[1] % 3
    for i in range(3):
        for j in range(3):
            if board[start_i + i][start_j + j] == num:
                return False

    return True

def solve_greedy(board):
    #find the next empty cell in the board
    empty1,empty2,possible = find_empty_greedy(board)
    empty = [empty1,empty2]
    #if there is no empty cell in the board,the sudoku is solved
    if not empty:
        return True 

    for nums in possible:
        #for a number 1 to 9 , check if the number is valid
        if valid(board, empty, nums): 
            #BACKTRACKING
            board[empty[0]][empty[1]] = nums
            if solve(board):  # recursive step
                return True
            # this number is wrong so we set it back to 0 (backtrack)
            board[empty[0]][empty[1]] = 0

    return False


def solve(board):
    #find the next empty cell in the board
    empty = find_empty(board)

    #if there is no empty cell in the board,the sudoku is solved
    if not empty:
        return True 

    for nums in range(1, 10):
        #for a number 1 to 9 , check if the number is valid
        if valid(board, empty, nums): 
            #BACKTRACKING
            board[empty[0]][empty[1]] = nums
            if solve(board):  # recursive step
                return True
            # this number is wrong so we set it back to 0 (backtrack)
            board[empty[0]][empty[1]] = 0

    return False


def generate_board():
    board = [[0 for i in range(9)] for j in range(9)]

    # Fill the diagonal boxes
    for i in range(0, 9, 3):
        nums = list(range(1, 10))
        shuffle(nums)
        for row in range(3):
            for col in range(3):
                board[i + row][i + col] = nums.pop()

    # Fill the remaining cells with backtracking
    def fill_cells(board, row, col):
        if row == 9:
            return True
        if col == 9:
            return fill_cells(board, row + 1, 0)

        if board[row][col] != 0:
            return fill_cells(board, row, col + 1)

        for num in range(1, 10):
            if valid(board, (row, col), num):
                board[row][col] = num

                if fill_cells(board, row, col + 1):
                    return True

        board[row][col] = 0
        return False

    fill_cells(board, 0, 0)

    # Remove a greater number of cells to create a puzzle with fewer initial numbers
    for _ in range(randint(55, 65)):
        row, col = randint(0, 8), randint(0, 8)
        board[row][col] = 0

    return board

# if __name__ == "__main__":

#     seqtimes = []
#     greedytimes = []

#     for i in range(1):
#         board = generate_board()
#         board2 = copy.deepcopy(board)
#         print_board(board)
#         starttime = time.time()
#         cProfile.run("solve(board)")
#         endtime = time.time()
#         #print("Time taken : ", endtime - starttime)
#         seqtime = endtime - starttime
#         seqtimes += [seqtime]
#         print_board(board)

#         print_board(board2)
#         starttime2 = time.time()
#         cProfile.run("solve_greedy(board2)")
#         endtime2 = time.time()
#         #print("Time taken : ", endtime - starttime)
#         greedytime = endtime2 - starttime2
#         greedytimes += [greedytimes]
#         print_board(board2)

#         with open('values.csv','a') as f:
#             wr = csv.writer(f)
#             wr.writerow([seqtime,greedytime])

if __name__ == "__main__":

    array = []
    with open('hard_sudokus.txt') as my_file:
        for line in my_file:
            array.append(line)

    n = int(array[0])
    for i in range(1,100):
        str = array[i].rstrip("\n")
        board = []
        k = 0
        for p in range(9):
            arr = []
            for q in range(9):
                arr.append(int(str[k]))
                k = k + 1
            board.append(arr)
        board2 = copy.deepcopy(board)

        start1 = time.time()
        solve(board)
        seqtime = time.time() - start1

        start2 = time.time()
        solve_greedy(board2)
        greedytime = time.time() - start2

        print(i)
        with open('values.csv','a') as f:
            wr = csv.writer(f)
            wr.writerow([seqtime,greedytime])
