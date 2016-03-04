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

    def CheckValidPawnMove(self, newFile, newRank):
      # Check to see if there is another of our pieces already at this position
      print("Checking " + str(newFile) + str(newRank))
      
      return True
      
    def GetRandomPawn(self):
      pawns = []
      for piece in self.player.pieces:
        if piece.type == "Pawn":
          pawns.append(piece)    
      return random.choice(pawns)
      
    def MovePawnUpOneRank(self, pawn):
    
      # Make sure we are moving a pawn.
      if pawn.type != "Pawn":
        return False
        
      # Make sure we do not move the pawn into an occupied space.
      newFile = pawn.file
      newRank = pawn.rank+self.player.rank_direction
      for piece in self.game.pieces:
        if piece.file == newFile and piece.rank == newRank:
          return False
      
      # Move the pawn.
      pawn.move(newFile, newRank)
      return True

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
        while(validMove is False):
          thePiece = random.choice(self.player.pieces)
          theMove = random.randint(0,1)
          if theMove == 0:
            validMove = self.MovePawnUpOneRank(thePiece)
          if theMove == 1:
            validMove = self.MovePawnUpOneRank(thePiece)

        print("End of my turn.")
        return True # to signify we are done with our turn.
