from typing import List

from src.models.base import X, Synthesis, Progress
from src.models.base_for_view import Xshow


class Xplus:
    def __init__(
        self,
        x: X,
        show: Xshow = None,
    ):
        self.x = x
        self.show = show if show is not None else Xshow(x)
        self.is_valid = self.x.is_valid or not self.x.synthesises
        if not self.x.synthesises:
            self.show.is_tip = True

    @property
    def is_valid(self):
        return self.x.is_valid

    @is_valid.setter
    def is_valid(self, val: bool):
        self.x.is_valid = val

    def best_synthesis(self, data: dict[X, "Xplus"], border: Progress):
        best = None
        best_score = None

        for synthesis in self.x.synthesises:

            if not synthesis.is_ready(border):
                continue

            child_ranks = [data[y].show.rank for y in synthesis.x]
            child_efforts = [data[y].show.effort for y in synthesis.x]
            score = (
                calculate_total_effort(
                    child_efforts, True if synthesis.catalyst else False
                ),
                calculate_next_rank(child_ranks),
            )

            if best_score is None or score <= best_score:
                best = synthesis
                best_score = score

        return best, best_score

    def can_update(self, data: dict[X, "Xplus"], border: Progress):
        """
        自分の持っている合成ルートのうち、どれか一つでも素材がそろっている場合、
        そのSynthesisオブジェクトを返す。なければNone。
        """
        synthesis, _ = self.best_synthesis(data, border)
        return synthesis

    def update_status(self, synthesis: Synthesis, data: dict[X, "Xplus"]):
        """
        決定した synthesis をもとに自分の数値を更新する
        """
        child_ranks = [data[y].show.rank for y in synthesis.x]
        child_efforts = [data[y].show.effort for y in synthesis.x]
        child_shows = [data[y].show for y in synthesis.x]

        self.show.rank = calculate_next_rank(child_ranks)
        self.show.effort = calculate_total_effort(
            child_efforts, True if synthesis.catalyst else False
        )
        self.show = self.show.register_synthesis(synthesis, child_shows)
        self.is_valid = True

    @property
    def synthesis(self):
        return self.show.synthesis


def calculate_next_rank(child_ranks: List[int]):
    if not child_ranks:
        return 0
    return max(child_ranks) + 1


def calculate_total_effort(child_efforts: List[int], catalyst_exist: bool):
    catalyst_plus = 0.5 if catalyst_exist else 0
    return sum(child_efforts) + catalyst_plus + 1


def to_list_xs(data: dict[X, Xplus]):
    list_xs: List[Xshow] = []
    for xp in data.values():
        if xp.is_valid:
            list_xs.append(xp.show)
    return sorted(list_xs, key=lambda xs: xs.effort, reverse=True)
