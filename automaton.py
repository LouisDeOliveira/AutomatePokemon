from re import I
from pokemon_types import *
import random
import cv2


class PokemonAutomaton:
    SIZE = 128
    TYPES = list(PokemonType)

    def __init__(self) -> None:
        self.board = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self._fill_board()

    def _fill_board(
        self,
    ):

        for i in range(self.SIZE):
            for j in range(self.SIZE):
                self.board[i][j] = random.choice(self.TYPES)

    def show_board(self):
        image = np.array(
            [[TypeUtils.get_color(pokemon) for pokemon in row] for row in self.board]
        )

        return image


if __name__ == "__main__":
    automaton = PokemonAutomaton()
    image = automaton.show_board()
    cv2.imshow("image", cv2.resize(image, (512, 512), interpolation=cv2.INTER_NEAREST))
    cv2.waitKey(0)
