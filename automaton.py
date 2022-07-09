from abc import abstractmethod
from pokemon_types import *
import random
import cv2
from collections import Counter


class EvolutionStrategy:
    @abstractmethod
    def find_neighbors(self, board, SIZE, i, j):
        """
        Should return a list of neighbors to consider for the strategy
        given the coords of the current cell
        """

    @abstractmethod
    def find_winner(self, board, SIZE, i, j):
        """
        Should return the new Pokemon in the cell i,j
        """


class SimpleStrategy(EvolutionStrategy):
    def find_neighbors(self, board, SIZE, i, j):
        neighbors = []
        to_try = [(i + k, j + l) for k in range(-1, 2) for l in range(-1, 2)]
        for k, l in to_try:
            neighbors.append(board[k % SIZE][l % SIZE])
        return neighbors

    def find_winner(self, board, SIZE, i, j):
        neighbors = self.find_neighbors(board, SIZE, i, j)
        counter = Counter(neighbors)
        unique_neighbors = list(set(neighbors))
        score = [0 for _ in range(len(unique_neighbors))]

        for idx, neighbor in enumerate(unique_neighbors):
            score[idx] = TypeUtils.get_score(neighbor, board[i][j])

        best_neighbor = unique_neighbors[np.argmax(score)]

        if counter[best_neighbor] >= 2:
            return best_neighbor
        else:
            return board[i][j]


class PokemonAutomaton:
    SIZE = 128
    TYPES = list(PokemonType)
    ITERATIONS = 1000

    def __init__(self, strategy: EvolutionStrategy) -> None:
        self.board = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.strategy = strategy
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
        ).astype(np.uint8)

        return image

    def _update_board(self):
        new_board = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]

        for i in range(self.SIZE):
            for j in range(self.SIZE):
                new_board[i][j] = self.strategy.find_winner(self.board, self.SIZE, i, j)

        self.board = new_board

    def evolution(self):
        it = 0
        while it < self.ITERATIONS:
            self._update_board()
            image = cv2.cvtColor(self.show_board(), cv2.COLOR_RGB2BGR)
            cv2.imshow(
                "image",
                cv2.resize(image, (1024, 1024), interpolation=cv2.INTER_NEAREST),
            )
            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                cv2.destroyAllWindows(image)
                break

            it += 1
        cv2.imshow(
            "image",
            cv2.resize(image, (1024, 1024), interpolation=cv2.INTER_NEAREST),
        )
        if (cv2.waitKey(0) & 0xFF) == ord("q"):
            cv2.destroyAllWindows(image)


if __name__ == "__main__":
    automaton = PokemonAutomaton(SimpleStrategy())
    automaton.evolution()
