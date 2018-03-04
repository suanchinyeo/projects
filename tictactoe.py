class Game():
    """ 
    Game should be able to do the following:
    0. Start game.
    1. Get players. 2 players are needed for each game, they can be human or computer.
    2. Determines if game is won.
    3. Determines winner.
    """
    def __init__(self):
        """
        Game has following objects:
        1. 3x3 board. This is represented in the following way:
                1 2 3
                4 5 6
                7 8 9 
        2. Players: player1 and player2.
        3. Solution: a list of possible rows that can still be claimed by either player1 
        or player2.
        4. Winner: player1 or player 2 or None (tie/game is not yet over).
        """
        self.board = {i:False for i in range(1, 10)}
        self.player1 = None
        self.player2 = None
        self.solution = [[1, 2, 3], [4, 5, 6], [7, 8, 9], 
                         [1, 4, 7], [2, 5, 8], [3, 6, 9], 
                         [1, 5, 9], [3, 5, 7]]
        self.getPlayers()
        self.winner = None
        self.play()

    def setPlayer(self, player, n):
        """
        Given a player and a number (1 or 2), assigns it to player 1 or 2.
        """
        if n == 1:
            self.player1 = player
        elif n == 2:
            self.player2 = player

    def getPlayers(self):
        """
        Prompts user to set player1 and 2 as either human or computer.
        Enter h or H or any string containing H to play as human.
        Leave blank for Computer.
        """
        n = 0
        while n < 2:
            playerType = input("Player"+str(n+1)+": Play as Human by inserting 'H', insert ' ' to play as Computer:")
            if "H" in playerType.upper():
                player = Human(self, n+1)
                self.setPlayer(player, n+1)
            else:
                player = Computer(self, n+1)
                self.setPlayer(player, n+1)
            n += 1
        if self.player1.isComputer():
            self.player1.getOpponent()

    def getBoard(self):
        return self.board

    def __str__(self):
        """ The string representation of the board. """
        res = ""
        board = self.board
        spaces = 0
        for i in range(1, 10):
            if not board[i]:
                res += str(i)
            else:
                res += board[i]
            if spaces <2:
                res += " "
                spaces += 1
            elif spaces == 2:
                res += "\n"
                spaces = 0
        return res

    def isOver(self):
        """
        If game is over and there is a winner, updates winner and returns True.
        If game is not there is no winner, returns True.
        If game is not over, updates solution by removing the solutions that are no longer
        possible for either player.
        """
        solution = self.solution[:]
        board = self.getBoard()
        for i in solution[:]:
            p1 = 0
            p2 = 0
            for c in range(len(i)):
                if board[i[c]] == self.player1.getChar():
                    p1 += 1
                if board[i[c]] == self.player2.getChar():
                    p2 += 1
            if p1 == 3:
                self.winner = self.player1
                return True
            if p2 == 3:
                self.winner = self.player2
                return True
            if p1 != 0 and p2 != 0:
                solution.remove(i)
        if len(solution) == 0:
            return True
        else:
            self.solution = solution


    def updateBoard(self, location, char):
        """Inserts a piece onto the board"""
        self.board[location] = char

    def play(self):
        """
        Player1 plays first, then player2.
        When game is over, announces winner or tie.
        """
        while not self.isOver():
            self.player1.play()
            if not self.isOver():
                self.player2.play()
        if self.winner == None:
            print("Game Over! It's a tie.")
            print(self)
        else:
            print("Congratulations! "+self.winner.getName()+" has won!")
            print(self)



class Player():
    """
    Player has the following objects:
    Game: a Game object it is playing.
    Name: just for instructions and announcing winner.
    Char: this is the piece the player plays with. "x" or "o".
    Num: 1 or 2. Player1 or Player2 in self.game.
    """
    def __init__(self, Game, n):
        self.game = Game
        self.name = None
        self.Num = n
        self.char = None

    def getName(self):
        return self.name

    def getChar(self):
        return self.char


class Human(Player):
    """
    Human player.
    """
    def __init__(self, Game, n):
        Player.__init__(self, Game, n)
        self.name = self.setName()
        self.char = self.setChar()

    def isHuman(self):
        return True

    def isComputer(self):
        return False

    def setChar(self):
        """
        If human player is player1, gets to choose between "o" or "x".
        If human player is player2, gets the leftover piece, and is informed of what
        that is.
        """
        if self.Num == 1:
            char = input("Insert 'x' or 'o' to select your piece:")
            while char.lower() not in "xo":
                char = input("Invalid input. Please select 'x' or 'o':")
            return char.lower()
        else:
            opponentchar = self.game.player1.getChar() 
            if opponentchar == "x":
                print("Your piece is 'o'.")
                return "o"
            print("Your piece is 'x'.")
            return "x"

    def setName(self):
        name = input("Insert name:")
        return name

    def play(self):
        """
        Prompts human player to enter cell to place piece on.
        Loops error message until choice is valid.
        """
        possibles = [i for i in self.game.getBoard() if self.game.getBoard()[i] == False]
        print(self.name+"'s Turn: your piece is "+self.char)
        print("Empty cells are represented by their numbers, filled cells are represented by 'x's and 'o's:")
        print(self.game)
        loc = input("Choose cell by inserting its number:")
        while int(loc) not in possibles:
            print(self.game)
            loc = input("Invalid entry. Please insert available numbers:")
        self.game.updateBoard(int(loc), self.char)
        print(self.game)

class Computer(Player):
    """
    Computer player. Like human player but makes best move available. Never loses.
    unlike human player, has self.opponent. So it is aware of its opponent's moves.
    """
    def __init__(self, Game, n):
        Player.__init__(self, Game, n)
        if self.Num == 1:
            self.name = "player1"
        elif self.Num == 2:
            self.name = "player2"
        self.opponent = self.getOpponent()
        self.char = self.setChar()

    def getOpponent(self):
        """ 
        Gets the opponent.
        If player1 is a computer and player2 has not been assigned, there's a line
        in Game()'s getPlayers() method that calls this method again for player1 after
        the player2 has been assigned.
        """
        if self.Num == 1:
            self.opponent = self.game.player2
            return self.game.player2
        elif self.Num == 2:
            self.opponent = self.game.player1
            return self.game.player1

    def setChar(self):
        """ 
        Due to lack of creativity, computer always picks "x" if given first choice.
        Else it will take leftover piece.
        """
        if self.Num == 1:
            return "x"
        elif self.opponent.getChar() == "x":
            return "o"
        return "x"

    def move(self, location):
        """
        Makes a move, informs user of what cell it has chosen.
        """
        self.game.updateBoard(location, self.char)
        print(self.name+" has chosen cell "+str(location)+".")
        print(self.game)



    def play(self):
        """
        Computer plays by following these rules:
        1. If computer has a possible win within 1 move, it will make that move.
        2. If 1. is not true, and opponent has possible win within 1 move, it will block that win.
        3. If neither 1 nor 2 is true, computer will look at its possible solutions (the solutions
        in which its opponents have yet to play), and pick the cell that appears in the most
        possible wins.
        4. If none of the above is true, it will pick a random empty cell.
        """
        print("Computer: "+self.name+" is playing ...")
        solution = self.game.solution[:]
        board = self.game.getBoard()
        bestcells = {i:0 for i in board if board[i] == False} # all the empty cells and their scores
        opponentw = None # the move the opponent needs to win at their next turn
        for i in solution[:]:
            sol = [board[a] for a in i]
            if self.opponent.getChar() not in sol: # computer has a chance of winning in this solution
                scount = 0
                empties = []
                for c in range(len(i)):
                    if board[i[c]] == self.char: # number of pieces computer has in this solution
                        scount += 1
                    else:
                        empties.append(i[c])
                        bestcells[i[c]] += 1
                if scount == 2: # computer has 2 in a line and can win in this move
                    self.move(empties[0])
                    return
            if self.char not in sol: # opponent has a chance of winning in this solution
                ocount = 0
                empties = []
                for e in range(len(i)):
                    if board[i[e]] == self.opponent.getChar(): # number of pieces opponent has in this solution.
                        ocount += 1
                    else:
                        empties.append(i[e])
                if ocount == 2: # opponent has 2 in a line and can win at their next move
                    opponentw = empties[0]
        if opponentw != None:
            self.move(opponentw)
            return
        loc = max(bestcells, key=bestcells.get)
        self.move(loc)
        return

    def isHuman(self):
        return False

    def isComputer(self):
        return True


Game()


        
