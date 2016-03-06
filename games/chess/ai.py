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
            
        self.pawnList = [piece for piece in self.player.pieces if piece.type == "Pawn"]
        self.knightList = [piece for piece in self.player.pieces if piece.type == "Knight"]
        self.bishopList = [piece for piece in self.player.pieces if piece.type == "Bishop"]
        self.rookList = [piece for piece in self.player.pieces if piece.type == "Rook"]
        self.queenList = [piece for piece in self.player.pieces if piece.type == "Queen"]
        self.theKing = [piece for piece in self.player.pieces if piece.type == "King"]

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
      newRank = self.ChangeRank(pawn.rank, self.player.rank_direction)
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
      newRank = pawn.rank+self.player.rank_direction
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
      newRank = pawn.rank+self.player.rank_direction
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          return theMoveList
      
      # Make sure we do not move the pawn into an occupied space.
      newRank = newRank+self.player.rank_direction
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          return theMoveList
      
      theMoveList.append( (newFile, newRank, pawn) )
      return theMoveList
      
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
        return "Invalid"
    
      # Make sure we do not move the piece into an occupied space.
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          if piece.owner == self.player:
            return "Player"
          else:
            return "Opponent"

      return "Valid"
      
      
    def MoveListCardinal(self, piece, newMoves, step, direction):
      currentFile = piece.file
      currentRank = piece.rank
      encounteredPiece = False
      while(encounteredPiece is False):
        newMove = None
        if direction == 'h':
          newMove = (self.ChangeFile(currentFile, step), currentRank, piece)
        else:
          newMove = (currentFile, self.ChangeRank(currentRank, step), piece)
        validity = self.CheckValidSpace(newMove[0], newMove[1])
        if validity == "Valid":
          newMoves.append(newMove)
          currentFile = newMove[0]
          currentRank = newMove[1]
        elif validity == "Opponent":
          newMoves.append(newMove)
          currentFile = newMove[0]
          currentRank = newMove[1]
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
        validity = self.CheckValidSpace(newMove[0], newMove[1])
        if validity == "Valid":
          newMoves.append(newMove)
          currentFile = newMove[0]
          currentRank = newMove[1]
        elif validity == "Opponent":
          newMoves.append(newMove)
          currentFile = newMove[0]
          currentRank = newMove[1]
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

      # Generate all the possible Rook moves
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
      
      # Generate all the possible Rook moves
      theMoveList = self.MoveListDiagonal(bishop, theMoveList, 1, 1)
      theMoveList = self.MoveListDiagonal(bishop, theMoveList, 1, -1)
      theMoveList = self.MoveListDiagonal(bishop, theMoveList, -1, 1)
      theMoveList = self.MoveListDiagonal(bishop, theMoveList, -1, -1)

      return theMoveList
      
      
    def GenerateKnightMoves(self, knight, theMoveList):

      # Generate all the possible Knight moves
      knightMoves = [ (2,-1), (2, 1), (-2, -1), (-2, 1), (1, -2), (-1, -2), (1, 2), (-1, 2) ]
      
      for move in knightMoves:
        newMove = (self.ChangeFile(knight.file, move[0]), self.ChangeRank(knight.rank, move[1]), knight)
        validity = self.CheckValidSpace(newMove[0], newMove[1])
        if validity == "Valid" or validity == "Opponent":
          theMoveList.append(newMove)

      return theMoveList
      
    def GenerateKingMoves(self, king, theMoveList):
      
      # Generate all the possible King moves
      kingMoves = [ (0,1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1) ]
      
      for move in kingMoves:
        newMove = (self.ChangeFile(king.file, move[0]), self.ChangeRank(king.rank, move[1]), king)
        validity = self.CheckValidSpace(newMove[0], newMove[1])
        if validity == "Valid" or validity == "Opponent":
          theMoveList.append(newMove)

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
        
        theMoveList = []

        for piece in self.pawnList:
          theMoveList = self.GeneratePawnMoves(piece, theMoveList)
          
        for piece in self.knightList:
          theMoveList = self.GenerateKnightMoves(piece, theMoveList) 
          
        for piece in self.bishopList:
          theMoveList = self.GenerateBishopMoves(piece, theMoveList) 
          
        for piece in self.rookList:
          theMoveList = self.GenerateRookMoves(piece, theMoveList) 
          
        for piece in self.queenList:
          theMoveList = self.GenerateQueenMoves(piece, theMoveList) 
          
        for piece in self.theKing:
          theMoveList = self.GenerateKingMoves(piece, theMoveList) 
        
        # print("Total Moves:")
        # print(theMoveList)
        
        
        randomMove = random.choice(theMoveList)
        print("Moving " + str(randomMove[2]))
        randomMove[2].move(randomMove[0], randomMove[1])
        # print("Moved to: " + str(newFile) + str(newRank))
        print("End of my turn.")
        return True # to signify we are done with our turn.
