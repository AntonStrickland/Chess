# This is where you build your AI for the Chess game.

# NAME: Anton Strickland

from joueur.base_ai import BaseAI
import random

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    # knightMoves = [False, False, False, False, False, False, False, False]

    def get_name(self):
        """ This is the name you send to the server so your AI will control the player named this string.

        Returns
            str: The name of your Player.
        """

        return "Seacats" # REPLACE THIS WITH YOUR TEAM NAME



    def start(self):
        """ This is called once the game starts and your AI knows its playerID and game. You can initialize your AI here.
        """

        # replace with your start logic




    def game_updated(self):
        """ This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """

        # replace with your game updated logic


    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or lost.
        """

        # replace with your end logic
    
    
    def InCheck(self):
      print("...")
    
    
    def GetRandomPawn(self):
      pawns = []
      for piece in self.player.pieces:
        if piece.type == "Pawn":
          pawns.append(piece)    
      return random.choice(pawns)
      
      
    def MovePawnUpOneRank(self, pawn, newFile, newRank):
    
      
      # Make sure we are moving a pawn.
      if pawn.type != "Pawn":
        return False, None, None
        
      # Make sure we do not move the pawn into an occupied space.
      newFile = pawn.file
      newRank = pawn.rank+self.player.rank_direction
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          return False, None, None
      
      return True, newFile, newRank 
      
    def MovePawnUpTwoRanks(self, pawn, newFile, newRank):
    
      # Make sure we are moving a pawn.
      if pawn.type != "Pawn":
        return False, None, None
        
      # Make sure we only do this on the initial rank
      if pawn.rank != 2:
        return False, None, None
        
      # Make sure we do not move the pawn through an occupied space.
      newFile = pawn.file
      newRank = pawn.rank+self.player.rank_direction
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          return False, None, None
      
      # Make sure we do not move the pawn into an occupied space.
      newRank = newRank+self.player.rank_direction
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          return False, None, None
          
      return True, newFile, newRank
      
    def ChangeFile(self, oldFile, diff):
      files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
      
      index = 0
      for i in range(0, len(files)):
        if files[i] == oldFile:
          index = i
          # print("i is " + str(i))
          
      new = index+diff
          
      if new >= 0 and new < len(files):
        return files[new]
      else:
        return None
    
    def ChangeRank(self, oldRank, diff):
      
      newRank = oldRank + (self.player.rank_direction * diff)
      if newRank > 0 and newRank < 8:
        return newRank
      else:
        return None
    
    def CheckValidSpace(self, newFile, newRank):
    
      # If the space is out of bounds, return False
      if newFile is None or newRank is None:
        return False
    
      # Make sure we do not move the piece into an occupied space.
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
            return False
      return True
      
      
    def MoveListCardinal(self, piece, newMoves, step, direction):
      currentFile = piece.file
      currentRank = piece.rank
      encounteredPiece = False
      while(encounteredPiece is False):
        newMove = None
        if direction == 'h':
          newMove = (self.ChangeFile(currentFile, step), currentRank)
        else:
          newMove = (currentFile, self.ChangeRank(currentRank, step))
        if self.CheckValidSpace(newMove[0], newMove[1]):
          newMoves.append(newMove)
          currentFile = newMove[0]
          currentRank = newMove[1]
        else:
          encounteredPiece = True
      return newMoves
    
    def MoveListDiagonal(self, piece, newMoves, step1, step2):
      currentFile = piece.file
      currentRank = piece.rank
      encounteredPiece = False
      while(encounteredPiece is False):
        newMove = (self.ChangeFile(currentFile, step1), self.ChangeRank(currentRank, step2))
        if self.CheckValidSpace(newMove[0], newMove[1]):
          newMoves.append(newMove)
          currentFile = newMove[0]
          currentRank = newMove[1]
        else:
          encounteredPiece = True
      return newMoves
    
    def MoveRookCardinally(self, rook, newFile, newRank):
    
      
      # Make sure we are moving a knight.
      if rook.type != "Rook":
        return False, None, None
        
      newRookMoves = []
      
      print("Moving rook...")
      
      # Generate all the possible Rook moves
      newRookMoves = self.MoveListCardinal(rook, newRookMoves, 1, 'h')
      newRookMoves = self.MoveListCardinal(rook, newRookMoves, -1, 'h')
      newRookMoves = self.MoveListCardinal(rook, newRookMoves, 1, 'v')
      newRookMoves = self.MoveListCardinal(rook, newRookMoves, -1, 'v')
      
      # If no moves can be made, return False
      if (len(newRookMoves) <= 0):
        return False, None, None
        

      print("Final Moves:")
      print(newRookMoves)

      # Pick a random valid move
      newMove = random.choice(newRookMoves)
      newFile, newRank = newMove[0], newMove[1]

      return True, newFile, newRank
      

    def MoveQueen(self, queen, newFile, newRank):
    
      # Make sure we are moving a knight.
      if queen.type != "Queen":
        return False, None, None
        
      newQueenMoves = []
      
      print("Moving queen...")
      
      # Generate all the possible Rook moves
      newQueenMoves = self.MoveListCardinal(queen, newQueenMoves, 1, 'h')
      newQueenMoves = self.MoveListCardinal(queen, newQueenMoves, -1, 'h')
      newQueenMoves = self.MoveListCardinal(queen, newQueenMoves, 1, 'v')
      newQueenMoves = self.MoveListCardinal(queen, newQueenMoves, -1, 'v')
      newQueenMoves = self.MoveListDiagonal(queen, newQueenMoves, 1, 1)
      newQueenMoves = self.MoveListDiagonal(queen, newQueenMoves, 1, -1)
      newQueenMoves = self.MoveListDiagonal(queen, newQueenMoves, -1, 1)
      newQueenMoves = self.MoveListDiagonal(queen, newQueenMoves, -1, -1)
      
      # If no moves can be made, return False
      if (len(newQueenMoves) <= 0):
        return False, None, None
        
      print("Final Moves:")
      print(newQueenMoves)

      # Pick a random valid move
      newMove = random.choice(newQueenMoves)
      newFile, newRank = newMove[0], newMove[1]

      return True, newFile, newRank
      
      
    def MoveBishopDiagonally(self, bishop, newFile, newRank):
    
      # Make sure we are moving a knight.
      if bishop.type != "Bishop":
        return False, None, None
        
      newBishopMoves = []
      
      print("Moving bishop...")
      
      # Generate all the possible Rook moves
      newBishopMoves = self.MoveListDiagonal(bishop, newBishopMoves, 1, 1)
      newBishopMoves = self.MoveListDiagonal(bishop, newBishopMoves, 1, -1)
      newBishopMoves = self.MoveListDiagonal(bishop, newBishopMoves, -1, 1)
      newBishopMoves = self.MoveListDiagonal(bishop, newBishopMoves, -1, -1)
      
      # If no moves can be made, return False
      if (len(newBishopMoves) <= 0):
        return False, None, None
        
      print("Final Moves:")
      print(newBishopMoves)

      # Pick a random valid move
      newMove = random.choice(newBishopMoves)
      newFile, newRank = newMove[0], newMove[1]

      return True, newFile, newRank
      
      
    def MoveKnightUpTwoOverOne(self, knight, newFile, newRank):
  
      # directions1 = [(-1,0), (1,0)] # left, right
      # directions2 = [(0,1), (0,-1)] # up, down
      
      # Make sure we are moving a knight.
      if knight.type != "Knight":
        return False, None, None
        
      newKnightMoves = []
      
      # Generate all the possible Knight moves
        
      knightMoves = [ (2,-1), (2, 1), (-2, -1), (-2, 1), (1, -2), (-1, -2), (1, 2), (-1, 2) ]
      
      for move in knightMoves:
        newMove = (self.ChangeFile(knight.file, move[0]), self.ChangeRank(knight.rank, move[1]))
        if self.CheckValidSpace(newMove[0], newMove[1]) is True:
          newKnightMoves.append(newMove)
      
      print(newKnightMoves)
      
      # If no moves can be made, return False
      if (len(newKnightMoves) <= 0):
        return False, None, None
        

      print("Final Moves:")
      print(newKnightMoves)

      # Pick a random valid move
      newMove = random.choice(newKnightMoves)
      newFile, newRank = newMove[0], newMove[1]
      
      # Move the knight.
      # knight.move(newFile, newRank)

      return True, newFile, newRank
      
    def MoveKing(self, king, newFile, newRank):
  
      # directions1 = [(-1,0), (1,0)] # left, right
      # directions2 = [(0,1), (0,-1)] # up, down
      
      # Make sure we are moving a knight.
      if king.type != "King":
        return False, None, None
        
      newKingMoves = []
      
      # Generate all the possible King moves
        
      kingMoves = [ (0,1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
      
      for move in kingMoves:
        newMove = (self.ChangeFile(king.file, move[0]), self.ChangeRank(king.rank, move[1]))
        if self.CheckValidSpace(newMove[0], newMove[1]) is True:
          newKingMoves.append(newMove)
      
      print(newKingMoves)
      
      # If no moves can be made, return False
      if (len(newKingMoves) <= 0):
        return False, None, None
        

      print("Final Moves:")
      print(newKingMoves)

      # Pick a random valid move
      newMove = random.choice(newKingMoves)
      newFile, newRank = newMove[0], newMove[1]
      
      # Move the knight.
      # knight.move(newFile, newRank)

      return True, newFile, newRank

    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """

        # Here is where you'll want to code your AI.

        # We've provided sample code that:
        #    1) prints the board to the console
        #    2) prints the opponent's last move to the console
        #    3) prints how much time remaining this AI has to calculate moves
        #    4) makes a random (and probably invalid) move.

        # 1) print the board to the console
        for f in range(9, -2, -1): # iterate through the file in reverse order
            output = ""
            if f == 9 or f == 0: # then the top or bottom of the board
                output = "   +------------------------+"
            elif f == -1: # then show the ranks
                output = "     a  b  c  d  e  f  g  h"
            else: # board
                output = " " + str(f) + " |"
                # fill in all the ranks with pieces at the current rank
                for rankOffset in range(0, 8):
                    r = chr(ord("a") + rankOffset) # start at a, with with rank offset increasing the char
                    currentPiece = None
                    for piece in self.game.pieces:
                        if piece.file == r and piece.rank == f: # then we found the piece at (rank, file)
                            currentPiece = piece
                            break

                    code = "." # default "no piece"
                    if currentPiece:
                        code = currentPiece.type[0] # the code will be the first character of their type, e.g. 'Q' for "Queen"

                        if currentPiece.type == "Knight": # 'K' is for "King", we use 'N' for "Knights"
                            code = "N"

                        if currentPiece.owner.id == "1": # the second player (black) is lower case. Otherwise it's upppercase already
                            code = code.lower()

                    output += " " + code + " "

                output += "|"

            print(output)

        # 2) print the opponent's last move to the console
        if len(self.game.moves) > 0:
            print("Opponent's Last Move: '" + self.game.moves[-1].san + "'")

        # 3) print how much time remaining this AI has to calculate moves
        print("Time Remaining: " + str(self.player.time_remaining) + " ns")

        # 4) Make a Random Valid Move
        
        validMove = False
        newRank = None
        newFile = None
        while(validMove is False):
          thePiece = random.choice(self.player.pieces)
          theMove = random.randint(0,6)
          # print("Thinking...")
          if theMove == 0:
            validMove, newFile, newRank = self.MovePawnUpOneRank(thePiece, newFile, newRank)
          if theMove == 1:
            validMove, newFile, newRank = self.MovePawnUpTwoRanks(thePiece, newFile, newRank)
          if theMove == 2:
            validMove, newFile, newRank = self.MoveKnightUpTwoOverOne(thePiece, newFile, newRank)
          if theMove == 3:
            validMove, newFile, newRank = self.MoveRookCardinally(thePiece, newFile, newRank)
          if theMove == 4:
            validMove, newFile, newRank = self.MoveBishopDiagonally(thePiece, newFile, newRank)
          if theMove == 5:
            validMove, newFile, newRank = self.MoveQueen(thePiece, newFile, newRank)
          if theMove == 6:
            validMove, newFile, newRank = self.MoveKing(thePiece, newFile, newRank)
        thePiece.move(newFile, newRank)
        print("Moved to: " + str(newFile) + str(newRank))
        print("End of my turn.")
        return True # to signify we are done with our turn.
