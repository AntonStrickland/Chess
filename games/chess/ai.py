#Name: Anton Strickland
#CS5400 Game Project 1

from joueur.base_ai import BaseAI
import random

class State():
  __slots__ = ['board', 'actionTaken', 'actionSet', 'stateID', 'hasCastled']
  
  def __init__(self, board, actionTaken, castled=False):
    self.board = board
    self.actionTaken = actionTaken
    self.actionSet = None
    self.stateID = ""
    self.hasCastled = castled

  def assignID(self):
    stateID = ""
    for square in self.board:
      stateID += str(square)
    self.stateID = stateID
    return
  
  # Print the board to the screen
  def printBoard(self):
    for f in range(9, -2, -1):
        output = ""
        if f == 9 or f == 0:
            output = "   +------------------------+"
        elif f == -1:
            output = "     a  b  c  d  e  f  g  h"
        else:
            output = " " + str(f) + " |"
            # fill in all the ranks with pieces at the current rank
            for r in range(0, len(self.board)):
                output += " " + self.board[f-1][r] + " "
            output += "|"
        print(output)
        
class Action():
  __slots__ = ['to', 'frm', 'piece', 'notes', 'promotion']
  
  def __init__(self, newFile, newRank, piece, notes="none", promotion=None):
    self.to = (newFile, newRank)
    self.frm = (piece.file, piece.rank)
    self.piece = piece
    self.notes = notes
    self.promotion = promotion
    
  def __str__(self):
    return str(self.piece.type) + " from " + str(self.frm) + " to " + str(self.to)
    
  def __repr__(self):
    if self.notes is not None:
      return str(self.piece.type) + " from " + str(self.frm) + " to " + str(self.to) + ": " + str(self.notes)
    else:
      return str(self.piece.type) + " from " + str(self.frm) + " to " + str(self.to)
    
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
        
        self.pieceNames = [self.PAWN, self.KNIGHT, self.BISHOP, self.ROOK, self.QUEEN, self.KING]
        
        self.currentBoard = []
        self.stateHistory = []
        
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
 

    # Checks if the king is in check by examining each possible enemy position.
    # First start at the king's position on the board, and work backwards.
    # If an enemy is encountered based on their attack pattern then we know we are in check.
    # (There are still some mysterious problems here, but there is not enough time to fix them.)
    
    def CheckIfInCheck(self, board, kingFile, kingRank):
    
      print("---------------")
      
      newState = State(board, None)
      newFile = self.ChangeFile2(kingFile, -1)
      newRank = self.ChangeRank2(kingRank, 1*self.player.rank_direction)
      if newFile is not None and newRank is not None:
        piece = board[newRank][newFile]
        # newState.board[newRank][newFile] = 'X'
        # newState.printBoard()
        if piece is not None and self.GetPieceCode2(piece, self.PAWN):
          return True, self.PAWN
      
      newState = State(board, None)
      newFile = self.ChangeFile2(kingFile, 1)
      newRank = self.ChangeRank2(kingRank, 1*self.player.rank_direction)
      if newFile is not None and newRank is not None:
        piece = board[newRank][newFile]
        newState.board[newRank][newFile] = 'X'
        # newState.printBoard()
        if piece is not None and self.GetPieceCode2(piece, self.PAWN):
          return True, self.PAWN
          
      for move in self.knightMoves:
        newState = State(board, None)
        newFile = self.ChangeFile2(kingFile, move[0])
        newRank = self.ChangeRank2(kingRank, move[1])
        print(newFile, newRank)
        if newFile is not None and newRank is not None:
          if newFile >= 0 and newFile < 8 and newRank >= 0 and newRank < 8:
            # print(newFile, newRank)
            piece = board[newRank][newFile]
            # print("added x", newFile, newRank)
            newState.board[newRank][newFile] = 'X'
            # newState.printBoard()
            if piece is not None and self.GetPieceCode2(piece, self.KNIGHT):
              return True, self.KNIGHT

      for move in self.rookMoves:
        if self.CheckCardinally(board, kingFile, kingRank, move[0], move[1]):
          return True, self.ROOK
    
      # print("test bishop")
      for move in self.bishopMoves:
        if self.CheckDiagonally(board, kingFile, kingRank, move[0], move[1]):
          return True, self.BISHOP
          
      for move in self.kingMoves:
        newFile = self.ChangeFile2(kingFile, move[0])
        newRank = self.ChangeRank2(kingRank, move[1])
        if newFile is not None and newRank is not None:
          if newFile >= 0 and newFile < 8 and newRank >= 0 and newRank < 8:
            piece = board[newRank][newFile]
            # newState.board[newRank][newFile] = 'X'
            # newState.printBoard()
            if piece is not None and self.GetPieceCode2(piece, self.KING):
              return True, self.KING
          
      return False, None
    
    # Checks a board cardinally to see if the king is in check    
    def CheckCardinally(self, board, file, rank, step, direction):
      currentFile = self.ChangeFile2(file, 0)
      currentRank = rank
      # print(currentFile)
      newState = State(board, None)
      while currentFile is not None and currentRank is not None:
        
        if direction == 'h':
          currentFile = currentFile + step
        else:
          currentRank = currentRank + (self.player.rank_direction * step)
        
        # If the square is off the board we are not in check
        if currentFile >= len(board) or currentRank >= len(board) or currentFile < 0 or currentRank < 0:
          return False
        
        # print(currentFile, currentRank, board[currentRank][currentFile])
        piece = board[currentRank][currentFile]
        #newState.board[currentRank][currentFile] = 'X'
        #newState.printBoard()
        # print(piece)
        
        # If we run into an enemy and it is a queen or rook we are in check
        if self.GetPieceCode2(piece, self.QUEEN) or self.GetPieceCode2(piece, self.ROOK):
          return True
        elif piece != '.':
          return False
        
      return False
    
    # Checks a board diagonally to see if the king is in check
    def CheckDiagonally(self, board, file, rank, step1, step2):
      currentFile = self.ChangeFile2(file, 0)
      currentRank = rank
      newState = State(board, None)
      while currentFile is not None and currentRank is not None:

        currentFile = currentFile + step1
        currentRank = currentRank + (self.player.rank_direction * step2)
        
        # print(currentFile, currentRank)
        if currentFile >= len(board) or currentRank >= len(board) or currentFile < 0 or currentRank < 0:
          return False
          
        piece = board[currentRank][currentFile]
        #newState.board[currentRank][currentFile] = 'X'
        #newState.printBoard()
        
        if self.GetPieceCode2(piece, self.QUEEN) or self.GetPieceCode2(piece, self.BISHOP):
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
          validity = self.CheckValidSpace(newFile, newRank, pawn)
          if validity == "Opponent":
            theMoveList.append( Action(newFile, newRank, pawn, "Capture") )
          
      return theMoveList
      
    def MovePawnUpOneRank(self, pawn, theMoveList):
    
      # Make sure we do not move the pawn into an occupied space.
      newFile = pawn.file
      newRank = self.ChangeRank(pawn.rank, 1)
      print(str(self.player.id) + " moved from " + str(pawn.file) + str(pawn.rank) + " to " + str(newFile) + str(newRank))
      
      # Make sure the space is valid. Also consider pawn promotions.
      validity = self.CheckValidSpace(newFile, newRank, pawn)
      if validity == "Valid":
        if newRank != 1 and newRank != 8:
          theMoveList.append( Action(newFile, newRank, pawn, "up one") )
        else:
          theMoveList.append( Action(newFile, newRank, pawn, "promotion", self.QUEEN))
          theMoveList.append( Action(newFile, newRank, pawn, "promotion", self.ROOK))
          theMoveList.append( Action(newFile, newRank, pawn, "promotion", self.BISHOP))
          theMoveList.append( Action(newFile, newRank, pawn, "promotion", self.KNIGHT))
        
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
      
      # Make sure the space is valid
      validity = self.CheckValidSpace(newFile, newRank, pawn)
      if validity == "Valid":
        theMoveList.append( Action(newFile, newRank, pawn, "up two") )
      
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
      if new >= 0 and new < len(self.files):
        return new
      else:
        return None
        
    # Changing files with chessboard-based arrays
    def ChangeRank(self, oldRank, diff):
      if oldRank is None:
        return None
      
      newRank = oldRank + (self.player.rank_direction * diff)
      if newRank > 0 and newRank < 9:
        return newRank
      else:
        return None
    
    # Changing ranks with zero-based arrays
    def ChangeRank2(self, oldRank, diff):
      if oldRank is None:
        return None
      
      newRank = oldRank + (self.player.rank_direction * diff)
      if newRank >= 0 and newRank < 8:
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

      # Create a new board to simulate the next turn
      newBoard = []
      for x in range(0, 8):
        newBoard.append([])
        for y in range(0, 8):
          newBoard[x].append(self.currentBoard[x][y])
      
      # Modify the board to pretend we've moved the piece we want to move
      newBoard[movingPiece.rank-1][self.GetFileIndex(movingPiece.file)] = '.'
      newBoard[newRank-1][self.GetFileIndex(newFile)] = self.GetPieceCode(movingPiece)
      
      # Look for the king's new position and see if he is in check or not (with a reason why)
      for x in range(0,8):
          for y in range(0,8):
            if newBoard[x][y] == self.GetPieceCode(self.pieceDict[self.KING][self.player.id][0]):
              isCheck,reason = self.CheckIfInCheck(newBoard, self.files[y], x)
              # print(reason)
              
      # If he is in check, return Invalid
      if isCheck is True:
        return "Invalid"
         
      return validType
      
    # Generate a list of moves by iterating cardinally over the board
    def MoveListCardinal(self, piece, newMoves, step, direction):
      currentFile = piece.file
      currentRank = piece.rank
      encounteredPiece = False
      
      # Keep iterating until we run into an enemy, one of our pieces, or leave the boundaries of the board
      while(encounteredPiece is False):

        # Either iterate horizontally or vertically
        if direction == 'h':
          newMove = Action(self.ChangeFile(currentFile, step), currentRank, piece)
        else:
          newMove = Action(currentFile, self.ChangeRank(currentRank, step), piece)
          
        # Check to make sure this space is valid
        validity = self.CheckValidSpace(newMove.to[0], newMove.to[1], piece)
        
        if validity == "Valid":
          newMoves.append(newMove)
          currentFile = newMove.to[0]
          currentRank = newMove.to[1]
        elif validity == "Opponent":
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
        newMove = Action(self.ChangeFile(currentFile, step1), self.ChangeRank(currentRank, step2), piece)
       
        # Check to make sure this space is valid
        validity = self.CheckValidSpace(newMove.to[0], newMove.to[1], piece)
       
        if validity == "Valid":
          newMoves.append(newMove)
          currentFile = newMove.to[0]
          currentRank = newMove.to[1]
        elif validity == "Opponent":
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
        newMove = Action(self.ChangeFile(knight.file, move[0]), self.ChangeRank(knight.rank, move[1]), knight)
        validity = self.CheckValidSpace(newMove.to[0], newMove.to[1], knight)
        if validity == "Valid" or validity == "Opponent":
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
        newMove = Action(self.ChangeFile(king.file, move[0]), self.ChangeRank(king.rank, move[1]), king)
        validity = self.CheckValidSpace(newMove.to[0], newMove.to[1], king)
        if validity == "Valid" or validity == "Opponent":
          theMoveList.append(newMove)
      theMoveList = self.Castle(theMoveList)
      return theMoveList
    
    # Generates all possible valid moves for a player, given a board
    def GenerateAllValidMoves(self, board, id):
      theMoveList = []
      
      self.generators = { }
      self.currentBoard = board[:]
      
      if self.player.id == "1":
        print("My piece type is lower")
      else:
        print("My piece type is upper")
      
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
      
    def GetPieceCode2(self, piece, name):
      # Infer the player based on letter case
      # Should return True if we have found the designated enemy 
      
      king = self.GetPieceCode(self.pieceDict[self.KING][self.player.id][0])
      n = name[0]
      if name == self.KNIGHT:
        n = 'N'

      if piece == '.':
        return False
      
      if piece == n.lower() and king != king.lower():
        return True
      if piece == n.upper() and king != king.upper():
        return True
      
      return False
      
    # Returns a new state when given an action and a current state
    def Result(self, action, state):
      newBoard = []
      for x in range(0, 8):
        newBoard.append([])
        for y in range(0, 8):
          newBoard[x].append(state.board[x][y])
          
      print(self.GetFileIndex(action.frm[0]), action.frm[1])
      newBoard[self.GetFileIndex(action.frm[0])][action.frm[1]-1] = '.'
      newBoard[self.GetFileIndex(action.to[0])][action.to[1]-1] = self.GetPieceCode(action.piece)
      
      newState = State(newBoard, action)

      return newState
    
    def EnPassant(self, pawn, theMoveList):
      # Take place immediately after a pawn has been moved two spaces
      if len(self.game.moves) > 0 and self.game.moves[-1].piece.type == self.PAWN:
        if self.game.moves[-1].to_rank == 4 and self.game.moves[-1].from_rank == 2 or self.game.moves[-1].to_rank == 5 and self.game.moves[-1].from_rank == 7:
          if abs(self.GetFileIndex(pawn.file) - self.GetFileIndex(self.game.moves[-1].to_file)) == 1:
            newMove = Action(self.game.moves[-1].to_file, self.ChangeRank(self.game.moves[-1].to_rank, 1), pawn, "e.p.")
            validity = self.CheckValidSpace(newMove.to[0], newMove.to[1], pawn)
            if validity == "Valid" or validity == "Opponent":
              theMoveList.append(newMove)
            
      return theMoveList

    def Castle(self, theMoveList):
      
      # Get the rank for the first row based on the player
      if self.player.rank_direction == 1:
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
        validity1 = self.CheckValidSpace('d', theRank, self.pieceDict[self.KING][self.player.id][0])
        validity2 = self.CheckValidSpace('c', theRank, self.pieceDict[self.KING][self.player.id][0])
        if validity1 == "Valid" and validity2 == "Valid":
          theMoveList.append( Action('c', theRank, self.pieceDict[self.KING][self.player.id][0], "0-0-0") )
      
      # Add kingside castling to the move list if applicable      
      if hasCastledKingside is False:
        validity1 = self.CheckValidSpace('f', theRank, self.pieceDict[self.KING][self.player.id][0])
        validity2 = self.CheckValidSpace('g', theRank, self.pieceDict[self.KING][self.player.id][0])
        if validity1 == "Valid" and validity2 == "Valid":
          theMoveList.append( Action('g', theRank, self.pieceDict[self.KING][self.player.id][0], "0-0") )
          
      return theMoveList
            
         
            
    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        
        # Create the current board
        currentBoard = []
        for i in range(0,8):
          currentBoard.append([])
          for j in range(0,8):
            currentBoard[i].append('.')
        
        for piece in self.game.pieces:
          i = self.GetFileIndex(piece.file)
          currentBoard[piece.rank-1][i] = self.GetPieceCode(piece)

        # Create the current game state and print it
        currentState = State(currentBoard, None)
        currentState.printBoard()
        
        if len(self.game.moves) > 0:
            print("Opponent's Last Move: '" + self.game.moves[-1].san + "'")
        print("Time Remaining: " + str(self.player.time_remaining) + " ns")
        
        # Make a valid random move
        currentState.actionSet = self.GenerateAllValidMoves(currentBoard, self.player.id)
       
        newList = []
        for m in currentState.actionSet:
          newList.append( m )
        print(newList)
        

        randomMove = random.choice(currentState.actionSet)
        currentState.printBoard()
        print("Moving " + str(randomMove))
        
        if randomMove.promotion is None:
          randomMove.piece.move(randomMove.to[0], randomMove.to[1])
        else:
          randomMove.piece.move(randomMove.to[0], randomMove.to[1], randomMove.promotion)
        
        self.stateHistory.append( self.Result(randomMove, currentState) )
        # print("Moved to: " + str(newFile) + str(newRank))
        print("End of my turn.")
        return True # to signify we are done with our turn.
