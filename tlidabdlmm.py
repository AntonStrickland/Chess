#Name: Anton Strickland
#CS5400 Game Project 3
import sys
import states
import random
import time

class TLIDABDLMM():

  __slots__ = ['PieceValue', 'MoveGenerator', 'totalNodes', 'actionSet', 'playerID', 'startTime', 'timeLimit', 'TranspositionTable']

  def __init__(self, generator, t):
    self.totalNodes = 3
    self.MoveGenerator = generator
    self.startTime = 0
    self.timeLimit = t
    self.PieceValue = {}
    self.PieceValue['.'] = 0
    self.PieceValue['p'] = 1
    self.PieceValue['n'] = 3
    self.PieceValue['b'] = 3
    self.PieceValue['r'] = 5
    self.PieceValue['q'] = 9
    self.PieceValue['k'] = 100
    self.TranspositionTable = {}
    
  def Search(self, rootNode, id):
    # Test with a depth limit of 3
    # rootNode.printBoard()
    self.playerID = id
    self.startTime = time.time()
    depthLimit = 2
    bestFound = None
    bestU = -1*sys.maxsize
    for depth in range(0,depthLimit):
      # print("Current Depth:", depth)
      self.totalNodes = 1
      alpha = -1*sys.maxsize
      beta = sys.maxsize
      result,u = self.MiniMaxDecision(rootNode, depth, alpha, beta)
      
      if u > bestU:
        bestFound = result
        
      if time.time() - self.startTime >= self.timeLimit/1000000000:
        # print("Best action found: ", bestFound)
        return bestFound
        
      # print("Best action found: ", bestFound)
      # print(self.totalNodes)
    return bestFound
    
  def MiniMaxDecision(self, initialState, depth, alpha, beta):
  
    terminalTest = self.TerminalTest(depth, initialState)
    if terminalTest is not None:
      return terminalTest, -1*sys.maxsize
      
    # print("MINIMAX: ", depth, initialState.actionTaken, len(initialState.actionSet))
    # print(initialState.actionSet)
    v = -1*sys.maxsize
    prev = v
    a = None
    for action in initialState.actionSet:
      mm = self.MinValue(self.Result(initialState, action), depth-1, alpha, beta)
      # self.UnapplyMove(initialState, action)
      v = max(v, mm)
      if v > prev:
        a = action
        prev = v
        # print("New Utility: ", v, "Action: ", a)
      elif mm == prev:
        # 50% chance to choose current action if same utility as the best
        if random.random() > 0.5:
          a = action
          # print("Random switch! New Utility: ", v, "Action: ", a)
    # print("Depth: ", depth, "Utility: ", v, "Action: ", a)
    return a,v

  def MinValue(self, state, depth, alpha, beta):
    
    terminalTest = self.TerminalTest(depth, state)
    if terminalTest is not None:
      return terminalTest
      
    # print("MIN: ", depth, state.actionTaken, len(state.actionSet))
    # print(state.actionSet)
    v = sys.maxsize
    for action in state.actionSet:
      v = min(v, self.MaxValue(self.Result(state, action), depth-1, alpha, beta))
      # self.UnapplyMove(state, action)
      if v <= alpha:
        # print("Prune min", alpha, v)
        return v
      beta = min(beta, v)
    return v
    
  def MaxValue(self, state, depth, alpha, beta):
    
    terminalTest = self.TerminalTest(depth, state)
    if terminalTest is not None:
      return terminalTest

    # print("MAX: ", depth, state.actionTaken, len(state.actionSet))
    # print(state.actionSet)
    v = -1*sys.maxsize
    for action in state.actionSet:
      v = max(v, self.MinValue(self.Result(state, action), depth-1, alpha, beta))
      # self.UnapplyMove(state, action)
      if v >= beta:
        # print("Prune max", beta, v)
        return v
      alpha = max(alpha, v)
    return v
    
    
  def TerminalTest(self, depth, state):
  
    # Time limit reached?
    if time.time() - self.startTime >= self.timeLimit/1000000000:
      # print("time limit reached!", time.time() - self.startTime, self.timeLimit/1000000000)
      return -1*sys.maxsize
        
    if depth <= 0:
      if state.stateID not in self.TranspositionTable:
        self.TranspositionTable[state.stateID] = self.Utility(state)
      return self.TranspositionTable[state.stateID]
      
    if self.CheckIfInCheckMate(state):
      if state.stateID not in self.TranspositionTable:
        self.TranspositionTable[state.stateID] = sys.maxsize
      return self.TranspositionTable[state.stateID]
      
    # Avoid draw where you have no moves left but not in check (stalemate)
    if len(state.actionSet) == 0:
      return -1*sys.maxsize
      
    # Avoid draw where in 50 moves no pawn has moved or piece captured
    # print("TurnstoDraw:", state.turnsToDraw)
    if state.turnsToDraw <= 1:
      return -1*sys.maxsize
      
    # Avoid draw where not enough pieces (K vs. K, K vs. KB, K vs. KN, KB vs. KB)   
    if self.IsNotEnoughPieces(state):
      return -1*sys.maxsize
      
    # Avoid draw where threefold repetition
    if self.IsThreeFoldRepetition(state):
      return -1*sys.maxsize
      
    return None
    
  def CheckIfInCheckMate(self, state):
    # If this is the opponent's turn, then check if they are in check and have no moves available
    if self.MoveGenerator.playerAtPlay == self.MoveGenerator.player.other_player.id:
      
      # Look for the king's new position and see if he is in check or not (with a reason why)
      isCheck = False
     
      kingCode = self.MoveGenerator.pieceDict[self.MoveGenerator.KING][self.MoveGenerator.player.other_player.id][0]
      theirKing = self.MoveGenerator.GetPieceCode(kingCode)
      for x in range(0,8):
          for y in range(0,8):
            if state.board[x][y] == theirKing:
              # print(x, y, theirKing, self.MoveGenerator.playerAtPlay)
              isCheck,reason = self.MoveGenerator.CheckIfUnderAttack(state.board, y, x, state.board[x][y])
        
      if isCheck == True and state.actionSet == None:
        # print("Checkmate!!!")
        return True
        
    return False
    
  # Returns a new state when given an action and a current state
  def Result(self, state, action):
  
    
    # Create a new board to simulate the next turn
    newBoard = []
    for x in range(0, 8):
      newBoard.append([])
      for y in range(0, 8):
        newBoard[x].append(state.board[x][y])
    
    '''
    # Apply the move to the board
    state.previousPiece = state.board[action.frm[1]-1][self.MoveGenerator.GetFileIndex(action.frm[0])]
    state.board[action.frm[1]-1][self.MoveGenerator.GetFileIndex(action.frm[0])] = '.'
    state.board[action.to[1]-1][self.MoveGenerator.GetFileIndex(action.to[0])] = self.MoveGenerator.GetPieceCode(action.piece)'''

    state.previousPiece = state.board[action.frm[1]-1][self.MoveGenerator.GetFileIndex(action.frm[0])]
    newBoard[action.frm[1]-1][self.MoveGenerator.GetFileIndex(action.frm[0])] = '.'
    newBoard[action.to[1]-1][self.MoveGenerator.GetFileIndex(action.to[0])] = self.MoveGenerator.GetPieceCode(action.piece)
    
    self.MoveGenerator.SwitchPlayerAtPlay(state.playerID)
    newState = states.State(newBoard, self.MoveGenerator.playerAtPlay, action, self.TranspositionTable[state.stateID])
    
    # Adjust the turns remaining to a draw
    if action.piece.type == self.MoveGenerator.PAWN or action.hasCaptured == True or action.notes == "e.p.":
      newState.turnsToDraw = 100
    else:
      newState.turnsToDraw -= 1
    
    newState.actionSet = self.MoveGenerator.GenerateAllValidMoves(newBoard, self.MoveGenerator.playerAtPlay)
    return newState
    
  def UnapplyMove(self, state, action):
    # Unapply the move to the board
    state.board[action.to[1]-1][self.MoveGenerator.GetFileIndex(action.to[0])] = state.previousPiece
    state.board[action.frm[1]-1][self.MoveGenerator.GetFileIndex(action.frm[0])] = self.MoveGenerator.GetPieceCode(action.piece)
    return
    
  # Avoid draw where not enough pieces (K vs. K, K vs. KB, K vs. KN, KB vs. KB)   
  def IsNotEnoughPieces(self, state):
  
    knightsLower = 0
    knightsUpper = 0
    bishopsUpper = 0
    bishopsLower = 0
    bishopSquareLower = (0,0)
    bishopSquareUpper = (0,0)
    lowerPieces = []
    upperPieces = []
  
    for x in range(0, len(state.board)):
      for y in range(0, len(state.board)):
        if state.board[x][y] != '.':
          if state.board[x][y] == state.board[x][y].lower():
            lowerPieces.append(state.board[x][y])
            if state.board[x][y] == 'B':
              bishopsUpper += 1
              bishopSquareUpper = (x,y)
            elif state.board[x][y] == 'N':
              knightsUpper += 1
          if state.board[x][y] == state.board[x][y].upper():
            upperPieces.append(state.board[x][y])
            if state.board[x][y] == 'b':
              bishopsLower += 1
              bishopSquareLower = (x,y)
            elif state.board[x][y] == 'n':
              knightsLower += 1
            
    # Only check if 2 or less pieces remaining on each side
    if len(lowerPieces) > 2 or len(upperPieces) > 2:
      return False
      
    # King vs. King
    if len(lowerPieces) == 1 and len(upperPieces) == 1:
      return True
    
    # King vs. King and Bishop, or King vs. King and Knight
    if bishopsLower != bishopsUpper or knightsLower != knightsUpper:
      return True
    
    # King and Bishop vs. King and Bishop, where bishops are on same colored squares
    if (bishopSquareLower[0] + bishopSquareLower[1]) % 2 == (bishopSquareUpper[0] + bishopSquareUpper[1]) % 2:
      return True
      
    return False
      

  def IsThreeFoldRepetition(self, state):
    m = self.MoveGenerator.game.moves
    if len(m) >= 8 and state.turnsToDraw <= 92:
      # print(len(m),state.turnsToDraw)
      if self.IsMoveEqual(m[-1],m[-8]) and self.IsMoveEqual(m[-2],m[-7]):
        if self.IsMoveEqual(m[-3],m[-6]) and self.IsMoveEqual(m[-4],m[-5]):
          # print("Threefold repetition detected!")
          return True
    return False
    
  def IsMoveEqual(self, move1, move2):
    if move1.to_file == move2.from_file and move1.to_rank == move2.from_rank:
      if move2.to_file == move1.from_file and move2.to_rank == move1.from_rank:
        return True
    return False

  def Utility(self, state):
 
    u = 0
    
    # States which are further away from a draw are better
    u += state.turnsToDraw
         
    # For every piece on the board, add the piece's value to utility
    for x in range(0, len(state.board)):
      for y in range(0, len(state.board)):
        if self.playerID == "1":
          # If we are looking at a lowercase piece and we are black
          if state.board[x][y].islower():
            u += self.PieceValue[state.board[x][y]]
          else:
            u -= self.PieceValue[state.board[x][y].lower()] 
        else:
          # If we are looking at an uppercase piece and we are white
          if state.board[x][y].isupper():
            u += self.PieceValue[state.board[x][y].lower()]
          else:
            u -= self.PieceValue[state.board[x][y]]  
    
    #if state.actionTaken is not None and u > 98:
    #  print(u, state.actionTaken)
    return u