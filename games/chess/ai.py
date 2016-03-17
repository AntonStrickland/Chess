#Name: Anton Strickland
#CS5400 Game Project 2

from joueur.base_ai import BaseAI
import random
import datetime
import sys
# import movegen
# import iddlmm
import size
import states


class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    class IDDLMM():

      __slots__ = ['PieceValue', 'MoveGenerator', 'totalNodes', 'actionSet', 'playerID']

      def __init__(self, generator):
        self.totalNodes = 1
        self.MoveGenerator = generator
        self.PieceValue = {}
        self.PieceValue['.'] = 0
        self.PieceValue["p"] = 1
        self.PieceValue["n"] = 3
        self.PieceValue["b"] = 3
        self.PieceValue["r"] = 5
        self.PieceValue["q"] = 9
        self.PieceValue["k"] = 0
        
      def Search(self, rootNode, id):
        # Test with a depth limit of 3
        self.playerID = id
        for depth in range(0,3):
          print(depth)
          self.totalNodes = 1
          result = self.MiniMaxDecision(rootNode, depth)
          print(self.totalNodes)
        return result
        
      def MiniMaxDecision(self, initialState, depth):
        initialState.printBoard()
        if self.TerminalTest(initialState, depth):
          return self.Utility(initialState)
          
        print("MINIMAX: ", depth, initialState.actionTaken, len(initialState.actionSet))
        # print(initialState.actionSet)
        v = -1*sys.maxsize
        prev = v
        a = None
        for action in initialState.actionSet:
          v = max(v, self.MinValue(self.Result(initialState, action), depth-1))
          if v > prev:
            a = action
            prev = v
            print("New Utility: ", v, "Action: ", a)
          elif v == prev:
            if random.random() > 1.0:
              print("Random switch!")
              a = action
        print("Utility: ", v, "Action: ", a)
        return a
        
      def MinValue(self, state, depth):
        
        # state.printBoard()
        if self.TerminalTest(state, depth):
          u = self.Utility(state)
          #if u != 0:
          #  print("Utility: ", u, "Prev:", state.utility, "Action:", state.actionTaken, "Depth:", depth)
          return u
          
        print("MIN: ", depth, state.actionTaken, len(state.actionSet))
        # print(state.actionSet)
        v = sys.maxsize
        for action in state.actionSet:
          v = min(v, self.MaxValue(self.Result(state, action), depth-1))
        return v
        
      def MaxValue(self, state, depth):
        
        # state.printBoard()
        if self.TerminalTest(state, depth):
          u = self.Utility(state)
          #if u != 0:
          #  print("Utility: ", u, "Prev:", state.utility, "Action:", state.actionTaken, "Depth:", depth)
          return u
          
        print("MAX: ", depth, state.actionTaken, len(state.actionSet))
        # print(state.actionSet)
        v = -1*sys.maxsize
        for action in state.actionSet:
          v = max(v, self.MinValue(self.Result(state, action), depth-1))
        return v

      def TerminalTest(self, state, depth):
        # Check to see if we have reached the depth limit
        if depth <= 0:
          return True
        return self.CheckIfInCheckMate(state)
        
      def CheckIfInCheckMate(self, state):
        # Look for the king's new position and see if he is in check or not (with a reason why)
        isCheck = False
        for x in range(0,8):
            for y in range(0,8):
              if state.board[x][y] == self.MoveGenerator.GetPieceCode(self.MoveGenerator.pieceDict[self.MoveGenerator.KING][self.MoveGenerator.player.id][0]):
                isCheck,reason = self.MoveGenerator.CheckIfInCheck(state.board[:], y, x)
        if isCheck == True and state.actionSet == None:
          return True
        
      # Returns a new state when given an action and a current state
      def Result(self, state, action):
        # Create a new board to simulate the next turn
        newBoard = []
        for x in range(0, 8):
          newBoard.append([])
          for y in range(0, 8):
            newBoard[x].append(state.board[x][y])
        
        newBoard[action.frm[1]-1][self.MoveGenerator.GetFileIndex(action.frm[0])] = '.'
        newBoard[action.to[1]-1][self.MoveGenerator.GetFileIndex(action.to[0])] = self.MoveGenerator.GetPieceCode(action.piece)
        
        newID = "0"
        if state.playerID == "0":
          newID = "1"
        
        newState = states.State(newBoard, newID, action, self.Utility(state))
        self.MoveGenerator.playerAtPlay = newID
        newState.actionSet = self.MoveGenerator.GenerateAllValidMoves(newBoard, newID)
        return newState

      def Utility(self, state):
        u = state.utility
        # For every piece on the board, add the piece's value to utility
        for x in range(0, len(state.board)):
          for y in range(0, len(state.board)):
            if self.playerID == "1":
              if state.board[x][y].lower() == state.board[x][y]:
                u += self.PieceValue[state.board[x][y]]
              else:
                u -= self.PieceValue[state.board[x][y].lower()] 
            else:
              if state.board[x][y].upper() == state.board[x][y]:
                u += self.PieceValue[state.board[x][y].lower()]
              else:
                u -= self.PieceValue[state.board[x][y]]  
        
        return u
 
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
        self.randomSeed = datetime.datetime.now()
        
        self.playerAtPlay = self.player.id
        
        random.seed(self.randomSeed)
        
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
        print("Seconds taken: " + str((self.startTime - self.player.time_remaining)/1000000000))
        print("Turns taken: " + str(self.game.current_turn))
        print("Random seed: " + str(self.randomSeed))
 
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
    
    def CheckIfInCheck(self, board, kingFile, kingRank):
    
      # print("---------------")
      
      # newState = State(board, self.player.id, None)
      # newState.printBoard()
      piece = self.GetPieceAtBoard(board, kingFile - 1, kingRank + self.GetRankDirection())
      if piece is not None and self.GetPieceCode2(piece, self.PAWN):
        return True, self.PAWN
      
      piece = self.GetPieceAtBoard(board, kingFile + 1, kingRank + self.GetRankDirection())
      if piece is not None and self.GetPieceCode2(piece, self.PAWN):
        return True, self.PAWN
          
      for move in self.knightMoves:
        piece = self.GetPieceAtBoard(board, kingFile + move[0], kingRank + move[1])
        if piece is not None and self.GetPieceCode2(piece, self.KNIGHT):
          return True, self.KNIGHT

      for move in self.rookMoves:
        if self.CheckCardinally(board, kingFile, kingRank, move[0], move[1]):
          return True, self.ROOK

      for move in self.bishopMoves:
        if self.CheckDiagonally(board, kingFile, kingRank, move[0], move[1]):
          return True, self.BISHOP
          
      for move in self.kingMoves:
        piece = self.GetPieceAtBoard(board, kingFile + move[0], kingRank + move[1])
        if piece is not None and self.GetPieceCode2(piece, self.KING):
          return True, self.KING
          
      return False, None
    
    # Checks a board cardinally to see if the king is in check    
    def CheckCardinally(self, board, file, rank, step, direction):
      currentFile = file
      currentRank = rank

      newState = states.State(board[:], self.player.id, None, 0)
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
        if self.GetPieceCode2(piece, self.QUEEN) or self.GetPieceCode2(piece, self.ROOK):
          # print("Don't move to " + str(file) + str(rank) + self.ROOK)
          return True
        elif piece != '.':
          return False
        
      return False
    
    # Checks a board diagonally to see if the king is in check
    def CheckDiagonally(self, board, file, rank, step1, step2):
    
      currentFile = file
      currentRank = rank
      newState = states.State(board[:], self.player.id, None, 0)
      while currentFile is not None and currentRank is not None:

        currentFile = currentFile + step1
        currentRank = currentRank + (self.GetRankDirection() * step2)
        
        if currentFile >= len(board) or currentRank >= len(board) or currentFile < 0 or currentRank < 0:
          return False
          
        piece = board[currentRank][currentFile]
        
        if self.GetPieceCode2(piece, self.QUEEN) or self.GetPieceCode2(piece, self.BISHOP):
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
          validity = self.CheckValidSpace(newFile, newRank, pawn)
          if validity == "Opponent":
            if newRank != 1 and newRank != 8:
              theMoveList.append( states.Action(newFile, newRank, pawn, "capture") )
            else:
              theMoveList.append( states.Action(newFile, newRank, pawn, "promotion", self.QUEEN))
              theMoveList.append( states.Action(newFile, newRank, pawn, "promotion", self.ROOK))
              theMoveList.append( states.Action(newFile, newRank, pawn, "promotion", self.BISHOP))
              theMoveList.append( states.Action(newFile, newRank, pawn, "promotion", self.KNIGHT))
      return theMoveList
      
    def MovePawnUpOneRank(self, pawn, theMoveList):
    
      # Make sure we do not move the pawn into an occupied space.
      newFile = pawn.file
      newRank = self.ChangeRank(pawn.rank, 1)
      # print(str(self.player.id) + " moved from " + str(pawn.file) + str(pawn.rank) + " to " + str(newFile) + str(newRank))
      
      # Make sure the space is valid. Also consider pawn promotions.
      validity = self.CheckValidSpace(newFile, newRank, pawn)
      if validity == "Valid":
        if newRank != 1 and newRank != 8:
          theMoveList.append( states.Action(newFile, newRank, pawn, "up one") )
        else:
          theMoveList.append( states.Action(newFile, newRank, pawn, "promotion", self.QUEEN))
          theMoveList.append( states.Action(newFile, newRank, pawn, "promotion", self.ROOK))
          theMoveList.append( states.Action(newFile, newRank, pawn, "promotion", self.BISHOP))
          theMoveList.append( states.Action(newFile, newRank, pawn, "promotion", self.KNIGHT))
        
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
      print(oldFile, diff, new)
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
      
      # If the space is out of bounds, return False
      if newFile is None or newRank is None:
        return "Invalid"
    
      # Make sure we do not move the piece into an occupied space.
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          # print(piece.owner.id, self.playerAtPlay)
          if piece.owner.id == self.playerAtPlay:
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
              isCheck,reason = self.CheckIfInCheck(newBoard[:], y, x)
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
          newMove = states.Action(self.ChangeFile(currentFile, step), currentRank, piece)
        else:
          newMove = states.Action(currentFile, self.ChangeRank(currentRank, step), piece)
          
        # Check to make sure this space is valid
        validity = self.CheckValidSpace(newMove.to[0], newMove.to[1], piece)
        
        if validity == "Valid":
          newMoves.append(newMove)
          currentFile = newMove.to[0]
          currentRank = newMove.to[1]
        elif validity == "Opponent":
          newMove.notes = "capture"
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
        validity = self.CheckValidSpace(newMove.to[0], newMove.to[1], piece)
       
        if validity == "Valid":
          newMoves.append(newMove)
          currentFile = newMove.to[0]
          currentRank = newMove.to[1]
        elif validity == "Opponent":
          newMove.notes = "capture"
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
        validity = self.CheckValidSpace(newMove.to[0], newMove.to[1], knight)
        if validity == "Valid" or validity == "Opponent":
          if validity == "Opponent":
            newMove.notes = "capture"
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
        validity = self.CheckValidSpace(newMove.to[0], newMove.to[1], king)
        if validity == "Valid" or validity == "Opponent":
          if validity == "Opponent":
              newMove.notes = "capture"
          theMoveList.append(newMove)
      theMoveList = self.Castle(theMoveList)
      return theMoveList
    
    # Generates all possible valid moves for a player, given a board
    def GenerateAllValidMoves(self, board, id):
      theMoveList = []
      
      self.generators = { }
      self.currentBoard = board[:]
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
      
    def GetPieceCode2(self, piece, name):
      # Infer the player based on letter case
      # Should return True if we have found the designated enemy 
      
      king = self.GetPieceCode(self.pieceDict[self.KING][self.player.id][0])
      n = name[0]
      if name == self.KNIGHT:
        n = 'N'

      if piece == '.':
        return False
      
      if piece == n.lower() and king == king.upper():
        return True
      if piece == n.upper() and king == king.lower():
        return True
      
      return False
    
    def EnPassant(self, pawn, theMoveList):
      # Take place immediately after a pawn has been moved two spaces
      if len(self.game.moves) > 0 and self.game.moves[-1].piece.type == self.PAWN:
        if self.game.moves[-1].to_rank == 4 and self.game.moves[-1].from_rank == 2 or self.game.moves[-1].to_rank == 5 and self.game.moves[-1].from_rank == 7:
          if abs(self.GetFileIndex(pawn.file) - self.GetFileIndex(self.game.moves[-1].to_file)) == 1:
            if self.game.moves[-1].from_rank == pawn.rank:
              newMove = states.Action(self.game.moves[-1].to_file, self.ChangeRank(self.game.moves[-1].to_rank, 1), pawn, "e.p.")
              validity = self.CheckValidSpace(newMove.to[0], newMove.to[1], pawn)
              if validity == "Valid" or validity == "Opponent":
                theMoveList.append(newMove)
            
      return theMoveList

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
        validity1 = self.CheckValidSpace('d', theRank, self.pieceDict[self.KING][self.player.id][0])
        validity2 = self.CheckValidSpace('c', theRank, self.pieceDict[self.KING][self.player.id][0])
        if validity1 == "Valid" and validity2 == "Valid":
          theMoveList.append( states.Action('c', theRank, self.pieceDict[self.KING][self.player.id][0], "0-0-0") )
      
      # Add kingside castling to the move list if applicable      
      if hasCastledKingside is False:
        validity1 = self.CheckValidSpace('f', theRank, self.pieceDict[self.KING][self.player.id][0])
        validity2 = self.CheckValidSpace('g', theRank, self.pieceDict[self.KING][self.player.id][0])
        if validity1 == "Valid" and validity2 == "Valid":
          theMoveList.append( states.Action('g', theRank, self.pieceDict[self.KING][self.player.id][0], "0-0") )
          
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

        # Create the current game state and make a random valid move
        print(self.player.id)
        if self.player.id == 1 or self.player.id == 0:
          print("number")
        currentState = states.State(currentBoard, self.player.id, None, 0)
        self.playerAtPlay = self.player.id
        currentState.actionSet = self.GenerateAllValidMoves(currentBoard, self.player.id)
        # currentState.printBoard()
        
        # print("Board", size.getsize(currentBoard))
        # print("State", size.getsize(currentState))
        
        if len(self.game.moves) > 0:
            print("Opponent's Last Move: '" + self.game.moves[-1].san + "'")
        print("Time Remaining: " + str(self.player.time_remaining) + " ns")
        
        # Pick a random move from the list of valid moves for this turn
        if len(currentState.actionSet) > 0:
          IDDLMM = self.IDDLMM(self)
          bestMove = IDDLMM.Search(currentState, self.player.id) # random.choice(currentState.actionSet)
          # bestMove = random.choice(currentState.actionSet)
        else:
          return True
        
        # Get a list of moves for the randomly chosen piece
        # bestMoveList = []
        # for move in currentState.actionSet:
        #   if move.piece == bestMove.piece:
        #     bestMoveList.append(move)
        
        print("-----")
        print("Turn " + str(self.game.current_turn))
        print("-----")
        #for move in currentState.actionSet:
        print(currentState.actionSet)
        
        if bestMove.promotion is None:
          bestMove.piece.move(bestMove.to[0], bestMove.to[1])
        else:
          bestMove.piece.move(bestMove.to[0], bestMove.to[1], bestMove.promotion)
        
        # self.stateHistory.append( self.Result(bestMove, currentState) )

       
        # print("End of my turn.")
        return True # to signify we are done with our turn.
