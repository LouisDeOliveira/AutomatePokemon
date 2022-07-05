from pokemon_types import *
import random
import cv2

from collections import Counter


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
        to_try = [(i + k, j + l) for k in range(-1, 2) for l in range(-1, 2)]
        for k, l in to_try:
            neighbors.append(self.board[k % self.SIZE][l % self.SIZE])
        return neighbors

    def _find_winner(self, i, j):
        """
        doit renvoyer le nouveau type de la case i,j en fonction de ses voisins

        """
        neighbors = self._find_neighbors(i, j)
        counter = Counter(neighbors)
        unique_neighbors = list(set(neighbors))
        score = [0 for _ in range(len(unique_neighbors))]

        for idx, neighbor in enumerate(unique_neighbors):
            score[idx] = TypeUtils.get_score(neighbor, self.board[i][j])

        best_neighbor = unique_neighbors[np.argmax(score)]

        if counter[best_neighbor] >= 2:
            return best_neighbor
        else:
            return self.board[i][j]

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
