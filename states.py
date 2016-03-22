class State():
  __slots__ = ['board', 'actionTaken', 'actionSet', 'playerID', 'stateID', 'utility', 'hasCastled', 'turnsToDraw', 'previousPiece']
  
  def __init__(self, board, playerID, actionTaken, utility, castled=False):
    self.board = board
    self.actionTaken = actionTaken
    self.playerID = playerID
    self.actionSet = None
    self.stateID = self.assignID()
    self.hasCastled = castled
    self.utility = utility
    self.turnsToDraw = 100
    self.previousPiece = None

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
    return
    
class Action():
  __slots__ = ['to', 'frm', 'piece', 'notes', 'hasCaptured', 'capturedPiece', 'hasPromoted', 'promotedPiece']
  
  def __init__(self, newFile, newRank, piece, notes="none", hasCaptured=False, capturedPiece=None):
    self.to = (newFile, newRank)
    self.frm = (piece.file, piece.rank)
    self.piece = piece
    self.notes = notes
    self.hasCaptured = hasCaptured
    self.capturedPiece = capturedPiece
    self.hasPromoted = False
    self.promotedPiece = None
        
  def __repr__(self):
    return self.__str__()
    
  def __str__(self):
    oldTile = (str(self.frm[0]) + str(self.frm[1]))
    newTile = (str(self.to[0]) + str(self.to[1]))
    letter = self.piece.type[0]
    if self.piece.type == "Knight":
      letter = "N"
    if self.piece.type == "Pawn":
      letter = ""
      
    if self.notes == "0-0-0" or self.notes == "0-0":
      return letter + oldTile + " " + self.notes
    else:
      capture = ""
      if self.hasCaptured == True:
        capture = "x"
      ep = ""
      if self.notes == "e.p.":
        ep = "e.p."
        
      promote = ""
      if self.hasPromoted == True and self.promotedPiece is not None:
        promote = "=" + self.promotedPiece[0]
        if self.promotedPiece == "Knight":
          promote = "=" + "N"
      
    return letter + oldTile + " " + letter + capture + newTile + ep + promote