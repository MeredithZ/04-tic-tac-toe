#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a simple set of classes for playing Tic-Tac-Toe
according to the strategies laid out by Newell & Simon:
https://en.wikipedia.org/wiki/Tic-tac-toe

Note that this strategy is not necessarily optimal
since player 1 plays in the center instead of the corner.
With a game start with X0 O8, X could play at X1 and lose.

However, since the game begins with X4, it's self-consistent.
"""
__author__    = "Xinyuan Zhang & Lingfei Zhang"
__copyright__ = "Copyright 2017 You Again"
__email__     = "xinyuan@uchicago.edu & lingfeiz@uchicago.edu"

import sys
import random
from copy import deepcopy as dc


class player():
  """
  The player class contains its mark and a strategy for "moves."
  That strategy is specialized for human (input) and computer (N&S)
  classes, while the monkey class uses the player's random move.
  """

  def __init__(self, mark):
    """
    :param mark: the class simply knows its marker (X or O).
    """
    assert(mark in "XO")
    self.mark = mark
    self.other_mark = "XO"[mark == "X"]

  def move(self, match):
    """
    :param match: is an instance of the game class, for which to generate a move.
    """
    return random.choice([i for i in range(9) if not match.board[i]])


class monkey(player):
  """
  The monkey class is just a "cute" renaming of the player with random strategy.
  """

  def __init__(self, mark):
    """
    :param mark: the class simply knows its marker (X or O).
    """
    assert(mark in "XO")
    self.mark = mark
    self.other_mark = "XO"[mark == "X"]
  pass


class human(player):
  """
  The human player specializes the move for command-line input.
  """
  def move(self, match):
    """
    Method displays the game board and handles input for a human player.
    """
    m = -1
    while m not in range(9):
      try:
        print(match)
        m = int(input("Your move, {} [0-8]: ".format(self.mark)))
      except ValueError: continue
    return m


class computer(player):
  """
  This is the class to be specialized by students.
  """

  def move(self, match):
    """
    This is your specialization.
    I would suggest that you follow the strategy of N&S (wiki)
    https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
    but so long as you don't lose to monkeys, you can do what you want.
    """

    #1# Win if possible.
    #If the player has two in a row, they can place a third to get three in a row.
    win_cell = match.check_for_wins(self.mark)
    if win_cell is not None:
      return win_cell

    #2# Block wins, if possible.
    #If the opponent has two in a row, the player must play the third themselves to block the opponent.
    win_cell = match.check_for_wins(self.other_mark)
    if win_cell is not None:
      return win_cell

    #3# Fork.
    #Create an opportunity where the player has two threats to win (two non-blocked lines of 2).
    # X O X
    # - X O
    # - - -
    for i in range(9):

      hypo_match = dc(match)
      if hypo_match.board[i] is None:
        hypo_match.board[i] = self.mark
        cells = set()
        for three in hypo_match.threes:

          if sum(hypo_match.board[cell] == self.mark for cell in three) == 2:
            for cell in three:

              if hypo_match.board[cell] is None:
                cells.add(cell)

        if len(cells) == 2:
          return i

    #4# Force Defense.
    # For your OPPPONENT, get any potential twos.
    self_twos = match.check_for_twos(self.mark)
    # We'll now consider hypothetical games,
    # where we play in each of the "two" positions.
    for i in self_twos:                 # For each of these
      hypo_match = dc(match)          # create a copy of the game -- dc is deepcopy
      hypo_match.board[i] = self.mark # try playing there.
      # Now look for the win implied by your "two".
      # Your opponent would have to play here.
      w = hypo_match.check_for_wins(self.mark)
      # For your OPPPONENT, get any potential twos.
      hypo_twos = hypo_match.check_for_twos(self.other_mark)
      # If your potential win is not just a two for them,
      # but in fact a DOUBLE two -- a fork -- don't move here!
      if w in hypo_twos and hypo_twos[w] > 1: continue
      # Otherwise, it meets the condition.  Do it!!
      return i

    #5# Block a fork.
    for i in range(9):

      hypo_match = dc(match)
      if hypo_match.board[i] is None:
        hypo_match.board[i] = self.other_mark
        cells = set()
        for three in hypo_match.threes:
          if sum(hypo_match.board[cell] == self.other_mark for cell in three) == 2:
            for cell in three:
              if hypo_match.board[cell] == None:
                cells.add(cell)
        if len(cells) == 2:
          return i

    #6# Center.
    #A player marks the center. (If it is the first move of the game, playing on a corner gives the second player more opportunities to make a mistake and may therefore be the better choice; however, it makes no difference between perfect players.)
    if match.board[4] is None:
      return 4

    #7# Opposite corner.
    #If the opponent is in the corner, the player plays the opposite corner.
    maps = {0:8,8:0,2:6,6:2}
    corners = [0,2,6,8]
    for corner in corners:

      if match.board[corner] == self.other_mark and match.board[maps[corner]] is None:
        return maps[corner]

    #8# Empty corner
    #The player plays in a corner square.
    empty_corners = [cell for cell in corners if match.board[cell] is None]
    if len(empty_corners) > 0:
      return empty_corners[0]

    #9# Side
    #The player plays in a middle square on any of the 4 sides.
    sides = [1,3,5,7]
    empty_sides = [cell for cell in sides if match.board[cell] is None]
    if len(empty_sides) > 0:
      return empty_sides[0]




class game():
  """
  game contains two players -- humans, monkeys, or computers --
  who then play in a loop.
  """

  mini_num = "012345678"

  threes = [[0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # columns
            [0, 4, 8], [2, 4, 6]]            # diagonals

  def __init__(self, hmark = None, c1 = monkey, c2 = monkey):
    """
    Create a new game.

    :parame hmark: the marker for the human player
    :parame c1:    the class of computer 1, by default a monkey (random)
    :parame c2:    the class of computer 2, by default a monkey (random)
    """

    if hmark:
      if hmark.upper() not in ["X", "O"]:
        print("Human must play either X or O.  Quitting.")
        sys.exit()

      self.cmatch  = False
      self.vmark   = hmark
      self.players = [human(hmark), c1("XO"[hmark == "X"])]

    else:
      self.cmatch  = True
      self.vmark   = "XO"[random.randint(0, 1)]
      self.players = [c1("XO"[self.vmark == "X"]), c2(self.vmark)]

    self.players.sort(key = lambda x: x.mark, reverse = True)
    self.board = [None for x in range(9)]
    self.moves = 9 - self.board.count(None) # for debugging, can set moves...


  def __str__(self):

    s = ""
    for n in range(9):
      if not (n%3): s += "\n"
      if self.board[n]:
        s += self.board[n]
      else: s += game.mini_num[n]
      s += " "
    s += "\n"
    return s


  def play(self):
    """
    play is just a (max) 9 iteration loop
    between the two players defined,
    which returns the winning player (or None).
    """
    winner = ""
    while self.moves < 9 and not winner:
      m = self.players[self.moves % 2].move(self)
      #print(self.moves%2, m)
      while not self.check_move(m):
        m = self.players[self.moves % 2].move(self)
      self.board[m] = ["X", "O"][self.moves % 2]
      self.moves += 1
      winner = self.winner()
    if not self.cmatch:
      print(self)
      print("Alas, our game is at an end!")
      if self.moves < 9:
        print("Congratulations, player {}!!".format(winner))
      if self.moves == 9: print("It is a draw.")
    return winner


  def check_move(self, move):
    """
    Method verifies that the proposed move m is
    (a) legal -- that is, an integer from 0-8 and
    (b) not already taken.
    :param move: proposed move
    :return: boolean True if move is legal, otherwise False.
    """

    if type(move) != int or \
       move > 8 or move < 0:
      print("I require an integer, 0-8!")
      return False

    if self.board[move]:
      print("Players cannot play where there is already a mark!")
      print(self)
      return False

    return True



  def winner(self):
    """
    Method verifies that the proposed move m is
    (a) legal -- that is, an integer from 0-8 and
    (b) not already taken.
    :param move: proposed move
    :return: the winner (or "").
    """

    for m in ["X", "O"]:

      for three in game.threes:
        if all(self.board[sq] == m for sq in three):
          return m

    # Return the winner.  Game will end.
    return ""

  def check_for_wins(self, mark):
    """
    Look for any winning moves for player.
    :param mark: player to search for wins, for.
    :return: location of the first winning move, or None.
    """
    for three in game.threes:
      if sum(self.board[cell] == mark for cell in three) == 2:
        for cell in three:
          if self.board[cell] == None:
            return cell
    return None

  def check_for_twos(self, mark):
    """
    Search for twos
    :param mark: player to search for
    :return: dictionary of with multiplicity of twos created by playing at a location.
    """
    twos = {}
    for three in game.threes:
      diag = [self.board[cell] for cell in three]
      if mark in diag and diag.count(None) == 2:
        for cell in three:
          if not self.board[cell]:
            if cell in twos: twos[cell] += 1
            else: twos[cell] = 1
    return twos



