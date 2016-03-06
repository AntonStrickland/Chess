# This is where you build your AI for the Chess game.

# NAME: Anton Strickland

from joueur.base_ai import BaseAI
import random

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        """ This is the name you send to the server so your AI will control the player named this string.

        Returns
            str: The name of your Player.
        """

        return "Seacats" # REPLACE THIS WITH YOUR TEAM NAME



    def start(self):
        """ This is called once the game starts and your AI knows its playerID and game. You can initialize your AI here.
        """
        self.PAWN = "Pawn"
        self.KNIGHT = "Knight"
        self.BISHOP = "Bishop"
        self.ROOK = "Rook"
        self.QUEEN = "Queen"
        self.KING = "King"
        
        self.TheirMoveList = []
        self.enableCheckValidation = True
        
        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.knightMoves = [ (2,-1), (2, 1), (-2, -1), (-2, 1), (1, -2), (-1, -2), (1, 2), (-1, 2) ]
        self.kingMoves = [ (0,1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1) ]
        self.pieceNames = [self.PAWN, self.KNIGHT, self.BISHOP, self.ROOK, self.QUEEN, self.KING]
        
        self.generatorDict = { 
          self.PAWN: self.GeneratePawnMoves, self.KNIGHT: self.GenerateKnightMoves, self.BISHOP: self.GenerateBishopMoves, 
          self.ROOK: self.GenerateRookMoves, self.QUEEN: self.GenerateQueenMoves, self.KING: self.GenerateKingMoves
        }
        
        self.pieceDict = {}
        for name in self.pieceNames:
          self.pieceDict[name] = {
            self.player.id: [piece for piece in self.player.pieces if piece.type == name], 
            self.player.other_player.id: [piece for piece in self.player.other_player.pieces if piece.type == name]
          }

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
      
    def GeneratePawnMoves(self, pawn, theMoveList):
      theMoveList = self.MovePawnUpOneRank(pawn, theMoveList)
      theMoveList = self.MovePawnUpTwoRanks(pawn, theMoveList)
      theMoveList = self.CaptureWithPawn(pawn, theMoveList, 'l')
      theMoveList = self.CaptureWithPawn(pawn, theMoveList, 'r')
      return theMoveList
      
    def CaptureWithPawn(self, pawn, theMoveList, direction):
    
      # Generate new rank and new file
      newRank = self.ChangeRank(pawn.rank, 1)
      if direction == 'l':
        newFile = self.ChangeFile(pawn.file, -1)
      else:
        newFile = self.ChangeFile(pawn.file, 1)
      
      # If there is an enemy piece at that space, this is a valid move
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank and piece.owner != self.player:
          theMoveList.append( (newFile, newRank, pawn) )
      
      return theMoveList
      
    def MovePawnUpOneRank(self, pawn, theMoveList):
    
      # Make sure we do not move the pawn into an occupied space.
      newFile = pawn.file
      newRank = self.ChangeRank(pawn.rank, 1)
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          return theMoveList
      
      theMoveList.append( (newFile, newRank, pawn) )
      return theMoveList
      
    def MovePawnUpTwoRanks(self, pawn, theMoveList):
        
      # Make sure we only do this on the initial rank
      if pawn.rank != 2:
        return theMoveList
        
      # Make sure we do not move the pawn through an occupied space.
      newFile = pawn.file
      newRank = self.ChangeRank(pawn.rank, 1)
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          return theMoveList
      
      # Make sure we do not move the pawn into an occupied space.
      newRank = self.ChangeRank(newRank, 1)
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          return theMoveList
      
      theMoveList.append( (newFile, newRank, pawn) )
      return theMoveList
      
    def GetFileIndex(self, oldFile):
      
      index = 0
      for i in range(0, len(self.files)):
        if self.files[i] == oldFile:
          index = i
            
      return index
      
    def ChangeFile(self, oldFile, diff):
    
      if oldFile is None:
        return None
      
      new = self.GetFileIndex(oldFile) + diff
          
      if new >= 0 and new < len(self.files):
        return self.files[new]
      else:
        return None
    
    def ChangeRank(self, oldRank, diff):
    
      if oldRank is None:
        return None
      
      newRank = oldRank + (self.player.rank_direction * diff)
      if newRank > 0 and newRank < 9:
        return newRank
      else:
        return None
    
    def CheckValidSpace(self, newFile, newRank, movingPiece):
    
      validType = "Valid"
      
      # If the space is out of bounds, return False
      if newFile is None or newRank is None:
        return "Invalid"
    
      # Make sure we do not move the piece into an occupied space.
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          if piece.owner == self.player:
            validType = "Invalid"
            return validType
          else:
            validType = "Opponent"
            
            
      '''# If we are moving the king, make sure this move does not put him in check.
      # Else, if we are moving something else, make sure the king is not in check.
      if movingPiece.type == "King":
        # print("Please don't move into check.")
        isCheck = self.CheckForCheck(newFile, newRank)
      else:
        # print("Trying to resolve check.")
        isCheck = self.CheckForCheck(self.theKing[0].file, self.theKing[0].rank)
        
      if isCheck is True:
        print("Failed to resolve check.")
        return "Invalid"'''
      
      if self.enableCheckValidation == True:
        self.TheirMoveList = self.GenerateAllValidMoves(self.player.other_player.id)
        king = self.pieceDict[self.KING][self.player.id][0]
        for theirMove in self.TheirMoveList:
          if theirMove[0] == king.file and theirMove[1] == king.rank:
            return "Invalid"
         
      return validType
    
    def CheckForCheck(self, file, rank):

      newSquare = (self.ChangeFile(file, -1), self.ChangeRank(rank, -1))
      piece = self.GetPieceAtSquare(newSquare[0], newSquare[1])
      if piece is not None and piece.type == "Pawn":
        return True
        
      newSquare = (self.ChangeFile(file, 1), self.ChangeRank(rank, -1))
      piece = self.GetPieceAtSquare(newSquare[0], newSquare[1])
      if piece is not None and piece.type == "Pawn":
        return True
        
      for move in self.kingMoves:
        newSquare = (self.ChangeFile(file, move[0]), self.ChangeRank(rank, move[1]))
        piece = self.GetPieceAtSquare(newSquare[0], newSquare[1])
        if piece is not None and piece.type == "King":
          return True
          
      for move in self.knightMoves:
        newSquare = (self.ChangeFile(file, move[0]), self.ChangeRank(rank, move[1]))
        piece = self.GetPieceAtSquare(newSquare[0], newSquare[1])
        # print(file, rank, newSquare, self.GetPieceAtSquare(newSquare[0], newSquare[1]))
        if piece is not None and piece.type == "Knight":
          # print(file, rank, newSquare, piece.type)
          return True
      
      if self.CheckCardinally(file, rank, 1, 'h'):
        return True
      if self.CheckCardinally(file, rank, -1, 'h'):
        return True
      if self.CheckCardinally(file, rank, 1, 'v'):
        return True
      if self.CheckCardinally(file, rank, -1, 'v'):
        return True

      if self.CheckDiagonally(file, rank, 1, 1):
        return True
      if self.CheckDiagonally(file, rank, -1, -1):
        return True
      if self.CheckDiagonally(file, rank, 1, -1):
        return True
      if self.CheckDiagonally(file, rank, -1, 1):
        return True
        
      return False
      
    def CheckCardinally(self, file, rank, step, direction):
      currentFile = file
      currentRank = rank
      
      while True:
        if direction == 'h':
          newSquare = (self.ChangeFile(currentFile, step), currentRank)
        else:
          newSquare = (currentFile, self.ChangeRank(currentRank, step))
          
        enemyPiece = self.GetPieceAtSquare(newSquare[0], newSquare[1])
        
        # If we run into an enemy and it is a queen or rook we are in check
        if enemyPiece is not None and enemyPiece.owner != self.player:
          if enemyPiece.type == "Queen" or enemyPiece.type == "Rook":
            return True
        # If we run into our own piece we are not in check
        elif enemyPiece is not None and enemyPiece.owner == self.player:
          return False
        # If the square is off the board we are not in check
        elif newSquare[0] is None or newSquare[1] is None:
          return False
          
        currentFile = newSquare[0]
        currentRank = newSquare[1]
      return False
      
    def CheckDiagonally(self, file, rank, step1, step2):
      currentFile = file
      currentRank = rank
      while True:

        newSquare = (self.ChangeFile(currentFile, step1), self.ChangeRank(currentRank, step2))
        enemyPiece = self.GetPieceAtSquare(newSquare[0], newSquare[1])
        
        if enemyPiece is not None and enemyPiece.owner != self.player:
          if enemyPiece.type == "Queen" or enemyPiece.type == "Bishop":
            return True
        elif enemyPiece is not None and enemyPiece.owner == self.player:
          return False
        elif newSquare[0] is None and newSquare[1] is None:
          return False

        currentFile = newSquare[0]
        currentRank = newSquare[1]
      return False
      
    def GetPieceAtSquare(self, file, rank):
      if file is None or rank is None:
        return None
    
      for piece in self.game.pieces:
        if piece.file == file and piece.rank == rank:
          return piece
      return None
      
      
    def MoveListCardinal(self, piece, newMoves, step, direction):
      currentFile = piece.file
      currentRank = piece.rank
      encounteredPiece = False
      
      while(encounteredPiece is False):

        if direction == 'h':
          newMove = (self.ChangeFile(currentFile, step), currentRank, piece)
        else:
          newMove = (currentFile, self.ChangeRank(currentRank, step), piece)
          
        validity = self.CheckValidSpace(newMove[0], newMove[1], piece)
        
        if validity == "Valid":
          newMoves.append(newMove)
          currentFile = newMove[0]
          currentRank = newMove[1]
        elif validity == "Opponent":
          newMoves.append(newMove)
          encounteredPiece = True
        else:
          encounteredPiece = True
          
      return newMoves
    
    def MoveListDiagonal(self, piece, newMoves, step1, step2):
      currentFile = piece.file
      currentRank = piece.rank
      encounteredPiece = False
      
      while(encounteredPiece is False):
        newMove = (self.ChangeFile(currentFile, step1), self.ChangeRank(currentRank, step2), piece)
        validity = self.CheckValidSpace(newMove[0], newMove[1], piece)
       
        if validity == "Valid":
          if newMove[1] < 0:
            print(newMove[1])
          newMoves.append(newMove)
          currentFile = newMove[0]
          currentRank = newMove[1]
        elif validity == "Opponent":
          newMoves.append(newMove)
          encounteredPiece = True
        else:
          encounteredPiece = True
          
      return newMoves
    
    def GenerateRookMoves(self, rook, theMoveList):

      # Generate all the possible Rook moves
      theMoveList = self.MoveListCardinal(rook, theMoveList, 1, 'h')
      theMoveList = self.MoveListCardinal(rook, theMoveList, -1, 'h')
      theMoveList = self.MoveListCardinal(rook, theMoveList, 1, 'v')
      theMoveList = self.MoveListCardinal(rook, theMoveList, -1, 'v')

      return theMoveList
      

    def GenerateQueenMoves(self, queen, theMoveList):

      # Generate all the possible Queen moves
      theMoveList = self.MoveListCardinal(queen, theMoveList, 1, 'h')
      theMoveList = self.MoveListCardinal(queen, theMoveList, -1, 'h')
      theMoveList = self.MoveListCardinal(queen, theMoveList, 1, 'v')
      theMoveList = self.MoveListCardinal(queen, theMoveList, -1, 'v')
      theMoveList = self.MoveListDiagonal(queen, theMoveList, 1, 1)
      theMoveList = self.MoveListDiagonal(queen, theMoveList, 1, -1)
      theMoveList = self.MoveListDiagonal(queen, theMoveList, -1, 1)
      theMoveList = self.MoveListDiagonal(queen, theMoveList, -1, -1)

      return theMoveList
      
      
    def GenerateBishopMoves(self, bishop, theMoveList):
      
      # Generate all the possible Bishop moves
      theMoveList = self.MoveListDiagonal(bishop, theMoveList, 1, 1)
      theMoveList = self.MoveListDiagonal(bishop, theMoveList, 1, -1)
      theMoveList = self.MoveListDiagonal(bishop, theMoveList, -1, 1)
      theMoveList = self.MoveListDiagonal(bishop, theMoveList, -1, -1)

      return theMoveList
      
      
    def GenerateKnightMoves(self, knight, theMoveList):

      # Generate all the possible Knight moves
      for move in self.knightMoves:
        newMove = (self.ChangeFile(knight.file, move[0]), self.ChangeRank(knight.rank, move[1]), knight)
        validity = self.CheckValidSpace(newMove[0], newMove[1], knight)
        if validity == "Valid" or validity == "Opponent":
          theMoveList.append(newMove)

      return theMoveList
      
    def GenerateKingMoves(self, king, theMoveList):
      
      # Generate all the possible King moves
      for move in self.kingMoves:
        newMove = (self.ChangeFile(king.file, move[0]), self.ChangeRank(king.rank, move[1]), king)
        validity = self.CheckValidSpace(newMove[0], newMove[1], king)
        if validity == "Valid" or validity == "Opponent":
          theMoveList.append(newMove)

      return theMoveList
      
    def GenerateAllValidMoves(self, id):
      theMoveList = []
      
      self.generators = { }
      
      if id == self.player.other_player.id:
        self.enableCheckValidation = False
      else:
        self.enableCheckValidation = True
      
      for name in self.pieceNames:
        for piece in self.pieceDict[name][id]:
          if piece.captured is False:
            theMoveList = self.generatorDict[name](piece, theMoveList)
          
      return theMoveList

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
        
        self.TheirMoveList = self.GenerateAllValidMoves(self.player.other_player.id)
        MyMoveList = self.GenerateAllValidMoves(self.player.id)
        
        newList = []
        for m in MyMoveList:
          newList.append( (m[0], m[1], m[2].type) )
        print(newList)
        
        
        randomMove = random.choice(MyMoveList)
        print("Moving " + str(randomMove[2].type), randomMove[0], randomMove[1])
        randomMove[2].move(randomMove[0], randomMove[1])
        # print("Moved to: " + str(newFile) + str(newRank))
        print("End of my turn.")
        return True # to signify we are done with our turn.
