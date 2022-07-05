from sklearn import neighbors
from pokemon_types import *
import random
import cv2


class PokemonAutomaton:
    SIZE = 128
    TYPES = list(PokemonType)
    ITERATIONS = 1000

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

    def _update_board(self):
        new_board = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]

        for i in range(self.SIZE):
            for j in range(self.SIZE):
                new_board[i][j] = self._find_winner(i, j)

        self.board = new_board

    def _find_neighbors(self, i, j):
        neighbors = []
        to_try = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        for k, l in to_try:
            if 0 <= k < self.SIZE and 0 <= l < self.SIZE:
                neighbors.append(self.board[k][l])
        return neighbors

    def _find_winner(self, i, j):
        neighbors = self._find_neighbors(i, j)
        score = [0 for _ in range(len(neighbors))]

        for idx, neighbor in enumerate(neighbors):
            score[idx] = TypeUtils.get_score(neighbor, self.board[i][j])

        return neighbors[score.index(max(score))]

    def evolution(self):
        it = 0
        while it < self.ITERATIONS:
            self._update_board()
            image = self.show_board()
            cv2.imshow(
                "image",
                cv2.resize(image, (1024, 1024), interpolation=cv2.INTER_NEAREST),
            )
            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                cv2.destroyAllWindows(image)
                break

            it += 1


if __name__ == "__main__":
    automaton = PokemonAutomaton()
    automaton.evolution()
