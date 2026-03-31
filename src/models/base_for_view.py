from typing import List

from src.models.base import X, Synthesis, Progress


class Xshow:
    def __init__(self, x: X, rank: int = 0, effort: int = 1):
        self.x = x
        self.synthesis: SynthesisShow = None

        self.rank = rank
        self.effort = effort

        self.is_root = True
        self.is_tip = False

    def register_synthesis(self, synthesis: Synthesis, xs: List["Xshow"]):
        self.synthesis = SynthesisShow(synthesis, self, xs)
        if synthesis.is_native():
            self.is_tip = True

        return self

    @property
    def name(self):
        return self.x.name

    @property
    def connect(self):
        if not self.synthesis:
            return []
        return self.synthesis.xs


class SynthesisShow:
    def __init__(self, synthesis: Synthesis, ys: Xshow, xs: List[Xshow]):
        self.ys = ys
        self.catalyst = synthesis.catalyst
        self.xs = xs

    def inherit(self, synthesis: Synthesis):
        return (
            (self.ys.name == synthesis.y.name)
            and (self.catalyst == synthesis.catalyst)
            and (len(self.xs) == len(synthesis.x))
            and all(self.xs[i].name == synthesis.x[i].name for i in range(len(self.xs)))
        )
