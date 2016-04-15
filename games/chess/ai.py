#Name: Anton Strickland
#CS5400 Game Project 3

from joueur.base_ai import BaseAI
import random
import datetime
# import iddlmm
# import tlidabdlmm
import tlhtqsidabdlmm
import sys
import states
# import size
 
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
        
        # Constant values
        self.PAWN = "Pawn"
        self.KNIGHT = "Knight"
        self.BISHOP = "Bishop"
        self.ROOK = "Rook"
        self.QUEEN = "Queen"
        self.KING = "King"
        
        self.startTime = self.player.time_remaining
        self.randomSeed = 9 # datetime.datetime.now()
        
        
        self.promotedPreviousMove = False
        self.playerAtPlay = self.player.id
        
        random.seed(self.randomSeed)
        
        self.pieceNames = [self.PAWN, self.KNIGHT, self.BISHOP, self.ROOK, self.QUEEN, self.KING]
        
        self.currentBoard = []
        self.transpTable = {}
        self.historyTable = {}
        
        for i in range(0,8):
          self.currentBoard.append([])
          for j in range(0,8):
            self.currentBoard[i].append('.')
        
        # Constant arrays
        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.knightMoves = [ (2,-1), (2, 1), (-2, -1), (-2, 1), (1, -2), (-1, -2), (1, 2), (-1, 2) ]
        self.kingMoves = [ (0,1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1) ]
        self.rookMoves = [(1,'h'), (-1, 'h'), (1,'v'), (-1,'v')]
        self.bishopMoves = [(1,1), (1,-1), (-1,1), (-1,-1)]
      
        # Dictionary of generators which contains functions, where the key is the piece name
        self.generatorDict = { 
          self.PAWN: self.GeneratePawnMoves, self.KNIGHT: self.GenerateKnightMoves, self.BISHOP: self.GenerateBishopMoves, 
          self.ROOK: self.GenerateRookMoves, self.QUEEN: self.GenerateQueenMoves, self.KING: self.GenerateKingMoves
        }
        
        # Dictionary containing each players' respective pieces
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
        print("Seconds taken: " + str((self.startTime - self.player.time_remaining)/1000000000))
        print("Turns taken: " + str(self.game.current_turn))
        print("Random seed: " + str(self.randomSeed))
        
    def SwitchPlayerAtPlay(self, id):
      newID = "0"
      if id == "0":
        newID = "1"
      self.playerAtPlay = newID
      return
        
    def GetPieceAtBoard(self, board, newFile, newRank):
      if newFile is not None and newRank is not None:
        if newFile >= 0 and newFile < 8 and newRank >= 0 and newRank < 8:
          return board[newRank][newFile]
      return None
      
    def GetRankDirection(self):
      if self.playerAtPlay == self.player.id:
        return self.player.rank_direction
      else:
        return self.player.other_player.rank_direction
      
    # Checks if the king is in check by examining each possible enemy position.
    # First start at the king's position on the board, and work backwards.
    # If an enemy is encountered based on their attack pattern then we know we are in check.
    
    def CheckIfUnderAttack(self, board, kingFile, kingRank, pieceInCheck, friendlyFire=False):
    
      # print("---------------")
      
      # newState = State(board, self.player.id, None)
      # newState.printBoard()
      piece = self.GetPieceAtBoard(board, kingFile - 1, kingRank + self.GetRankDirection())

      if piece is not None and self.GetPieceCode2(piece, self.PAWN, pieceInCheck, friendlyFire):
        # print(piece, self.GetPieceCode2(piece,self.PAWN))
        return True, self.PAWN
      
      piece = self.GetPieceAtBoard(board, kingFile + 1, kingRank + self.GetRankDirection())
      if piece is not None and self.GetPieceCode2(piece, self.PAWN, pieceInCheck, friendlyFire):
        # print(piece, self.GetPieceCode2(piece,self.PAWN))
        return True, self.PAWN
          
      for move in self.knightMoves:
        piece = self.GetPieceAtBoard(board, kingFile + move[0], kingRank + move[1])
        if piece is not None and self.GetPieceCode2(piece, self.KNIGHT, pieceInCheck, friendlyFire):
          return True, self.KNIGHT

      for move in self.rookMoves:
        if self.CheckCardinally(board, kingFile, kingRank, pieceInCheck, move[0], move[1], friendlyFire):
          return True, self.ROOK

      for move in self.bishopMoves:
        if self.CheckDiagonally(board, kingFile, kingRank, pieceInCheck, move[0], move[1], friendlyFire):
          return True, self.BISHOP
          
      for move in self.kingMoves:
        piece = self.GetPieceAtBoard(board, kingFile + move[0], kingRank + move[1])
        if piece is not None and self.GetPieceCode2(piece, self.KING, pieceInCheck, friendlyFire):
          return True, self.KING
          
      return False, None
    
    # Checks a board cardinally to see if the king is in check    
    def CheckCardinally(self, board, file, rank, king, step, direction, friendlyFire=False):
      currentFile = file
      currentRank = rank

      newState = states.State(board, self.player.id, None, 0)
      while currentFile is not None and currentRank is not None:
        
        if direction == 'h':
          currentFile = currentFile + step
        else:
          currentRank = currentRank + (self.GetRankDirection() * step)
        
        # If the square is off the board we are not in check
        if currentFile >= len(board) or currentRank >= len(board) or currentFile < 0 or currentRank < 0:
          return False

        piece = board[currentRank][currentFile]

        # If we run into an enemy and it is a queen or rook we are in check
        if self.GetPieceCode2(piece, self.QUEEN, king, friendlyFire) or self.GetPieceCode2(piece, self.ROOK, king, friendlyFire):
          # print("Don't move to " + str(file) + str(rank) + self.ROOK)
          return True
        elif piece != '.':
          return False
        
      return False
    
    # Checks a board diagonally to see if the king is in check
    def CheckDiagonally(self, board, file, rank, king, step1, step2, friendlyFire=False):
    
      currentFile = file
      currentRank = rank
      newState = states.State(board, self.player.id, None, 0)
      while currentFile is not None and currentRank is not None:

        currentFile = currentFile + step1
        currentRank = currentRank + (self.GetRankDirection() * step2)
        
        if currentFile >= len(board) or currentRank >= len(board) or currentFile < 0 or currentRank < 0:
          return False
          
        piece = board[currentRank][currentFile]
        
        if self.GetPieceCode2(piece, self.QUEEN, king, friendlyFire) or self.GetPieceCode2(piece, self.BISHOP, king, friendlyFire):
          # print("Don't move to " + str(file) + str(rank) + self.BISHOP)
          return True
        elif piece != '.':
          return False
          
      return False
      
    def CaptureWithPawn(self, pawn, theMoveList, direction):
    
      # Generate new rank and new file
      newRank = self.ChangeRank(pawn.rank, 1)
      newFile = self.ChangeFile(pawn.file, direction)

      # If there is an enemy piece at that space, this is a valid move
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank and piece.owner != self.player:
          validity,reason = self.CheckValidSpace(newFile, newRank, pawn)
          if validity == "Opponent":
            if newRank != 1 and newRank != 8:
              theMoveList.append( states.Action(newFile, newRank, pawn, None, True, reason) )
            else:
              newMove = states.Action(newFile, newRank, pawn)
              newMove.hasPromoted = True
              newMove.promotedPiece = self.QUEEN
              theMoveList.append(newMove)
              newMove.promotedPiece = self.ROOK
              theMoveList.append(newMove)
              newMove.promotedPiece = self.BISHOP
              theMoveList.append(newMove)
              newMove.promotedPiece = self.KNIGHT
              theMoveList.append(newMove)
      return theMoveList
      
    def MovePawnUpOneRank(self, pawn, theMoveList):
    
      # Make sure we do not move the pawn into an occupied space.
      newFile = pawn.file
      newRank = self.ChangeRank(pawn.rank, 1)
      # print(str(self.player.id) + " moved from " + str(pawn.file) + str(pawn.rank) + " to " + str(newFile) + str(newRank))
      
      # Make sure the space is valid. Also consider pawn promotions.
      validity,reason = self.CheckValidSpace(newFile, newRank, pawn)
      if validity == "Valid":
        if newRank != 1 and newRank != 8:
          theMoveList.append( states.Action(newFile, newRank, pawn, "up one") )
        else:
          newMove = states.Action(newFile, newRank, pawn)
          newMove.hasPromoted = True
          newMove.promotedPiece = self.QUEEN
          theMoveList.append(newMove)
          newMove.promotedPiece = self.ROOK
          theMoveList.append(newMove)
          newMove.promotedPiece = self.BISHOP
          theMoveList.append(newMove)
          newMove.promotedPiece = self.KNIGHT
          theMoveList.append(newMove)
      return theMoveList
      
    def MovePawnUpTwoRanks(self, pawn, theMoveList):
        
      # Make sure we only do this on the initial rank
      if self.playerAtPlay == self.player.id and pawn.rank != 2 :
        return theMoveList
      elif self.playerAtPlay == self.player.other_player.id and pawn.rank != 7 :
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
      
      # Make sure the space is valid
      validity,reason = self.CheckValidSpace(newFile, newRank, pawn)
      if validity == "Valid":
        theMoveList.append( states.Action(newFile, newRank, pawn, "up two") )
      
      return theMoveList
      
    # Converts a chessboard-based file into an integer  
    def GetFileIndex(self, oldFile):
      index = 0
      for i in range(0, len(self.files)):
        if self.files[i] == oldFile:
          index = i
      return index
    
    # Changing files with chessboard-based arrays  
    def ChangeFile(self, oldFile, diff):
      if oldFile is None:
        return None
      new = self.GetFileIndex(oldFile) + diff
      if new >= 0 and new < len(self.files):
        return self.files[new]
      else:
        return None
        
    # Changing files with zero-based arrays    
    def ChangeFile2(self, oldFile, diff):
      if oldFile is None:
        return None
      new = self.GetFileIndex(oldFile) + diff
      # print(oldFile, diff, new)
      if new >= 0 and new < len(self.files):
        return new
      else:
        return None
        
    # Changing files with chessboard-based arrays
    def ChangeRank(self, oldRank, diff):
      if oldRank is None:
        return None
      
      newRank = oldRank + (self.GetRankDirection() * diff)
      if newRank > 0 and newRank < 9:
        return newRank
      else:
        return None
    
    # Changing ranks with zero-based arrays
    def ChangeRank2(self, oldRank, diff):
      if oldRank is None:
        return None
      
      newRank = oldRank + (self.GetRankDirection() * diff)
      if newRank >= 0 and newRank < 8:
        return newRank
      else:
        return None
        
    def CheckValidSpace(self, newFile, newRank, movingPiece):
    
      validType = "Valid"
      capturedPiece = None
      
      # If the space is out of bounds, return False
      if newFile is None or newRank is None:
        return "Invalid",capturedPiece
    
      # Make sure we do not move the piece into an occupied space.
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          # print(piece.owner.id, self.playerAtPlay)
          if piece.owner.id == self.playerAtPlay:
            validType = "Invalid"
            return validType,capturedPiece
          else:
            validType = "Opponent"
            capturedPiece = piece.type

      # Create a new board to simulate the next turn
      newBoard = []
      for x in range(0, 8):
        newBoard.append([])
        for y in range(0, 8):
          newBoard[x].append(self.currentBoard[x][y])
      
      # Modify the board to pretend we've moved the piece we want to move
      newBoard[movingPiece.rank-1][self.GetFileIndex(movingPiece.file)] = '.'
      newBoard[newRank-1][self.GetFileIndex(newFile)] = self.GetPieceCode(movingPiece)
      
      isCheck = False
      
      # Look for the king's new position and see if he is in check or not (with a reason why)
      for x in range(0,8):
          for y in range(0,8):
            if newBoard[x][y] == self.GetPieceCode(self.pieceDict[self.KING][self.player.id][0]):
              isCheck,reason = self.CheckIfUnderAttack(newBoard, y, x, newBoard[x][y])
              # print(reason)

      # Unapply the move
      # self.currentBoard[newRank-1][self.GetFileIndex(newFile)] = previousPiece
      # self.currentBoard[movingPiece.rank-1][self.GetFileIndex(movingPiece.file)] = self.GetPieceCode(movingPiece)
      
      # If he is in check, return Invalid
      if isCheck is True:
        return "Invalid",capturedPiece
              
      return validType,capturedPiece
      
    # Generate a list of moves by iterating cardinally over the board
    def MoveListCardinal(self, piece, newMoves, step, direction):
      currentFile = piece.file
      currentRank = piece.rank
      encounteredPiece = False
      
      # Keep iterating until we run into an enemy, one of our pieces, or leave the boundaries of the board
      while(encounteredPiece is False):

        # Either iterate horizontally or vertically
        if direction == 'h':
          newMove = states.Action(self.ChangeFile(currentFile, step), currentRank, piece)
        else:
          newMove = states.Action(currentFile, self.ChangeRank(currentRank, step), piece)
          
        # Check to make sure this space is valid
        validity,reason = self.CheckValidSpace(newMove.to[0], newMove.to[1], piece)
        
        if validity == "Valid":
          newMoves.append(newMove)
          currentFile = newMove.to[0]
          currentRank = newMove.to[1]
        elif validity == "Opponent":
          newMove.hasCaptured = True
          newMove.capturedPiece = reason
          newMoves.append(newMove)
          encounteredPiece = True
        else:
          encounteredPiece = True
          
      return newMoves
    
    # Generate a list of moves by iterating diagonally over the board
    def MoveListDiagonal(self, piece, newMoves, step1, step2):
      currentFile = piece.file
      currentRank = piece.rank
      encounteredPiece = False
      
      # Keep iterating until we run into an enemy, one of our pieces, or leave the boundaries of the board
      while(encounteredPiece is False):
        newMove = states.Action(self.ChangeFile(currentFile, step1), self.ChangeRank(currentRank, step2), piece)
       
        # Check to make sure this space is valid
        validity,reason = self.CheckValidSpace(newMove.to[0], newMove.to[1], piece)
       
        if validity == "Valid":
          newMoves.append(newMove)
          currentFile = newMove.to[0]
          currentRank = newMove.to[1]
        elif validity == "Opponent":
          newMove.hasCaptured = True
          newMove.capturedPiece = reason
          newMoves.append(newMove)
          encounteredPiece = True
        else:
          encounteredPiece = True
          
      return newMoves
    
    # Generate all the possible Pawn moves    
    def GeneratePawnMoves(self, pawn, theMoveList):
      theMoveList = self.MovePawnUpOneRank(pawn, theMoveList)
      theMoveList = self.MovePawnUpTwoRanks(pawn, theMoveList)
      theMoveList = self.CaptureWithPawn(pawn, theMoveList, -1)
      theMoveList = self.CaptureWithPawn(pawn, theMoveList, 1)
      theMoveList = self.EnPassant(pawn, theMoveList)
      return theMoveList
      
    # Generate all the possible Knight moves
    def GenerateKnightMoves(self, knight, theMoveList):
      for move in self.knightMoves:
        newMove = states.Action(self.ChangeFile(knight.file, move[0]), self.ChangeRank(knight.rank, move[1]), knight)
        validity,reason = self.CheckValidSpace(newMove.to[0], newMove.to[1], knight)
        if validity == "Valid" or validity == "Opponent":
          if validity == "Opponent":
            newMove.hasCaptured = True
            newMove.capturedPiece = reason
          theMoveList.append(newMove)
      return theMoveList
    
    # Generate all the possible Bishop moves
    def GenerateBishopMoves(self, bishop, theMoveList): 
      for move in self.bishopMoves:
        theMoveList = self.MoveListDiagonal(bishop, theMoveList, move[0], move[1])
      return theMoveList
      
    # Generate all the possible Rook moves
    def GenerateRookMoves(self, rook, theMoveList):  
      for move in self.rookMoves:
        theMoveList = self.MoveListCardinal(rook, theMoveList, move[0], move[1])
      return theMoveList
     
    # Generate all the possible Queen moves
    def GenerateQueenMoves(self, queen, theMoveList):  
      for move in self.rookMoves:
        theMoveList = self.MoveListCardinal(queen, theMoveList, move[0], move[1])
      for move in self.bishopMoves:
        theMoveList = self.MoveListDiagonal(queen, theMoveList, move[0], move[1])
      return theMoveList
    
    # Generate all the possible King moves
    def GenerateKingMoves(self, king, theMoveList):
      for move in self.kingMoves:
        newMove = states.Action(self.ChangeFile(king.file, move[0]), self.ChangeRank(king.rank, move[1]), king)
        validity,reason = self.CheckValidSpace(newMove.to[0], newMove.to[1], king)
        if validity == "Valid" or validity == "Opponent":
          if validity == "Opponent":
            newMove.hasCaptured = True
            newMove.capturedPiece = reason
          theMoveList.append(newMove)
      theMoveList = self.Castle(theMoveList)
      return theMoveList
    
    # Generates all possible valid moves for a player, given a board
    def GenerateAllValidMoves(self, board, id):
      theMoveList = []
      
      self.generators = { }
      self.currentBoard = board
      self.playerAtPlay = id
      
      for name in self.pieceNames:
        for piece in self.pieceDict[name][id]:
          if piece.captured is False:
            theMoveList = self.generatorDict[name](piece, theMoveList)
          
      return theMoveList
    
    # Returns the single-character code for the piece
    def GetPieceCode(self, piece):
      code = piece.type[0]
      if piece.type == "Knight":
        code = "N"
      if piece.owner.id == "1":
        code = code.lower()
      return code
      
    def GetPieceCode2(self, piece, name, attacked, friendlyFire=False):
      # Infer the player based on letter case
      # Should return True if we have found the designated enemy 
     
      if piece == '.' or piece == None:
        return False
        
      n = name[0]
      if name == self.KNIGHT and self.playerAtPlay == self.player.id:
        n = 'N'
      elif name == self.KNIGHT and self.playerAtPlay == self.player.other_player.id:
        n = 'n'
      
      # print(piece, attacked)
      
      # Friendly fire means we are checking to see if a piece is protected by its own team.
      # Otherwise check to see if a piece is under attack by the opposing team.
      if friendlyFire == True:
        if piece == n.upper() and attacked == attacked.upper():
          return True
        if piece == n.lower() and attacked == attacked.lower():
          return True
      else:
        # If the piece is black and the king is white, check!
        if piece == n.lower() and attacked == attacked.upper():
          # print(piece, king)
          # print("Check 1")
          return True
          
        # If the piece is white and the king is black, check!
        if piece == n.upper() and attacked == attacked.lower():
          # print(piece, king)
          # print("Check 2")
          return True
      
      return False
    
    def EnPassant(self, pawn, theMoveList):
      # Take place immediately after a pawn has been moved two spaces
      if len(self.game.moves) > 0 and self.game.moves[-1].piece.type == self.PAWN:
        if self.game.moves[-1].to_rank == 4 and self.game.moves[-1].from_rank == 2 or self.game.moves[-1].to_rank == 5 and self.game.moves[-1].from_rank == 7:
          if abs(self.GetFileIndex(pawn.file) - self.GetFileIndex(self.game.moves[-1].to_file)) == 1:
            if self.game.moves[-1].from_rank == pawn.rank:
              newMove = states.Action(self.game.moves[-1].to_file, self.ChangeRank(self.game.moves[-1].to_rank, 1), pawn, "e.p.")
              validity,reason = self.CheckValidSpace(newMove.to[0], newMove.to[1], pawn)
              if validity == "Valid" or validity == "Opponent":
                if validity == "Opponent":
                  newMove.hasCaptured == True
                  newMove.capturedPiece = reason
                theMoveList.append(newMove)
            
      return theMoveList

    #TODO: Fix some things here
    def Castle(self, theMoveList):
      
      # Get the rank for the first row based on the player
      if self.GetRankDirection() == 1:
        theRank = 1
      else:
        theRank = 8
        
      hasCastledKingside = False
      hasCastledQueenside = False
    
      for move in self.game.moves:
        # Don't castle if the king has moved previously
        if move.piece.type == self.KING and move.piece.owner == self.player:
          return theMoveList
        
        # Don't castle if the rook in question has been moved
        if move.piece.type == self.ROOK and move.piece.owner == self.player:
          if move.from_file == 'a' and move.from_rank == theRank:
            hasCastledQueenside = True
          if move.from_file == 'h' and move.from_rank == theRank:
            hasCastledKingside = True
      
      # Add queenside castling to the move list if applicable
      if hasCastledQueenside is False:
        validity1,reason = self.CheckValidSpace('d', theRank, self.pieceDict[self.KING][self.player.id][0])
        validity2,reason = self.CheckValidSpace('c', theRank, self.pieceDict[self.KING][self.player.id][0])
        if validity1 == "Valid" and validity2 == "Valid":
          theMoveList.append( states.Action('c', theRank, self.pieceDict[self.KING][self.player.id][0], "0-0-0") )
      
      # Add kingside castling to the move list if applicable      
      if hasCastledKingside is False:
        validity1,reason = self.CheckValidSpace('f', theRank, self.pieceDict[self.KING][self.player.id][0])
        validity2,reason = self.CheckValidSpace('g', theRank, self.pieceDict[self.KING][self.player.id][0])
        if validity1 == "Valid" and validity2 == "Valid":
          theMoveList.append( states.Action('g', theRank, self.pieceDict[self.KING][self.player.id][0], "0-0") )
          
      return theMoveList
            
                
    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        print("-----")
        print("Turn " + str(self.game.current_turn))
        print("-----")
        
        # If we promoted a piece on the last move, add that piece to our list of pieces
        if self.promotedPreviousMove is True:
          for name in self.pieceNames:
            self.pieceDict[name] = {
              self.player.id: [piece for piece in self.player.pieces if piece.type == name], 
              self.player.other_player.id: [piece for piece in self.player.other_player.pieces if piece.type == name]
            }
          self.promotedPreviousMove = False

        # Create the current board
        currentBoard = []
        for i in range(0,8):
          currentBoard.append([])
          for j in range(0,8):
            currentBoard[i].append('.')

        for piece in self.game.pieces:
          i = self.GetFileIndex(piece.file)
          currentBoard[piece.rank-1][i] = self.GetPieceCode(piece)

        # Create the current game state and make a random valid move
        currentState = states.State(currentBoard, self.player.id, None, 0)
        currentState.turnsToDraw = self.game.turns_to_draw
        self.playerAtPlay = self.player.id
        currentState.actionSet = self.GenerateAllValidMoves(currentBoard, self.player.id)
        # currentState.printBoard()
        
        # print("Board", size.getsize(currentBoard))
        # print("State", size.getsize(currentState))
        
        # Pick a random move from the list of valid moves for this turn
        if len(currentState.actionSet) > 0:
          minimax = tlhtqsidabdlmm.TLHTQSIDABDLMM(self, self.player.time_remaining*0.1, self.transpTable, self.historyTable)
          bestMove = minimax.Search(currentState, self.player.id) # random.choice(currentState.actionSet)
          # print("Turns to stalemate: ", self.game.turns_to_draw)
          # bestMove = random.choice(currentState.actionSet)
        else:
          print("There are no moves.")
          return True
        

        #if len(self.game.moves) > 0:
        #  print("Opponent's Last Move: '" + self.game.moves[-1].san + "'")
        #  print("Time Remaining: " + str(self.player.time_remaining/1000000000) + " sec")
        # print(currentState.actionSet)
        
        # Get a list of moves for the chosen piece
        bestMoveList = []
        for move in currentState.actionSet:
          if move.piece == bestMove.piece:
            bestMoveList.append(move)
        
        #for move in bestMoveList:
        #  print(move)
             
        if bestMove is None:
          print("There are no moves.")
          return True
          
       #  print(bestMove)
        if bestMove.promotedPiece is None:
          bestMove.piece.move(bestMove.to[0], bestMove.to[1])
        else:
          bestMove.piece.move(bestMove.to[0], bestMove.to[1], bestMove.promotedPiece)
          self.promotedPreviousMove = True
        
        # print("End of my turn.")
        return True # to signify we are done with our turn.
