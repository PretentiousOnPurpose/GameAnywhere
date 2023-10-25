import sys
from pathlib import Path
sys.path.append( str( Path(__file__).parent.parent.parent.parent) )

from typing import Tuple, Union

from game_anywhere.include import run_game
from game_anywhere.include.core.game import AgentId, html
from game_anywhere.include.core import TurnBasedGame, SimpleGameSummary
from game_anywhere.include.components import Component, CheckerBoard

class TicTacToeField(Component):
    def __init__(self):
        super().__init__()
        self.empty = True
        self.player : AgentId = 0

    def __str__(self):
        return ' ' if self.empty else 'X' if self.player==0 else 'O'

    @staticmethod
    def html():
        return ''

BOARD_SIZE = 3

TicTacToeBoard = CheckerBoard.specialize(height=BOARD_SIZE, width=BOARD_SIZE, CellType = TicTacToeField)

def hasRow(player: AgentId, board: TicTacToeBoard, start: Tuple[int, int], step: Tuple[int, int]):
    for i in range(BOARD_SIZE):
        if board[start].empty or board[start].player != player:
            return False
        start = [start[i] + step[i] for i in range(2) ]
    return True

class TicTacToe(TurnBasedGame):
    SummaryType = SimpleGameSummary

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = TicTacToeBoard()

    def turn(self) -> Union[None, SimpleGameSummary]:
        TOTAL_MOVES = self.board.get_size()

        if self.get_current_turn() == TOTAL_MOVES:
            return SimpleGameSummary(SimpleGameSummary.NO_WINNER)

        fields = list(filter( lambda field : field.empty, self.board.all_fields() ))
        print(fields)

        field = self.get_current_agent().choose_one_component(fields)
        print(repr(field))
        field.empty = False
        field.player = self.get_current_agent_index()

        message = "-------\n"
        for row in self.board.board:
            for cell in row:
                message += '|' + str(cell)
            message += "|\n-------\n"

        for agent in self.agents:
            agent.message(message)

        #check rows
        for row in range(BOARD_SIZE):
            if hasRow( self.get_current_agent_index(), self.board, (row, 0), (0, 1)):
                return SimpleGameSummary(self.get_current_agent_id())

        #check rows
        for col in range(BOARD_SIZE):
            if hasRow( self.get_current_agent_index(), self.board, (0, col), (1, 0)):
                return SimpleGameSummary(self.get_current_agent_id())

        #check diagonals
        if hasRow( self.get_current_agent_index(), self.board, (0, 0), (1, 1)):
            return SimpleGameSummary( self.get_current_agent_id() )
        if hasRow( self.get_current_agent_index(), self.board, (0, BOARD_SIZE-1), (1, -1)):
            return SimpleGameSummary( self.get_current_agent_id() )

        return None

    @classmethod
    def html(cls) -> html:
        return TicTacToeBoard.html()

if __name__ == "__main__":
    run_game(TicTacToe, sys.argv);
