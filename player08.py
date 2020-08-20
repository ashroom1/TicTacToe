winners = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
valid_board_list = []
no_symmetries = {}
if_player_won = 0
move_list_per_game = []
import random


def game_not_over(board, who):
    for win in winners:
        if all([board[x] == who for x in win]):
            return False, who
    if 0 in board:
        return True, 99
    return False, 100


def game_not_over2(board, who):
    for win in winners:
        if all([int(board[x]) == who for x in win]):
            return False, who
    if '0' in board:
        return True, 99
    return False, 100


class Player08:

    def __init__(self, who):
        global valid_board_list
        self.who = who
        base_board = [0] * 9
        valid_board_list = [tuple(base_board)]
        self.valid_boards(base_board, 1)
        for x in valid_board_list:
            self.eliminate_symmetries(self.find_canonical(''.join(map(str, x))))
        self.outFile = open('cs47508.dump', 'wt')

    def find_canonical(self, board):
        symmetries = ["012345678", "630741852", "258147036", "876543210", "210543876", "678345012", "852741630",
                      "036147258"]

        symmetry_all = set()
        temp_board = ['0']*9

        for y in symmetries:
            for x in range(0, 9):
                temp_board[y.find(str(x))] = board[x]
            symmetry_all.add(''.join(temp_board))

        return sorted(symmetry_all)[0]

    def valid_boards(self, current_board, player_to_move):
        global valid_board_list

        empty_positions = [x for x in range(9) if current_board[x] == 0]
        for y in empty_positions:
            current_board[y] = player_to_move
            if list(current_board) not in valid_board_list:
                valid_board_list.append(list(current_board))
                truth, value = game_not_over(current_board, player_to_move)
                if truth:
                    self.valid_boards(current_board, 3 - player_to_move)
            current_board[y] = 0
        return valid_board_list

    def eliminate_symmetries(self, each_valid_board):
        global no_symmetries
        if each_valid_board not in no_symmetries:
            no_symmetries[each_valid_board] = 0.5
        return no_symmetries

    def getmove(self, board):
        new_board = []
        for x in board:
            new_board.append(str(x))
        board = new_board

        #Find out whether the board is valid
        if self.find_canonical((''.join(board))) not in no_symmetries:
            return -1

        global if_player_won
        global move_list_per_game
        move_list = [x for x in range(9) if board[x] == '0']
        best_current_move = ''
        best_current_weight = 0
        truth, value = game_not_over2(board, self.who) #was 2 instead of self.who
        if truth:
           for mov in move_list:
               board[mov] = str(self.who)
               if no_symmetries.get(self.find_canonical(''.join(board))) >= best_current_weight:
                   best_current_move = mov
                   best_current_weight = no_symmetries.get(self.find_canonical(''.join(board)))
               board[mov] = '0'
           board[best_current_move] = str(self.who)
           move_list_per_game.append(self.find_canonical(board))

    #To check if other player can win next move
        truth , value = game_not_over2(board, self.who)
        if truth:
            possible_o_moves = [y for y in range(9) if board[y] == '0']
            for move in possible_o_moves:
                board[move] = str(3 - self.who)
                truth, value = game_not_over2(board, 3 - self.who)
                board[move] = '0'
                if not truth:
                    board[move] = str(3 - self.who)
                    if value == 3 - self.who:
                        if_player_won = 1
                        move_list_per_game.append(self.find_canonical(board))
                        no_symmetries[move_list_per_game[-1]] = 0
                        for x in range(2, len(move_list_per_game) + 1):
                            no_symmetries[move_list_per_game[-x]] = (no_symmetries.get(move_list_per_game[-x]) + no_symmetries.get(
                             move_list_per_game[-x + 1])) / 2
                    move_list_per_game = move_list_per_game[0:len(move_list_per_game)]
                    break
        # We won yay!
        truth, value = game_not_over2(board, self.who)
        if not truth:
            if value == self.who:
                if_player_won = 1
                no_symmetries[move_list_per_game[-1]] = 1
                for x in range(2, len(move_list_per_game) + 1):
                    no_symmetries[move_list_per_game[-x]] = (no_symmetries.get(move_list_per_game[-x]) + no_symmetries.get(
                        move_list_per_game[-x + 1])) / 2
            move_list_per_game = []

        #It's a tie
        if not truth:
            if if_player_won == 100:
                for x in range(2, len(move_list_per_game) + 1):
                    no_symmetries[move_list_per_game[-1]] = 0.35
                    no_symmetries[move_list_per_game[-x]] = (no_symmetries.get(move_list_per_game[-x]) + no_symmetries.get(
                        move_list_per_game[-x + 1])) / 2
                move_list_per_game = []
            if_player_won = 0

        return best_current_move

    def datadump(self): 
        self.outFile.write(str(no_symmetries))
        self.outFile.write('\n' + '-------------------------------------' + '\n')

    def __string__(self):
        return 'Ashwin Murali'

    def gameover(self,board,rv):
        pass
